import sys
import subprocess
import os
import platform

def CALL_LOGO(): # function prints out logo upon call
    Logo = r"""
  _____    _             
 |  ___|__| |_ ___  __ _ 
 | |_ / __| __/ _ \/ _` |
 |  _|\__ \ ||  __/ (_| |
 |_|  |___/\__\___|\__, |
                   |___/ 
    """
    print(Logo)
    
def QUIT(): # closes Fsteg
    try: # this uses a try except clause to hide any errors upon closing
        sys.exit()
    except SystemExit:
        pass

def PRINT_INSTR(): # responsible for formatting the instructions
    instr = r"""
  To continue, please enter a flag to be run on the file. (Enter the flag letter without the '-')

  -L : Uses LSB steganography to check for hidden data.
  -Lp [password] : Uses LSB steganography to check for hidden data with a password
  -q : Exits Fsteg

    """
    print(instr)

def get_steg_path(): # this function returns the path to the steghide binary based on the OS of the running device
    opsys = platform.system() # finds OS of the running device and references the steghide in bin accordingly
    if opsys == "Windows":
        return os.path.join("bin", "Windows", "steghide.exe")
    elif opsys in ["Linux", "Darwin"]:  # Darwin = macOS
        return os.path.join("bin", "Unix", "steghide")
    else:
        raise Exception("Unsupported OS")

def steg_extract(spath, passw):
    build_cmd = [ # this builds out the steghide command to perform the extraction
        spath,
        "extract",
        "-sf", fpath,
        "-p", passw,
        "-xf", "extracted.txt"
    ]

    try: # runs command with subprocess
        result = subprocess.run(build_cmd, capture_output=True, text=True, check=True)
        print("Steghide Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)

def Lfunction(): # gathers steghide filepath and then calls the stegextract function with no pass.
    relpath = get_steg_path()
    nopass = ""
    steg_extract(relpath, nopass)

def Lpfunction():
    print("Write Me!")

flag_dict = { # This is where the acceptable flags and their associated functions are stored in a dictionary
    "L" : Lfunction,
    "Lp" : Lpfunction,
    "q" : QUIT
}

def init(): # initializes program; is called by main function when proper arguments are passed
    PRINT_INSTR()
    input_flag = input()
    
    if input_flag in flag_dict: # this takes an input and checks it to the flag dictionary
        flag_dict[input_flag]() # if the flag is in the flag dictionary its associated function is called
    else: 
        print("Invalid flag entered, please try again.")
        init() # recursive call on bad input

if __name__ == "__main__": # main function; calls init() when provided with a file as a proper argument
    if (len(sys.argv)) < 2:
        print("Example Usage: python3 fsteg.py file")
    else:
        global fpath #global var for the image path fsteg is running on
        fpath = sys.argv[1] #!! Add code here to verify that the image path is a valid filepath
        CALL_LOGO()
        init()