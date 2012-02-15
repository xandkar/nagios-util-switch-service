#!/usr/bin/env python


import re
import os
import sys
import shutil


class State():
    def __init__(self):
        self.in_block = False
        self.block_name = ''
        self.block_lines = []


class Block():
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines


def get_service_blocks(file_lines):
    pattern_block_begin = re.compile(r'^define\ service[\ |\{]')
    pattern_block_end   = re.compile(r'^\}')

    # Collection
    blocks = []

    # State
    line_number = 0
    state = State()

    for line in file_lines:
        line_number += 1
        line = line.strip()

        #
        # Exit block
        #
        if re.match(pattern_block_end, line):
            # Collect line number
            state.block_lines.append(line_number)

            # Save data
            if state.in_block:
                block = Block(state.block_name, state.block_lines)
                blocks.append(block)

            # Reset state
            state = State()

        #
        # In block
        #
        if state.in_block:
            # Collect line number
            state.block_lines.append(line_number)

            # Collect data
            key, value = line.split()[:2]

            if key == 'use':
                state.block_name = value

        #
        # Enter block
        #
        if re.match(pattern_block_begin, line):
            # Collect line number
            state.block_lines.append(line_number)

            # Set state
            state.in_block = True

    return blocks


def main():
    # Parse arguments
    target_dir_path, target_service, desired_state = sys.argv[1:4]

    # Filter directory contents
    target_dir_contents = os.listdir(target_dir_path)
    target_file_names = [f for f in target_dir_contents if f.endswith('.cfg')]

    # Main loop
    for file_name in target_file_names:
        file_path = os.path.join(target_dir_path, file_name)

        if not desired_state in ['on', 'off']:
            sys.exit('INVALID STATE')

        # Read original file, striping trailing whitespace
        original_file_lines = [l.rstrip() for l in open(file_path).readlines()]

        # Parse into service blocks
        service_blocks = get_service_blocks(original_file_lines)

        # Initialize new file content
        new_file_lines = original_file_lines

        # Modify appropriate lines
        for block in service_blocks:
            if block.name == target_service:
                for line_number in block.lines:
                    index = line_number - 1  # Correct for 0-indexed list

                    if desired_state == 'off' \
                    and not original_file_lines[index].startswith('#'):
                        new_file_lines[index] = \
                            '#%s' % original_file_lines[index]
                    elif desired_state == 'on':
                        new_file_lines[index] = \
                            original_file_lines[index].replace('#', '')

        # Backup original file
        shutil.copy2(file_path, '%s.bak' % file_path)

        # Write new lines to original file
        try:
            new_file = open(file_path, 'wb')
            new_file.writelines('\n'.join(new_file_lines))
        finally:
            new_file.close()


if __name__ == '__main__':
    main()
