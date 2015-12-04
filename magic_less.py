#!/usr/bin/python3

import fileinput
import termbox
import time
import math
import re

def getNumWindows(lines, height):
    return max(math.ceil(len(lines) / height), 1)
def getWindowToPutLineInto(index, height):
    return int(index / height)
def getLinesToDisplay(lines, height, startingIndex):
    return min(len(lines) - startingIndex, height)

if __name__ == '__main__':
    lines = []

    for line in fileinput.input():
        lines.append(line)

    t = termbox.Termbox()

    height = t.height()

    numWindows = getNumWindows(lines, height)

    windowIndex = 0

    windows = [[] for i in range(numWindows)]

    width = t.width()

    for i in range(len(lines)):
        windows[getWindowToPutLineInto(i, height)].append(lines[i])

    items = []

    while True:
        t.clear()
        startingIndex = windowIndex * height
        window = windows[windowIndex]
        items.append(window[0])
        for y in range(len(window)):
            for x in range(min(len(window[y][:-1] if window[y][-1] == '\n' else window[y]), width)):
                t.change_cell(x, y, ord(window[y][x]), termbox.DEFAULT, termbox.DEFAULT)
        t.present()
        char = t.poll_event()
        if char[1] == 'q':
            break
        elif char[1] == 'j':
            windowIndex = (windowIndex + 1) % numWindows
        elif char[1] == 'k':
            windowIndex = (windowIndex - 1) % numWindows

    t.close()
