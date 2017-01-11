import sys
import binascii
from display import Display


def main(argv):
    ROM_PATH = "P:\Development\Python\c8emu\c8emu\\roms\\" + argv
    try:
        with open(ROM_PATH, mode="rb") as file:
            rom = binascii.hexlify(file.read())
    except:
        print("ERROR: rom file not found")
        return

    display = Display(rom)
    display.start()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: python main.py <rom_name>")
    else:
        main(sys.argv[1])
