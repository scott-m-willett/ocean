import argparse
import sys
import paramiko
import time
import subprocess

from classes import OceanDependency
from classes import OceanDroplet

# https://blogs.gnome.org/markmc/2012/11/26/cfg-and-argparse-sub-commands/
class OceanHandler:
    
    def __init__(self, arguments):
        self.ocean_dependency = OceanDependency.OceanDependency()
        self.ocean_droplet = OceanDroplet.OceanDroplet()
        self.create_parsers()
        
        
    # Issue - help only shows for the original parser
    def create_parsers(self):
    
        # The main parser
        self.main_parser = argparse.ArgumentParser(prog="ocean", description='Pentesting automations with the Digital Ocean Cloud Platform and Droplets (VMs).')
        self.main_parser.add_argument('--destroy', action="store_true", help='Destroy all droplets after confirmation.')
        self.main_parser.add_argument('--ssh', help='Specify a droplet name to ssh into it.')
        self.main_parser.add_argument('--cmd', help='Run a command on all boxes.')

        self.main_parser.add_argument('--image', help='Get the id of a given image name. Use this to create and environment variable (digitalocean_image) to set the image. Type "show" to read the environment variable.')
        
        self.main_parser.add_argument('--create', action='store_true', help='Create Droplets')
        self.main_parser.add_argument('--name', help='Provide an optional name for the Droplet. Default will be the type followed by a sequential number (eg: kali2) if unspecified.')
        self.main_parser.add_argument('--number', type=int, default=1, help='The number of Droplets to create, account droplet_limits permitting (check with --list limits). One Droplet is created if unspecified.')
        self.main_parser.add_argument('--region', help='The region to create the Droplet. A random region is select if unspecified. Options: ' + self.ocean_droplet.get_regions_comma())
        self.main_parser.add_argument('--size', default="s-1vcpu-1gb",help='Droplet sizing and spec options. Default is "s-1vcpu-1gb" (smallest and cheapest) if unspecified. Options: ' + self.ocean_droplet.get_sizes_comma())  

        main_args = self.main_parser.parse_args()
        
        # Run a command on all droplets
        if main_args.cmd is not None:
            manager = digitalocean.Manager(token=self.ocean_dependency.token)
            my_droplets = manager.get_all_droplets()
            for droplet in my_droplets:
                ip = droplet.networks['v4'][1]['ip_address']
                ssh_connection   = paramiko.SSHClient()
                ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_connection.connect(ip, username='root', key_filename=self.ocean_dependency.key_file)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh_connection.exec_command(main_args.cmd)
                print(droplet.name)
                for line in ssh_stdout.readlines():
                    print(line)
                ssh_connection.close()
        
        # ssh into the box given the droplet name. Don't check the key.
        if main_args.ssh is not None:
            ip = self.ocean_droplet.get_droplet_ip(main_args.ssh)
            cmd = 'ssh -o StrictHostKeyChecking=no root@' + ip
            subprocess.call(cmd, shell=True)
        
        # Show the set image, or find the id of an image
        if main_args.image is not None:
            if main_args.image == "show":
                print(os.environ["digitalocean_image"])
            else:
                self.ocean_droplet.set_droplet_image(main_args.image)
            sys.exit()
            
        # Destroy droplets after confirmmation
        if main_args.destroy is True:
            destroy = input("This will destroy all ocean droplets. Are you sure? (y/n): ")
            if destroy == "y":
                self.ocean_droplet.destroy_droplets()
                sys.exit()
            else:
                sys.exit()
            # prompt y or n, then action
        
        # Create droplets based on args
        if main_args.create is True:
            self.ocean_droplet.create_droplets(main_args.name, main_args.number, main_args.region, main_args.size)  
            sys.exit()
            

