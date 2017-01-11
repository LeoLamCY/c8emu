import random


class Chip8(object):
    ERROR_UNKNOWN_OPCODE = "ERROR: unknown opcode"
    running = False
    count = 0

    font_set = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,
        0x20, 0x60, 0x20, 0x20, 0x70,
        0xF0, 0x10, 0xF0, 0x80, 0xF0,
        0xF0, 0x10, 0xF0, 0x10, 0xF0,
        0x90, 0x90, 0xF0, 0x10, 0x10,
        0xF0, 0x80, 0xF0, 0x10, 0xF0,
        0xF0, 0x80, 0xF0, 0x90, 0xF0,
        0xF0, 0x10, 0x20, 0x40, 0x40,
        0xF0, 0x90, 0xF0, 0x90, 0xF0,
        0xF0, 0x90, 0xF0, 0x10, 0xF0,
        0xF0, 0x90, 0xF0, 0x90, 0x90,
        0xE0, 0x90, 0xE0, 0x90, 0xE0,
        0xF0, 0x80, 0x80, 0x80, 0xF0,
        0xE0, 0x90, 0x90, 0x90, 0xE0,
        0xF0, 0x80, 0xF0, 0x80, 0xF0,
        0xF0, 0x80, 0xF0, 0x80, 0x80
    ]

    def __init__(self, display):
        self.reset()
        self.display = display

    def reset(self):
        self.pc = 0x200
        self.v = 16 * [0]
        self.i = 0
        self.memory = 0x1000 * [0]
        self.delay_timer = None
        self.sound_timer = None
        self.stack = 16 * [0]
        self.sp = 0
        self.keys = 16 * [0]

        for i, font in enumerate(self.font_set):
            self.memory[i] = hex(font)[2:]

    def load_rom(self, rom):
        k = 0
        for i in range(0, len(rom), 2):
            self.memory[k + 0x200] = rom[i:i + 2]
            k += 1

    def emulateCycle(self):
        self.running = True
        self.read_execute_instruction(
            self.memory[self.pc] + self.memory[self.pc + 1])

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            # make sound
            self.display.playSound()
            self.sound_timer = 0

    def read_execute_instruction(self, instruction):
        def bit_and(instruction, and_target):
            return int(instruction, 16) & and_target

        inst = format(int(instruction, 16) & 0xf000, "#06x")
        x = bit_and(instruction, 0x0f00) >> 8
        y = bit_and(instruction, 0x00f0) >> 4
        n = bit_and(instruction, 0x000f)
        nn = bit_and(instruction, 0x00ff)
        nnn = bit_and(instruction, 0x0fff)

        if inst == "0x0000":
            nn = format(nn, "#06x")
            if nn == "0x00e0":
                # clear disp
                self.display.clear_screen()
                self.pc += 2
            elif nn == "0x00ee":
                # return from subroutine
                self.sp -= 1
                self.pc = self.stack[self.sp]
            else:
                self.running = False

        elif inst == "0x1000":
            # goto addr NNN
            self.pc = nnn

        elif inst == "0x2000":
            # calls subroutine at nnn
            self.stack[self.sp] = self.pc + 2
            self.sp += 1
            self.pc = nnn

        elif inst == "0x3000":
            # Skips the next instruction if VX equals NN. (Usually the next
            # instruction is a jump to skip a code block)
            if self.v[x] == nn:
                self.pc += 4
            else:
                self.pc += 2

        elif inst == "0x4000":
            # Skips the next instruction if VX doesn't equal NN. (Usually the
            # next instruction is a jump to skip a code block)
            if self.v[x] != nn:
                self.pc += 4
            else:
                self.pc += 2

        elif inst == "0x5000":
            # Skips the next instruction if VX equals VY. (Usually the next
            # instruction is a jump to skip a code block)
            if bit_and(instruction, 0x000f) != "0x0000":
                raise Exception(self.ERROR_UNKNOWN_OPCODE + " " + instruction)
            if self.v[x] == self.v[y]:
                self.pc += 4
            else:
                self.pc += 2

        elif inst == "0x6000":
            # Sets VX to NN.
            self.v[x] = nn
            self.pc += 2

        elif inst == "0x7000":
            # Adds NN to VX.
            self.v[x] += nn
            if self.v[x] > 255:
                self.v[x] -= 256
            self.pc += 2

        elif inst == "0x8000":
            n = format(n, "#06x")
            if n == "0x0000":
                # Sets VX to the value of VY.
                self.v[x] = self.v[y]

            elif n == "0x0001":
                # Sets VX to VX or VY. (Bitwise OR operation)
                self.v[x] = self.v[x] | self.v[y]

            elif n == "0x0002":
                # Sets VX to VX and VY. (Bitwise AND operation)
                self.v[x] = self.v[x] & self.v[y]

            elif n == "0x0003":
                # Sets VX to VX xor VY.
                self.v[x] = self.v[x] ^ self.v[y]

            elif n == "0x0004":
                # Adds VY to VX. VF is set to 1 when there's a carry, and to 0
                # when there isn't.
                self.v[x] += self.v[y]
                if self.v[x] > 255:
                    self.v[0xF] = 1
                    self.v[x] -= 256
                else:
                    self.v[0xF] = 0

            elif n == "0x0005":
                # VY is subtracted from VX. VF is set to 0 when there's a
                # borrow, and 1 when there isn't.
                self.v[x] -= self.v[y]
                if self.v[x] < 0:
                    self.v[0xF] = 0
                    self.v[x] += 256
                else:
                    self.v[0xF] = 1

            elif n == "0x0006":
                # Shifts VX right by one. VF is set to the value of the least
                # significant bit of VX before the shift.
                self.v[0xF] = int(bin(self.v[x][-1]))
                self.v[x] = self.v[x] >> 1

            elif n == "0x0007":
                # Sets VX to VY minus VX. VF is set to 0 when there's a borrow,
                # and 1 when there isn't.
                self.v[x] = self.v[y] - self.v[x]
                if self.v[x] < 0:
                    self.v[0xF] = 0
                    self.v[x] += 256
                else:
                    self.v[0xF] = 1

            elif n == "0x000e":
                # Shifts VX left by one. VF is set to the value of the most
                # significant bit of VX before the shift.
                self.v[0xF] = int(bin(self.v[x][0]))
                self.v[x] = self.v[x] << 1

            else:
                raise Exception(self.ERROR_UNKNOWN_OPCODE)
            self.pc += 2

        elif inst == "0x9000":
            n = format(n, "#06x")
            if n != "0x0000":
                raise Exception(self.ERROR_UNKNOWN_OPCODE)
            # Skips the next instruction if VX doesn't equal VY. (Usually the
            # next instruction is a jump to skip a code block)
            if self.v[x] != self.v[y]:
                self.pc += 4
            else:
                self.pc += 2

        elif inst == "0xa000":
            # Sets I to the address NNN.
            self.i = nnn
            self.pc += 2

        elif inst == "0xb000":
            # Jumps to the address NNN plus V0.
            addr = self.v[0] + nnn
            self.stack[self.sp] = self.pc
            self.sp += 1
            self.pc = addr

        elif inst == "0xc000":
            # Sets VX to the result of a bitwise and operation on a random
            # number (Typically: 0 to 255) and NN.
            self.v[x] = nn & random.randint(0, 255)
            self.pc += 2

        elif inst == "0xd000":
            # Draws a sprite at coordinate (VX, VY) that has a width of 8
            # pixels and a height of N pixels.
            sprite = []
            for i in range(n):
                sprite.append(int(self.memory[self.i + i], 16))
            self.v[0xf] = self.display.draw_sprite(
                self.v[x], self.v[y], sprite)
            self.pc += 2

        elif inst == "0xe000":
            nn = format(nn, "#06x")
            if nn == "0x009e":
                # Skips the next instruction if the key stored in VX is pressed.
                # (Usually the next instruction is a jump to skip a code block)
                if self.display.isKeyPressed(self.v[x]):
                    self.pc += 4
                else:
                    self.pc += 2

            elif nn == "0x00a1":
                # Skips the next instruction if the key stored in VX isn't pressed.
                # (Usually the next instruction is a jump to skip a code block)
                if not self.display.isKeyPressed(self.v[x]):
                    self.pc += 4
                else:
                    self.pc += 2

            else:
                raise Exception(self.ERROR_UNKNOWN_OPCODE)

        elif inst == "0xf000":
            nn = format(nn, "#06x")
            if nn == "0x0007":
                # Sets VX to the value of the delay timer.
                self.v[x] = self.delay_timer

            elif nn == "0x000a":
                # A key press is awaited, and then stored in VX. (Blocking
                # Operation. All instruction halted until next key event)
                self.display.pause()

            elif nn == "0x0015":
                # Sets the delay timer to VX.
                self.delay_timer = self.v[x]

            elif nn == "0x0018":
                # Sets the sound timer to VX.
                self.sound_timer = self.v[x]

            elif nn == "0x001e":
                # Adds VX to I.
                self.i += self.v[x]

            elif nn == "0x0029":
                # Sets I to the location of the sprite for the character in VX.
                # Characters 0-F (in hexadecimal) are represented by a 4x5
                # font.
                self.i = self.v[x] * 5

            elif nn == "0x0033":
                # Stores the binary-coded decimal representation of VX, with
                # the most significant of three digits at the address in I, the
                # middle digit at I plus 1, and the least significant digit at
                # I plus 2.
                vx = self.v[x]
                for i in range(2, 0, -1):
                    digit = vx % 10
                    self.memory[self.i + i] = digit
                    vx /= 10

            elif nn == "0x0055":
                # Stores V0 to VX (including VX) in memory starting at address
                # I.
                for i in range(0, x + 1):
                    self.memory[self.i + i] = self.v[i]

            elif nn == "0x0065":
                # Fills V0 to VX (including VX) with values from memory
                # starting at address I.
                # TODO normalize memory format
                for i in range(0, x + 1):
                    try:
                        self.v[i] = int(self.memory[self.i + i], 16)
                    except:
                        self.v[i] = self.memory[self.i + i]

            self.pc += 2
        else:
            raise Exception(self.ERROR_UNKNOWN_OPCODE + " " + instruction)
