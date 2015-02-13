#!/usr/bin/python
import sys
import re
import numpy as np

# high-level implementation of Brainfuck interpreter
# inspired by http://forum.openframeworks.cc/t/bodyfuck-a-gestural-brainfuck-interpreter/2772/2
# http://en.wikipedia.org/wiki/Brainfuck
# Used unichr function. Assumes that values are in range of ordinal i; 0 <= i <= 0x10ffff
# otherwise you'll get junk.


class Brainfuck:
    def __init__(self):
        self.ARRAY_SIZE = 30000  # in bytes
        self.ptr = 0
        self.instr_ptr = 0
        self.memory = np.zeros(self.ARRAY_SIZE)
        self.instructions = []


    def decr_ptr(self):
        if self.ptr - 1 < 0:
            print "{0} not in range of memory".format(self.ptr - 1)
        else:
            self.ptr -= 1
        self.instr_ptr += 1

    def incr_ptr(self):
        if self.ptr + 1 > self.ARRAY_SIZE - 1:
            print "{0} not in range of memory".format(self.ptr + 1)
        else:
            self.ptr += 1
        self.instr_ptr += 1

    def decr_val(self):
        if self.memory[self.ptr] == 0:
            print "contents at min value 0"
        else:
            self.memory[self.ptr] -= 1
        self.instr_ptr += 1

    def incr_val(self):
        if self.memory[self.ptr] == 127:
            print "contents at max value 127"
        else:
            self.memory[self.ptr] += 1
        self.instr_ptr += 1

    def get_val(self):
        sys.stdout.write(str(unichr(int(self.memory[self.ptr]))))
        self.instr_ptr += 1

    def set_val(self):
        val = raw_input("put char > ")
        while len(val) != 1:
            print "input should be a single character"
            val = raw_input("put char > ")
        self.memory[self.ptr] = ord(val)
        self.instr_ptr += 1

    def lparen(self):
        if self.memory[self.ptr] == 0:
            # jump to matching rparen
            parens = 1
            while parens != 0:
                self.instr_ptr += 1
                if self.instructions[self.instr_ptr] == '[':
                    parens += 1
                elif self.instructions[self.instr_ptr] == ']':
                    parens -= 1
        else:
            # move to next cmd
            self.instr_ptr += 1

    def rparen(self):
        if self.memory[self.ptr]:
            # jump to command after matching lparen
            parens = 1
            while parens != 0:
                self.instr_ptr -= 1
                if self.instructions[self.instr_ptr] ==']':
                    parens += 1
                if self.instructions[self.instr_ptr] == '[':
                    parens -= 1
        else:
            # move to next cmd
            self.instr_ptr += 1

    def read(self, inp):
        tokens = []
        for i in xrange(len(inp)):
            c = inp[i]
            if c in '<>+-[].,':
                tokens.append(c)
        self.instructions += tokens
        return tokens

    def eval(self):
        cmds = {'<': self.decr_ptr,
                '>': self.incr_ptr,
                '-': self.decr_val,
                '+': self.incr_val,
                '.': self.get_val,
                ',': self.set_val,
                '[': self.lparen,
                ']': self.rparen
        }
        while self.instr_ptr != len(self.instructions):
            try:
                cmds[self.instructions[self.instr_ptr]]()
            except Exception as e:
                print e


    def loop(self):
        if len(sys.argv) > 1:  # feed it a program
            filename = sys.argv[1]
            try:
                f = open(filename, 'rb')
                program = ''.join(f.readlines())
                f.close()
                self.read(program)
                self.eval()
            except Exception as e:
                print e
                print "Problem with opening file {0}".format(filename)
        else:  # interactive mode
            print "Brainfuck Interpreter http://en.wikipedia.org/wiki/Brainfuck"
            print "accepted characters are + - < > . , [ ]"
            print "input EXIT to quit, and DEBUG to cheat"
            while True:
                inp = raw_input("bfk: ")
                if inp == "EXIT":
                    print "goodbye"
                    sys.exit()
                elif inp == "DEBUG":
                    print "ptr: ", self.ptr
                    print "instr_ptr: ", self.instr_ptr
                    print "num instructions: ", len(self.instructions)
                    print "val: ", self.get_val()
                    print "raw val: ", self.memory[self.instr_ptr]
                else:
                    self.read(inp)
                    self.eval()


if __name__ == "__main__":
    interpreter = Brainfuck()
    interpreter.loop()
