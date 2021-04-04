import os
import sys
import shutil
import digitalocean
from digitalocean import SSHKey

# Ensures prerequisites, expected configurations and dependencies are met for this program, and corrects and advises if it isn't
# Also for checking account related info
# API token accessible from this class
class OceanDependency:
    
    # Initialiser
    def __init__(self,check_ssh=False):
        self.set_token()
        
        # Only verify ssh keys online if explicitly requested
        if check_ssh == True:
            self.check_ssh_installed()
            
        self.set_ssh_key(check_ssh)
    
    # Gets the DigitalOcean API key from and environment variable, and exits with a message if it can't be found
    # Also sets up a manager object to work with digital ocean using this token
    def set_token(self):
        self.token = os.environ['digitalocean_token']
        if self.token == None:
            print("You need to set an environment variable (digitalocean_token) to your DigitalOcean cloud API key.")
            # Advice: Create an account, find the api, set an environment variable in Linux or Windows
            sys.exit()
         
    # checks that SSH is installed. Exists the program with a message if it isn't
    def check_ssh_installed(self):
        result = shutil.which('ssh')
        if result == None:
            print("Program SSH is missing. Fatal issue. The ssh command must be available on your system.")
            sys.exit()
            
     # Checks if nmap is installed and returns a true or false result depending
    def check_nmap_installed(self):
        result = shutil.which('nmap')
        if result == None:
            return False
        else:
            return True
            
    # Gets the SSH key for the system. It is created if it doesn't exist. It is uploaded to DigitalOcean if it doesn't exist there too.
    def set_ssh_key(self, check_ssh):
        
        # Where our RSA key chould exist
        self.key_file = (os.path.expanduser('~') + '/.ssh/id_rsa.pub')
        key_file = (os.path.expanduser('~') + '/.ssh/id_rsa.pub')
        
        # If the RSA key doesn't exist, create it
        if check_ssh == True:
            if os.path.isfile(key_file) != True:
                os.system("ssh-keygen -b 2048 -t rsa -f " + key_file + " -q -N ") 
            # Set the member value ssh_key to the value of this file
            ssh_file = open(key_file)
            self.ssh_key = ssh_file.read().strip()
            ssh_file.close()
        
        if check_ssh == True:
            # Upload the SSH key to digital ocean if it isn't there already
            key_installed = False
            manager = digitalocean.Manager(token=self.token)
            keys = manager.get_all_sshkeys()
            for key in keys:
                if key.public_key == self.ssh_key:
                    key_installed = True
            if key_installed == False:
                key = SSHKey(token=digitalocean_token,
                         name='ocean_key_' + str(random.randint(11111,99999)),
                         public_key=self.ssh_key)
                key.create()
            
    # Check account limits to see how many droplets we're allowed to create
    def get_droplet_limit(self):
        manager = digitalocean.Manager(token=self.token)
        account = manager.get_account()
        return account.droplet_limit
        
    # Given the current number and the number of droplets to be created, check if the droplet limit will be reached for the account
    def check_limit(self,current_number,create_number):
        limit = self.get_droplet_limit()
        number = (current_number + create_number)
        return (number <= limit)