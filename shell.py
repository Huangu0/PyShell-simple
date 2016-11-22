import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func  import *

built_in_cmds = {}
SHELL_RUN = 0


def register_cmd(name, func):
    """
    link the name and func
    """
    built_in_cmds[name] = func


def init():
    """
    display all the command
    """
    register_cmd("cd", cd)
    register_cmd("exit",exit)
    register_cmd("getenv", getenv)
    register_cmd("history", history)


def display_cmd_prompt():
    # get now username
    user = getpass.getuser()
    # use socket.gethostname ruten the computer hostname
    hostname = socket.gethostname()
    # get work_dir
    cwd = os.getcwd()
    # based on cwd to get the base_dir
    # like ,cwd = '/home/huan'   base_dir = ""huan"
    base_dir = os.path.basename(cwd)
    # use ~ replace the home_dir
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = "~"

    # print the prompt
    if platform.system() != "Windows":
        sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (
            user, hostname, base_dir))
    else:
        sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
    sys.stdout.flush()


def ignore_signs():
    if platform.system() != "Windows":
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def tokenize(string):
    # split shell cmd like
    # ls -l /home/  ->  ["ls","-l ","/home/"]
    return shlex.split(string)


def preprocess(tokens):
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
    # get the envirment
            processed_token.append(os.getenv(token[1:]))
            
        else:
            processed_token.append(token)
    return processed_token

def handler_kill(signum,frame):
    raise OSError("Killed!")

def execute(cmd_tokens):
    with open(HISTORY_PATH,"a") as history_file:
        history_file.write(' '.join(cmd_tokens)+os.linesep)
    if cmd_tokens:
        cmd_name = cmd_tokens[0]
        cmd_args = cmd_tokens[1:]
    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)
    signal.signal(signal.SIGINT,handler_kill)
    if platform.system() != "Windows":
        p = subprocess.Popen(cmd_tokens)
        p.communicate()
    else:
        command = ""
        command = " ".join(cmd_tokens)
        os.system(command)
    return SHELL_RUN

def shell_loop():
    """
	realize the shell loop
	while status == 0,shell_loop break out
    """
    status = SHELL_RUN
    while status == SHELL_RUN:
	"""
	"""
	# print the prompt ,and format like"[<user>@<hostname> <base_dir>]$"
        display_cmd_prompt()
	# ignore the Ctrl_Z or Ctrl+C
        ignore_signs()
	
        try :
		# read the cmd from the stdin
            cmd = sys.stdin.readline()
		# split the cmd to a list 
            cmd_tokens = tokenize(cmd)
	    	# make the var replace to "true var"
            cmd_tokens = preprocess(cmd_tokens)
		# run the cmd and return the status
            status = execute(cmd_tokens)
        except:
		# sys.exc_info()return 3 var(type,value,traceback),
		# but only need the middle,that is a error 
            _,err,_ = sys.exc_info() 
            print(err)

def main():
    # before the shell start,app need to be init
    # when init() run,the define func will be registered 
    init()
    # the main func
    shell_loop()

if __name__ == "__main__":
    main()  




