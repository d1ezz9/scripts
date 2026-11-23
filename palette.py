#!/usr/bin/env python3
import sys
import time
import shutil
import signal

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J\033[H"
CLEAR_TO_EOL = "\033[K"
RESET = "\033[0m"
BG_TERMINAL_DEFAULT = "\033[49m"

COLORS = [
    "\033[41m", "\033[42m", "\033[43m", "\033[44m",
    "\033[45m", "\033[46m", "\033[47m"
]

def draw_palette(signum=None, frame=None):
    sys.stdout.write("\033[H" + HIDE_CURSOR)
    cols, rows = shutil.get_terminal_size()
    patch_w = 6
    patch_h = 7
    gap = 2
    step_size = 2
    num_patches = len(COLORS)
    total_w = (num_patches * patch_w) + ((num_patches - 1) * gap)
    start_x = max(0, (cols - total_w) // 2)
    start_y = max(0, (rows - patch_h) // 2)
    output = []
    for y in range(rows - 1):
        if start_y <= y < start_y + patch_h:
            curr_row_in_patch = y - start_y
            line = BG_TERMINAL_DEFAULT + " " * start_x
            for i in range(num_patches):
                color_code = COLORS[i]
                if curr_row_in_patch == 0:
                    line += color_code + " " * (patch_w - step_size) + BG_TERMINAL_DEFAULT + " " * step_size
                elif curr_row_in_patch == patch_h - 1:
                    line += BG_TERMINAL_DEFAULT + " " * step_size + color_code + " " * (patch_w - step_size)
                else:
                    line += color_code + " " * patch_w
                if i < num_patches - 1:
                    line += BG_TERMINAL_DEFAULT + " " * gap
            line += RESET + CLEAR_TO_EOL
        else:
            line = RESET + CLEAR_TO_EOL
        output.append(line + "\n")
    output.append(RESET + CLEAR_TO_EOL)
    sys.stdout.write("".join(output))
    sys.stdout.flush()

def graceful_exit(signum, frame):
    sys.stdout.write(RESET + SHOW_CURSOR + CLEAR_SCREEN)
    sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, graceful_exit)
    if hasattr(signal, 'SIGWINCH'):
        signal.signal(signal.SIGWINCH, draw_palette)
    sys.stdout.write(CLEAR_SCREEN)
    draw_palette()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            graceful_exit(None, None)
