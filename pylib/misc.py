
"""
This file will have miscellaneous python functions are utils can use.
"""

def filenm_from_key(key):
    """
    Get rid of spaces in a name for easier UNIX file names.
    """
    return key.replace(" ", "_")
