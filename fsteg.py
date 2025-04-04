import sys
def init():
    print("Program initialized!")

if __name__ == "__main__":
    if (len(sys.argv)) < 2:
        print("Example Usage: python3 fsteg.py file")
    else:
        init()