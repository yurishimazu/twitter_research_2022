import os
import fcntl

def process_lock():
    lockfile = os.path.splitext(os.path.abspath(__file__))[0] + '.lock'
    lockfp = open(lockfile, "w")
    try:
        fcntl.flock(lockfp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return
    return lockfp
