# This governs the installation of the package

import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name='ocean-pentest',  
    version='0.3',
    author="Scott Willett",
    author_email="swillett@protonmail.com",
    description="Automates many tasks for pentesting with the Digital Ocean Cloud Platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scott-m-willett/ocean",
    download_url="https://github.com/scott-m-willett/ocean/archive/refs/tags/v0.2-alpha.tar.gz",
    packages=["ocean","ocean.classes"],
    entry_points = {
        "console_scripts": ['ocean = ocean:main']
    },
    install_requires=['python-digitalocean','paramiko'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)