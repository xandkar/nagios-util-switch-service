#!/usr/bin/env python

import re
import sys


class State():
    def __init__(self):
        self.in_block = False
        self.block_name = ''
        self.block_lines = []


class Block():
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines


def get_blocks(cfg_file_lines):
    pattern_block_begin = re.compile(r'^define\ service[\ |\{]')
    pattern_block_end   = re.compile(r'^\}')

    # Collection
    blocks = []

    # State
    line_number = 0
    state = State()

    for line in cfg_file_lines:
        line_number += 1
        line = line.strip()

        #----------------------------------------------------------------------
        # Exit block
        #----------------------------------------------------------------------
        if re.match(pattern_block_end, line):
            # Collect line number
            state.block_lines.append(line_number)

            # Save data
            if state.in_block:
                block = Block(state.block_name, state.block_lines)
                blocks.append(block)

            # Reset state
            state = State()

        #----------------------------------------------------------------------
        # In block
        #----------------------------------------------------------------------
        if state.in_block:
            # Collect line number
            state.block_lines.append(line_number)

            # Collect data
            key, value = line.split()[:2]

            if key == 'use':
                state.block_name = value

        #----------------------------------------------------------------------
        # Enter block
        #----------------------------------------------------------------------
        if re.match(pattern_block_begin, line):
            # Collect line number
            state.block_lines.append(line_number)

            # Set state
            state.in_block = True

    return blocks


def main():
    file_path = sys.argv[1]
    cfg_file_lines = open(file_path).readlines()
    blocks = get_blocks(cfg_file_lines)

    for block in blocks:
        print block.name
        print block.lines
        print


if __name__ == '__main__':
    main()
