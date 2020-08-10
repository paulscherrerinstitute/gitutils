from ctypes import *
from ctypes import cdll

import os,sys

class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

def clearMaps():
    # Initialize maps
    initializeMaps = lib.InitializeMaps
    initializeMaps.argtypes = None
    initializeMaps.restype = None
    initializeMaps()


lib = cdll.LoadLibrary("/home/hax_l/software/gitutils/gitutils/glab/bin/libglab.so")
# Defines the maps setter arrcmd
new_arrcmd = lib.NewItemArrCmd
new_arrcmd.argtypes = [c_int, GoString]
new_arrcmd.restype = None
# Defines the maps setter cmdArgs
new_cmdArgs = lib.NewItemCmdArgs
new_cmdArgs.argtypes = [GoString, GoString]
new_cmdArgs.restype = None

# initialize maps for next config cmd
clearMaps()

# sets endpoint and token
endpoint = b"https://git.psi.ch"
url_go = GoString(endpoint, len(endpoint))
token = b"LB97zastgNdJeF5Zyky_"
token_go = GoString(token, len(token))
lib.SetUrlTokenGlobally.argstypes = [GoString, GoString]
lib.SetUrlTokenGlobally.restype = None
lib.SetUrlTokenGlobally(url_go, token_go)

# Exec caller
exec_function = lib.ExecCaller
exec_function.argtypes = [GoString]
exec_function.restype = None
# # initialize maps for next config cmd
clearMaps()
cmd_str = b"issue"
cmd = GoString(cmd_str, len(cmd_str))

list_str = b"list"
list_go = GoString(list_str, len(list_str))
new_arrcmd(c_int(0), list_go)

exec_function(cmd)

# check parameters and set maps inside library
# newCmdArgs = lib.NewItemCmdArgs
# newCmdArgs.argstypes= [GoString, GoString]
# newCmdArgs.restype = None

# cmdArgsKey = b"help"
# cmdArgsKey_go = GoString(cmdArgsKey, len(cmdArgsKey))

# cmdArgsValue = b"true"
# cmdArgsValue_go = GoString(cmdArgsValue, len(cmdArgsValue))

# newCmdArgs(cmdArgsKey_go, cmdArgsValue_go)



# newCmdArgs = lib.NewItemCmdArgs
# newCmdArgs.argstypes= [GoString, GoString]
# newCmdArgs.restype = None

# exec_function(cmd)
quit()