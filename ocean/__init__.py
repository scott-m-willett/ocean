# This provides other information on the package along with setup.py

import __main__
import sys
from ocean.classes.OceanHandlerModule import OceanHandler
from ocean.classes.OceanDropletModule import OceanDroplet
from ocean.classes.OceanDependencyModule import OceanDependency

def main():
    OceanHandler(sys.argv)

"""
pyexample.

An example python library.
"""

__version__ = "0.2.0"
__author__ = 'Scott Willett'

if __name__ == "__main__":
    import package.__main__
    __main__.main()