import time
import os


def ptime(*args):
    """Print a message with timestamp unix"""
    line = ""
    for a in args:
        line += str(a) + " "
    print "[", str(int(time.time())), "]", line


def createFolder(filepath):
    """
    Create a directory if not exits
    https://stackoverflow.com/q/273192/5125608
    """
    filepath = os.getcwd() + "\\" + filepath
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
    except OSError as e:
        raise e
