import os


def is_pid_running(pid):
    """ Check for the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
