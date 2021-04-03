import argparse
import sys
import paramiko
import time
import subprocess
import digitalocean

from ocean.classes.OceanDependencyModule import OceanDependency
from ocean.classes.OceanDropletModule import OceanDroplet

# https://blogs.gnome.org/markmc/2012/11/26/cfg-and-argparse-sub-commands/
# Parses / handles commands. Intend to move bits to other modules eventually. Messy at the moment
class OceanHandler:
    
    def __init__(self, arguments):
        self.ocean_dependency = OceanDependency()
        self.ocean_droplet = OceanDroplet()
        self.create_parsers()
        
        
    # Issue - help only shows for the original parser
    def create_parsers(self):
    
        # The main parser
        self.main_parser = argparse.ArgumentParser(prog="ocean", description='Pentesting automations with the Digital Ocean Cloud Platform and Droplets (VMs).')
        self.main_parser.add_argument('--destroy', action="store_true", help='Destroy all droplets after confirmation.')
        self.main_parser.add_argument('--ssh', help='Specify a droplet name to ssh into it.')
        self.main_parser.add_argument('--cmd', help='Run a command on all boxes.')
        self.main_parser.add_argument('--image', help='Get the id of a given image name. Use this to create and environment variable (digitalocean_image) to set the image. Type "show" to read the environment variable.')
        self.main_parser.add_argument('--list', choices=['droplets', 'proxychains', 'regions', 'sizes'], help='List information.')
        self.main_parser.add_argument('--create', action='store_true', help='Create Droplets')
        self.main_parser.add_argument('--name', help='Provide an optional name for the Droplet. Default will be the type followed by a sequential number (eg: kali2) if unspecified.')
        self.main_parser.add_argument('--number', type=int, default=1, help='The number of Droplets to create, account droplet_limits permitting. One Droplet is created if unspecified.')
        self.main_parser.add_argument('--region', help='The region to create the Droplet. A random region is select if unspecified.')
        self.main_parser.add_argument('--size', default="s-1vcpu-1gb",help='Droplet sizing and spec options. Default is "s-1vcpu-1gb" (smallest and cheapest) if unspecified.')  

        # Parse the arguments
        main_args = self.main_parser.parse_args()
        
        # There should only be one of these in a command. Exit if there is more than one. Print help if it isn't equal to 1.
        main_arg_count = 0
        if main_args.destroy != False:
            main_arg_count += 1
        if main_args.ssh is not None:
            main_arg_count += 1
        if main_args.cmd is not None:
            main_arg_count += 1
        if main_args.image is not None:
            main_arg_count += 1
        if main_args.list is not None:
            main_arg_count += 1
        if main_args.create != False:
            main_arg_count += 1
        if main_arg_count != 1:
            self.main_parser.print_help()
            sys.exit()
            
        # List info, depending on the choice provided
        if main_args.list is not None:
            if main_args.list == "droplets":
                self.ocean_droplet.list_droplets()
            if main_args.list == "proxychains":
                self.ocean_droplet.list_proxychains()
            if main_args.list == "regions":
                print(self.ocean_droplet.get_regions_comma())
            if main_args.list == "sizes":
                print(self.ocean_droplet.get_sizes_comma())

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