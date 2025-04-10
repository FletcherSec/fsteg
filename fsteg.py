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

def check_output_name(): #this function is responsible for making sure output filenames dont overlap
    default = "extracted_file"
    newfilename = default
    # Here an extension could read from the file fsteg could be read and appended to the output file.  I'll do this eventually.
    count = 1

    while os.path.exists(newfilename): #this increments a count number to the end of the filename until the filename doesn't already exist in the directory.
        newfilename = f"{default}_{count}"
        count += 1
    return newfilename

def PRINT_INSTR(): # responsible for formatting the instructions
    instr = r"""
  To continue, please enter a flag to be run on the file. (Enter the flag letter without the '-')

  -S : Uses steghide to check files (JPEG, BMP, WAV, and AU) for data hidden with Steghide.
  -Sp [password] : Uses steghide to check for hidden data with a password.
  -Sb : Bruteforces steghide password with a wordlist. (To be implemented)
  -Z : Uses zsteg to check files for data hidden with LSB steganography. (To be implemented)
  -A : Runs all tools in succession on specified file. (To be implemented)
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
    outfilename = check_output_name()
    build_cmd = [ # this builds out the steghide command to perform the extraction
        spath,
        "extract",
        "-sf", fpath,
        "-p", passw,
        "-xf", outfilename
    ]

    try: # runs command with subprocess
        result = subprocess.run(build_cmd, capture_output=True, text=True, check=True)
        print("\nSteghide Output: File Extracted Successfully, Printing Contents Below!")
        try:
            subprocess.run(["cat", outfilename]) # this line can be commented out if you dont want the contents of the file being printed in the program upon extraction.
        except subprocess.CalledProcessError as e: # this try except is to handle errors from windows (no cat command), since windows support isnt implemented yet.
            print("\nError:", e.stderr)
    except subprocess.CalledProcessError as e:
        print("\nError:", e.stderr)

def Sfunction(): # gathers steghide filepath and then calls the stegextract function with no pass.
    relpath = get_steg_path()
    nopass = ""
    steg_extract(relpath, nopass)

def Spfunction():
    relpath = get_steg_path()
    print("Enter Passkey:")
    entered_pass = input() # specifies the passkey for steghide
    steg_extract(relpath, entered_pass)

def Sbfunction():
    print("Write Me!")

def Afunction():
    print("Write Me!")

def Zfunction():
    print("Write Me!")

flag_dict = { # This is where the acceptable flags and their associated functions are stored in a dictionary
    "S" : Sfunction,
    "Sp" : Spfunction,
    "Sb" : Sbfunction,
    "Z" : Zfunction,
    "A" : Afunction,
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