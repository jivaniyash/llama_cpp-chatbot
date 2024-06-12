# pip install docstring_parser

import ast
import inspect
import docstring_parser
from typing import Any, get_type_hints
import types
import typing

# edited from source https://github.com/janekb04/py2gpt/blob/main/main.py
def create_openai_function_description(func_obj):
    defaults: dict[str, Any] = {}

    source = inspect.getsource(func_obj) # Get the source code of the function
    module = ast.parse(source) # Parse the source code into an AST
    func:ast.FunctionDef = module.body[0] # Extract the function definition node
    for i, arg in enumerate(reversed(func.args.defaults)):
        if not isinstance(arg, ast.Constant):
            raise ValueError("Only constant default values are supported")
        defaults[func.args.args[-i - 1].arg] = arg.value

    docstring = func.body[0].value.s

    try:
        parsed_docstring = docstring_parser.parse(docstring)
    except docstring_parser.ParseError as e:
        raise ValueError("Invalid function docstring format") from e

    func_name = func.name

    type_hints = get_type_hints(func_obj, globals(), defaults)

    args = [arg.arg for arg in func.args.args]

    for doc_param in parsed_docstring.params:
        if doc_param.arg_name not in args:
            raise ValueError(
                f"Docstring describes non-existing argument: {doc_param.arg_name}"
            )
        if (
            "optional" in doc_param.description.lower()
            and doc_param.arg_name not in defaults
        ):
            raise ValueError(
                f"Docstring marks parameter {doc_param.arg_name} as optional but it doesn't have a default value"
            )
        if (
            "required" in doc_param.description.lower()
            and doc_param.arg_name in defaults
        ):
            raise ValueError(
                f"Docstring marks parameter {doc_param.arg_name} as required but it has a default value"
            )
        if (
            (doc_param.type_name is not None)
            and (doc_param.arg_name in type_hints)
            and (eval(doc_param.type_name) != type_hints[doc_param.arg_name])
        ):
            raise ValueError(
                f"Type hint {type_hints[doc_param.arg_name]} for parameter {doc_param.arg_name} doesn't match with it's description in docstring {eval(doc_param.type_name)}"
            )
        if (doc_param.type_name is None) and (doc_param.arg_name not in type_hints):
            raise ValueError(
                f"Docstring doesn't describe type of parameter {doc_param.arg_name}"
            )
        if (
            doc_param.description is None
            or doc_param.description.isspace()
            or doc_param.description == ""
        ):
            raise ValueError(
                f"Docstring doesn't describe parameter {doc_param.arg_name}"
            )
    doc_arg_names = [doc_param.arg_name for doc_param in parsed_docstring.params]
    for arg in args:
        if arg not in doc_arg_names:
            raise ValueError(f"Docstring doesn't include argument: {arg}")

    if parsed_docstring.raises and (
        len(parsed_docstring.raises) != 1
        or parsed_docstring.raises[0].type_name != "None"
    ):
        raise ValueError("The function should not raise any exception")

    if (parsed_docstring.returns is not None) and (
        eval(parsed_docstring.returns.type_name) != type_hints.get("return")
    ):
        raise ValueError(
            f"Return type {type_hints.get('return')} doesn't match with it's description in docstring {eval(parsed_docstring.returns.type_name)}"
        )

    if (
        parsed_docstring.short_description is None
        or parsed_docstring.short_description.isspace()
        or parsed_docstring.short_description == ""
    ):
        raise ValueError("Docstring doesn't describe function")

    param_jsons = {}
    for param in parsed_docstring.params:
        name = param.arg_name
        description = param.description
        t = eval(param.type_name) if param.type_name is not None else type_hints[name]
        type_descriptor = get_type_descriptor(t)
        param_jsons[name] = {"description": description, **type_descriptor}

    return {
        "type":"function",
        "function":{
            "name": func_name,
            "description": parsed_docstring.short_description,
            "parameters": {
                "type": "object",
                "properties": param_jsons,
            },
            "required": [name for name in args if name not in defaults],
        }
    }


def get_type_descriptor(t: type) -> dict:
    if t == str:
        return {"type": "string"}
    elif t == int:
        return {"type": "integer"}
    elif t == float or t == int | float:
        return {"type": "number"}
    elif t == bool:
        return {"type": "boolean"}
    elif t == type(None):
        return {"type": "null"}
    elif t == list:
        return {"type": "array"}
    elif t == dict:
        return {"type": "object"}
    elif type(t) == types.GenericAlias:
        if t.__origin__ == list:
            return {"type": "array", "items": get_type_descriptor(t.__args__[0])}
        elif t.__origin__ == dict:
            if t.__args__[0] != str:
                raise ValueError(f"Unsupported type (JSON keys must be strings): { t}")
            return {
                "type": "object",
                "patternProperties": {".*": get_type_descriptor(t.__args__[1])},
            }
        else:
            raise ValueError(f"Unsupported type: {t}")
    elif type(t) == typing._LiteralGenericAlias:
        for arg in t.__args__:
            if type(arg) != type(t.__args__[0]):
                raise ValueError(f"Unsupported type (definite type is required): {t}")
        return {**get_type_descriptor(type(t.__args__[0])), "enum": t.__args__}
    else:
        raise ValueError(f"Unsupported type: {t}")