# This governs the installation of the package

import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name='ocean',  
    version='0.2',
    author="Scott Willett",
    author_email="swillett@protonmail.com",
    description="Automates many tasks for pentesting with the Digital Ocean Cloud Platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scott-m-willett/Ocean",
    packages=["ocean","ocean.classes"],
    entry_points = {
        "console_scripts": ['ocean = ocean:main']
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)