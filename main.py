#!/usr/bin/env python3

import sys, os, subprocess
import json, datetime, glob


def backup_apt():
    cmd = """comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u)"""
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash").stdout.read().decode().split('\n')
    del output[-1]
    i = 0
    while i < len(output):
        cmd = "apt-cache policy " + output[i] + "| sed -n 2p"
        output[i] += "=" + subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash").stdout.read().decode().split(' ')[-1]
        output[i] = output[i][:-1]
        i += 1
    apt = {}
    apt["app"] = "apt-get"
    apt["arg"] = "install"
    apt["src"] = output
    return apt

def backup_pip():
    if subprocess.call(["pip", "--version"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True) == 0:
        pip = {}
        cmd = "pip list --user"
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, executable="/bin/bash").stdout.read().decode().split('\n')
        if len(output[0]) == 0:
            return None
        pip["app"] = "pip"
        pip["arg"] = "install"
        pip["src"] = output
        return pip
    else:
        print('pip not installed')
    return None

def backup_pip3():
    if subprocess.call(["pip3", "--version"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True) == 0:
        pip3 = {}
        cmd = "pip3 list --user"
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, executable="/bin/bash").stdout.read().decode().split('\n')
        pip3["app"] = "pip3"
        pip3["arg"] = "install"
        pip3["src"] = output
        del pip3["src"][0]
        del pip3["src"][0]
        del pip3["src"][-1]
        for x in range(len(pip3["src"])):
            a = pip3["src"][x].split(" ")[0]
            b = pip3["src"][x].split(" ")[-1]
            print(pip3["src"][x].split(" "))
            pip3["src"][x] = a + "==" + b

filter(lambda a: a != 2, x)

        return pip3
    else:
        print('pip3 not installed')
    return "None"

def backup():
    backup = {}
    backup["apt"] = backup_apt()
    backup["pip"] = backup_pip()
    backup["pip3"] = backup_pip3()
    return backup

def restore(name, version):
    if not name:
        list_of_files = glob.glob('*.json')
        json_file = max(list_of_files, key=os.path.getctime)
    else:
        json_file = name
    try:
        with open(json_file) as json_data:
            restore_json = json.load(json_data)
    except:
        print("No such file or directory")
        exit(0)
    for (name, data) in restore_json["backup"].items():
        if data:
            for package in data["src"]:
                if package and version == 0:
                    print(f'sudo {data["app"]} {data["arg"]} {package.split("=")[0]}')
                elif package and version == 1:
                    print(f'sudo {data["app"]} {data["arg"]} {package}')
    




def main():
    if sys.argv[1] == "--backup" or sys.argv[1] == "-b":
        main_json = {}
        if len(sys.argv) == 2:
            main_json['backup'] = backup()
            name = "backup-" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".json"
            with open(name, "w") as file:
                json.dump(main_json, file, indent=4, sort_keys=True)
        else:
            main_json['backup'] = backup()
            with open(sys.argv[2] + ".json", "w") as file:
                json.dump(main_json, file, indent=4, sort_keys=True)
    elif sys.argv[1] == "--restore" or sys.argv[1] == "-r":
        if len(sys.argv) == 3:
            restore(sys.argv[2], 0)        
        else:
            restore("", 0)
    elif sys.argv[1] == "--restore-version" or sys.argv[1] == "-rv":
        restore("", 1)

    else:
        usage()

def usage():
    print("\nUsage")
    print("   myApp <command> [options]\n")
    print("Commands\n   -b, --backup [output_json_name]\t\tsave system configurationin ouput file [name]")
    print("   -r, --restore [input_json_name]\t\trestore from last file, or file defined by his name")
    print("   -v, --version \t\t\t\tdisplay EasyPizi version\n")
    exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h")):
        print(usage())
    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        print("EasyPizi Alpha 0.0.1")
        exit(0)
    main()



