"""
1. utils functions
"""
import time
import shlex
import datetime


def getTime():
    """
    return accurate time point in format: Year-Month-Day-Hour:Minute:Second.unique_labels
    """ 
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S.%f')

def getUsername():
    cmd = "whoami"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    return out


def mergeDict(old=None, new=None):
    if new is None:
        return old

    for item in new:
        old[item] = new[item]

    return old


def getJobID(out):
    if "<" not in out or ">" not in out:
        return None
    else:
        return out.split("<")[1].split(">")[0]

def argsToCommand(args, item=None, _iter=None):
    command = ""
    if item is None:
        for each in args:
            if args[each] is None:
                continue 
            command += " --"+str(each)+" "+str(args[each])
        return command
    elif item is not None and _iter is None:
        for each in item:
            if each in args and args[each] is not None:
                command += " --"+str(each)+" "+str(args[each])
        return command
    elif item is not None and _iter is not None:
        for idx, each in enumerate(item):
            if each in args and args[each] is not None:
                command += " --"+str(_iter[idx])+" "+str(args[each])
        return command
    else:
        return command

