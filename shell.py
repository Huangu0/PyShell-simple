import os,sys,shelx,getpass,socket,signal,subprocess,platform
from func  import *

built_in_cmds = {}

def register_cmd(name,func):
    """
	link the name and func
    """
    built_in_cmds[name]=func

def init():
    """
	display all the command
    """
    register_cmd("cd",cd)
    register_cmd("exit".exit)
    register_cmd("getenv",getenv)
    register_cmd("history",history)

def shell_loop():
    """
	realize the shell loop
    """
    status = SHELL_RUN
    while status == SHELL_RUN:
	"""
	"""
	#print the prompt "$"
	display_cmd_prompt()
	# ignore the Ctrl_Z or Ctrl+C
	ignore_signs()
	
	try :
		#read the cmd from the stdin
	    cmd = sys.stdin.readline()
		#split the cmd to a list 
	    cmd_tokens = tokenize(cmd)
	    	#	
	    cmd_tokens = preprocess(cmd_tokens)
	    status = execute(cmd_tokens)   
