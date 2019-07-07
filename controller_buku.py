import subprocess
from subprocess import PIPE, DEVNULL, check_output, call
import sys
import os
import colorama

from utils.spinner import Spinner

PROJECT_NAME = "BMM"
# EXPORT_FILE_PATH = "./temp/bukuExport.html"
# ERASE_BEFORE_INIT = False

def run(ERASE_BEFORE_INIT = False, EXPORT_FILE_PATH = "./temp/browserExport.html", mute = False):
    try:
        output = check_output(["buku", "-v"], stderr=PIPE)   # Avoid using shell=True for security issues, however it's safe for use here though, cause no user input is used.
        if output:  output = output.decode("ascii").strip()
        if not mute: print("Buku version("+output+") Detected!")


        if(ERASE_BEFORE_INIT == True):
            print("\n Erasing Buku Database before Export Initialization")
            call("expect ./bukuOps/bukuErase.sh", shell=True)


        if not mute:
            sys.stdout.write("\n> Auto-Importing bookmarks from all available browsers: ")
            with Spinner():
                call("expect ./bukuOps/bukuAI.sh", shell=True, stdout=DEVNULL)
        else: call("expect ./bukuOps/bukuAI.sh", shell=True, stdout=DEVNULL)


        if os.path.exists(EXPORT_FILE_PATH):
            os.remove(EXPORT_FILE_PATH)
        out = check_output(["buku", "-e", EXPORT_FILE_PATH])
        if out: out = out.decode("ascii").strip()

        if not mute:
            print("\n\t Buku Status:", out)
            print("\n")


    except subprocess.CalledProcessError as e:
        print("\'Buku\' Not Found!")
        print("BMM uses Buku as a temporary backend tool for interacting with your browser...")
        print("Please install Buku through: https://github.com/jarun/Buku\n")



if __name__ == '__main__':
    colorama.init(autoreset = True)
    print(colorama.Fore.WHITE + colorama.Back.RED + 'Warning! This script is to be run internally by ' + PROJECT_NAME + ' scripts, direct use might lead to unexpected behaviour\n')
    # print('\x1b[6;37;41m' +  + '\x1b[0m' + '\n')
    run()
