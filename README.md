Ocean
=====

Pentesting automations with the Digital Ocean Cloud Platform and Droplets (VMs).

It provides a way to easily provision penetration testing VMs in digital ocean for various purposes, for example:
- Use hack tools
- Set up proxies for use with proxychains
- Tunnel traffic through a droplet

https://pypi.org/project/ocean-pentest/0.3/

Setup
-----

Install this python3 package with pip3: pip3 install ocean-pentest

Create an account at Digital Ocean with my referral link (both you and I get free credit): https://m.do.co/c/dcd323d4b19c

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