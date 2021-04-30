"""
This module will generate an index page for pydoc generated documentations
files in a particular directory.ç:w
"""
import os
import glob

def main():
    for name in glob.glob('*.py'):
        print(f"name = {name}")

if __name__ == "__main__":
    main()
