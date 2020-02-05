import subprocess

cmd = "lsb_release -d | grep '18'"
output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, executable="/bin/bash").stdout.read().decode()

if (output != ''):
    print("ubuntu v18 detected")
else:
    print("I don't know")

cmd = "lsb_release -d | grep '19'"
output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, executable="/bin/bash").stdout.read().decode()

if (output != ''):
    print("ubuntu v19 detected")
else:
    print("I don't know")