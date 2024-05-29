### Create ssh key and connect to VM with Termainal & VS Code (Windows)

1. Create ssh key
    - Run `ssh-keygen -t rsa -f C:\Users\<WINDOWS_USER>\.ssh\<KEY_FILENAME> -C <USERNAME> -b 2048` in command  shell    
    - Open <KEY_FILENAME.pub> and copy the contents

2. Create VM instance in GCP
    - Create Project
    - Enable `Compute Engine API`
    - Click on Left menu -> `Compute Engine` -> `VM instances` -> `Create Instance` -> Edit the configuration based on requirements 

3. Add SSH key in VM
    - Click on Left menu -> `Compute Engine` -> `Metadata` -> `SSH key` -> `Add SSH key` -> Paste it and save changes

4. Create firewalls to prevent other hosts to access
    - Type `ipconfig` to and copy `IPv4 Address` of local machine 
    - Click on Left menu -> `VPC Network` -> `Firewall` ->  `Create Firewall Rule` -> Make changes to the firewall rule -> Paste the `IPv4 Address` to `Source IPv4 ranges` box

5. Connect Terminal with VM instance
    - Go to `VM Instance` -> `Select Instance` -> `Network interfaces` -> `External IP address` - Copy IP address
    - Type `ssh -i  C:\Users\<WINDOWS_USER>\.ssh\<KEY_FILENAME> <USERNAME>@<External_IP>` in command shell

6. Connect VS Code with VM instance
    - Install VS code if not installed
    - Install `Remote -SSH` Extension
    - Press `Ctrl + Shift + P` -> Search `Add New Host` -> type `ssh <USERNAME>@<External_IP> -i  C:/Users/<WINDOWS_USER>/.ssh/<KEY_FILENAME>`
    - Select the config file to be updated
    - Press `Ctrl + Shift + P` -> Search `connect to Host`-> Click on the `<External IP Address>` from the list
    - This will open a new VS code Window connected with the VM instance.
    - Select the remote OS
