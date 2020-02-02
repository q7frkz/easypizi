def usage():
    print("\nUsage")
    print("   ./easypizi <command> [options]\n")
    print("Commands\n   -b,  --backup [output_json_name]\t\tsave system configurationin ouput file [name]")
    print("   -r,  --restore [input_json_name]\t\trestore all packages in json without specific version")
    print("   -rv, --restore-version [input_json_name]\trestore all packages in json with regitered version")
    print("   -ra, --restore-auto [input_json_name]\trestore all packages, with specific version if possible")
    print("   -v,  --version \t\t\t\tdisplay EasyPizi version\n")
    exit(0)

ERROR = "\nERROR: Ubuntu version not detected!\nEasypizi only works on Ubuntu18 and Ubuntu19\nEasypizi only works on French and English version\n"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'