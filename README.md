Ocean
=====

Pentesting automations with the Digital Ocean Cloud Platform and Droplets (VMs).

It provides a way to easily provision penetration testing VMs in digital ocean for various purposes in an efficient and economical way, for example:
- Use hack tools
- Set up proxies for use with proxychains
- Tunnel traffic through a droplet

After creating a custom lightweight kali image and uploading it, this tool allows you to rapidly provision those kali machines and control them. The idea is to extend your pentesting footprint into the cloud in an efficient and econommical way.

https://pypi.org/project/ocean-pentest/0.3/

pip3 install ocean-pentest


ToDo / Bugs
-----------

1. Multithreading when working with multiple machines (--cmd, --create, --destroy)

2. Add --list option to view limits and account settings. Also to filter other options based on name or tag

3. Look at getting the --image command to set the environment variable

4. Separate and modularise functions in OceanHandler and OceanDroplet (after writing tests0

5. Write more tests for current functionality. Separate and organise better.

6. More commenting and documentation.

7. Add error handling

8. Add a --scan function to quickly scan the droplet IPs with nmap

9. Allow --cmd to run a command depending on name or tag

10. Allow create to add tags to a machine or number of machines

11. Allow destruction based on a tag or name

12. More guides in doco to digital ocean KB articles and the like - help assumes to much of users at times

13. Provide guidance on creating and uploading a custom kali image to digital ocean

14. Test on multiple platforms (only one platform tested so far)

15. Consider providing my own kali-rolling image via github or similar

16. Better output from the --cmd command (try printing the host to stderr so stdout can be redirected, or provide text so output can be cut and grepped)

17. Look at a --deploy switch to upload a local or remote image, and set it as the active image automatically 

18. Look at creating profile scripts to orchestrate scenarios (eg: setting up 10 socks5 proxies, create a scan box and a rshell handler)

19. Create a --setup and/or --check command to check and upload ssh-keys, check and set the active image, check installed programs (ssh, nmap), check dependencies, check account status and credits

20. Handling: no internet

21. Look at a --proxy switch to move traffic for this script through a http or socks4/5 proxy

22. Better formatting of the README.md doc (eg: code, headings).

23. More detail and examples of commands

24. ASCII art banner for help - gotta do it (does argsparse provide options for this?)

25. Look at a feature to assist in creating a new account and auto setting the env var (if possible) (--new-account?)


Setup
-----

Install this python3 package with pip3: pip3 install ocean-pentest

Create an account at Digital Ocean with my referral link (both you and I get free credit): https://m.do.co/c/dcd323d4b19c
I highly recommend creating a dedicated account for your pentesting tasks. DO NOT USE AN ACCOUNT WITH PRODUCTION SERVERS IN IT.

Get your API key from your account page and put it into an environment variable on your machine (digitalocean_token).

You can build your own custom image and upload with a process such as this: https://medium.com/@hackthebox/how-to-deploy-a-kali-linux-distribution-in-digital-ocean-cloud-c556edf17741
My own instructions on this to come.

For custom images, you need to put the ID of the machine into an environment variable (digitalocean_image). You can use "ocean --image #image_name#" to retrieve this from your account.
You can use a generic image such as ubuntu-20-04-x64 by simply putting that value into the environment variable (digitalocean_image)

Setup a passwordless ssh public key with ssh-keygen in your terminal. Ocean may be able to do this for you (untested).


Help
----

ocean -h

ocean --help

ocean


Create Droplets
----------------

You can automatically create one or many droplets. Below are all valid commands.

ocean --create

ocean --create --number 10

ocean --create --number 1

Other options for create are listed in the command help (ocean -h).


Destroy Droplets
----------------

ocean --destroy

You will be prompted to confirm, then all droplets will be destroyed.

BE CAREFUL WITH THIS COMMAND IF YOU HAVE A PRODUCTION SERVER IN YOUR ACCOUNT. UNLIKELY YOU WILL GET IT BACK.


Interact with Droplets
----------------------

Run a command on all current droplets with --cmd

eg: ocean --cmd "hostname && whoami && curl ipinfo.io/ip"

You can also ssh into a box by its name and avoid looking up the IP, accepting cert keys etc:

ocean --ssh ocean1


List Information
----------------

This will list all your current droplets, along with their IPs and current status.

ocean --list droplets

This will list all your current droplets in a list useful for your proxychains.conf file ("socks5 #IP# 80").

ocean --list proxychains

This will show all available regions in a comma seperated list.
Some regions excluded due to issues: https://docs.digitalocean.com/products/platform/availability-matrix/
"only users who already have existing resources in those regions can create more resources there."

ocean --list regions

This will show all available sizing options for droplets. The default sizes used for ocean is "s-1vcpu-1gb" (smallest and cheapest).

ocean --list sizes