import binascii
from chip8 import Chip8


def main():
    ROM_NAME = "PONG"
    try:
        with open(ROM_NAME, mode="rb") as file:
            rom = binascii.hexlify(file.read())
    except:
        print("ERROR: rom file not found")
        return
    chip8 = Chip8()
    chip8.load_rom(rom)

    chip8.emulateCycle()
    # if chip8.get_draw_flag() == True:
    #   display.update_graphics()
    # chip8.set_keys()

if __name__ == '__main__':
    main()
