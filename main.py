import binascii
from display import Display


def main():
    ROM_NAME = "P:\Development\Python\c8emu\c8emu\\roms\PONG"
    try:
        with open(ROM_NAME, mode="rb") as file:
            rom = binascii.hexlify(file.read())
    except:
        print("ERROR: rom file not found")
        return

    display = Display(rom)
    display.start()

    # if chip8.get_draw_flag() == True:
    #   display.update_graphics()
    # chip8.set_keys()

if __name__ == '__main__':
    main()
