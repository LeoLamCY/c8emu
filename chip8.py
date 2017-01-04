class Chip8(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.pc = 0x200
        self.v = 16 * [0x00]
        self.i = 0x0000
        self.memory = 512 * [0x00]
        self.delay_timer = None
        self.sound_timer = None
        self.stack = 16 * [0x0000]
        self.sp = 0
        self.keys = 16 * [0x00]

    def load_rom(self, rom):
        for i in range(0, len(rom), 2):
            self.memory.append(rom[i:i + 2])

    def emulateCycle(self):
        print(
            "reading:" + hex(int(self.memory[self.pc] + self.memory[self.pc + 1], 16)))
        self.read_execute_instruction(
            self.memory[self.pc] + self.memory[self.pc + 1])

    def read_execute_instruction(self, instruction):
        def bit_and(self, instruction, and_target):
            return format((int(instruction, 16) & and_target), 'x')

        inst = hex(int(instruction, 16) & 0xf000)
        print(inst)
        if inst == "0x0":
            if inst == "0x00E0":
                # clear disp
                pass
            elif inst == "0x00EE":
                # return from subroutine
                pass
        elif inst == "0x1":
            # goto addr NNN
            nnn = bit_and(0x0fff)
            pass
        elif inst == "0x2":
            # calls subroutine at NNN
            nnn = bit_and(0x0fff)
            pass
        elif inst == "0x3":
            # Skips the next instruction if VX equals NN. (Usually the next
            # instruction is a jump to skip a code block)
            x = bit_and(0x0f00)
            nn = bit_and(0x00ff)
            pass
        elif inst == "0x4":
            # Skips the next instruction if VX doesn't equal NN. (Usually the
            # next instruction is a jump to skip a code block)
            x = bit_and(0x0f00)
            nn = bit_and(0x00ff)
            pass
        elif inst == "0x5":
            # Skips the next instruction if VX equals VY. (Usually the next
            # instruction is a jump to skip a code block)
            if bit_and(0x000f) != "0":
                raise Exception("unknown opcode")
            x = bit_and(0x0f00)
            y = bit_and(0x00f0)
            pass
        elif inst == "0x6":
            # Sets VX to NN.
            x = bit_and(0x0f00)
            nn = bit_and(0x00ff)
            print(inst)
            pass
        elif inst == "0x7":
            # Adds NN to VX.
            x = bit_and(0x0f00)
            nn = bit_and(0x00ff)
            pass
        elif inst == "0x8":
            last_nibble = bit_and(0x000f)
            x = bit_and(0x0f00)
            y = bit_and(0x00f0)
            if last_nibble == "0":
                # Sets VX to the value of VY.
                pass
            elif last_nibble == "1":
                # Sets VX to VX or VY. (Bitwise OR operation)
                pass
            elif last_nibble == "2":
                # Sets VX to VX and VY. (Bitwise AND operation)
                pass
            elif last_nibble == "3":
                # Sets VX to VX xor VY.
                pass
            elif last_nibble == "4":
                # Adds VY to VX. VF is set to 1 when there's a carry, and to 0
                # when there isn't.
                pass
            elif last_nibble == "5":
                # VY is subtracted from VX. VF is set to 0 when there's a
                # borrow, and 1 when there isn't.
                pass
            elif last_nibble == "6":
                # Shifts VX right by one. VF is set to the value of the least
                # significant bit of VX before the shift.
                pass
            elif last_nibble == "7":
                # Sets VX to VY minus VX. VF is set to 0 when there's a borrow,
                # and 1 when there isn't.
                pass
            elif last_nibble == "E":
                # Shifts VX left by one. VF is set to the value of the most
                # significant bit of VX before the shift.
                pass
            else:
                raise Exception("unknown opcode")
        elif inst == "0x9":
            if bit_and(0x000f) != "0":
                raise Exception("unknown opcode")
            # Skips the next instruction if VX doesn't equal VY. (Usually the
            # next instruction is a jump to skip a code block)
            x = bit_and(0x0f00)
            y = bit_and(0x00f0)
            pass
        elif inst == "0xA":
            # Sets I to the address NNN.
            nnn = bit_and(0x0fff)
            pass
        elif inst == "0xB":
            # Jumps to the address NNN plus V0.
            nnn = bit_and(0x0fff)
            pass
        elif inst == "0xC":
            # Sets VX to the result of a bitwise and operation on a random
            # number (Typically: 0 to 255) and NN.
            x = bit_and(0x0f00)
            nn = bit_and(0x00ff)
            pass
        elif inst == "0xD":
            # Draws a sprite at coordinate (VX, VY) that has a width of 8
            # pixels and a height of N pixels.
            x = bit_and(0x0f00)
            y = bit_and(0x00f0)
            n = bit_and(0x000f)
        elif inst == "0xE":
            x = bit_and(0x0f00)
            # Skips the next instruction if the key stored in VX is pressed.
            # (Usually the next instruction is a jump to skip a code block)
            if bit_and(0x00ff) == "9E":
                pass

            # Skips the next instruction if the key stored in VX isn't pressed.
            # (Usually the next instruction is a jump to skip a code block)
            elif bit_and(0x00ff) == "A1":
                pass
            else:
                raise Exception("unknown opcode")
        elif inst == "0xF":
            last_two_nibbles = bit_and(0x00ff)
            x = bit_and(0x0f00)
            if last_two_nibbles == "07":
                # Sets VX to the value of the delay timer.
                pass

            elif last_two_nibbles == "0A":
                # A key press is awaited, and then stored in VX. (Blocking
                # Operation. All instruction halted until next key event)
                pass

            elif last_two_nibbles == "15":
                # Sets the delay timer to VX.
                pass

            elif last_two_nibbles == "18":
                # Sets the sound timer to VX.
                pass

            elif last_two_nibbles == "1E":
                # Adds VX to I.
                pass

            elif last_two_nibbles == "29":
                # Sets I to the location of the sprite for the character in VX.
                # Characters 0-F (in hexadecimal) are represented by a 4x5
                # font.
                pass

            elif last_two_nibbles == "33":
                # Stores the binary-coded decimal representation of VX, with
                # the most significant of three digits at the address in I, the
                # middle digit at I plus 1, and the least significant digit at
                # I plus 2.
                pass

            elif last_two_nibbles == "55":
                # Stores V0 to VX (including VX) in memory starting at address
                # I.
                pass

            elif last_two_nibbles == "65":
                # Fills V0 to VX (including VX) with values from memory
                # starting at address I.
                pass
