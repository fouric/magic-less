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
def tabConvert(line):
    result = ''
    screenIndex = 0
    for charIndex in range(len(line)):
        if line[charIndex] == '\t':
            result += ' ' * (8 - screenIndex % 8)
            screenIndex += 8 - screenIndex % 8
        else:
            result += line[charIndex]
            screenIndex += 1
    return result
def drawText(t, x, y, text, fg = termbox.DEFAULT, bg = termbox.DEFAULT):
    for i in range(len(text)):
        t.change_cell(x + i, y, ord(text[i]), fg, bg)

if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line if line[-1] != '\n' else line[:-1])

    t = termbox.Termbox()

    height = t.height()
    width = t.width()

    numWindows = getNumWindows(lines, height)
    waningWindowIndex = 0
    windows = [[] for i in range(numWindows)]
    for i in range(len(lines)):
        windows[getWindowToPutLineInto(i, height)].append(tabConvert(lines[i]))

    barrierIndex = -1

    while True:
        t.clear()
        waning = windows[waningWindowIndex]
        waxing = windows[(waningWindowIndex + 1) % numWindows]

        # aligned perfectly on a page
        if barrierIndex == -1:
            for y in range(len(waning)):
                drawText(t, 0, y, waning[y])
        else:
            for y in range(barrierIndex):
                drawText(t, 0, y, waxing[y])
            drawText(t, 0, barrierIndex, '-' * width)
            for y in range(min(height - barrierIndex - 1, len(waning))):
                drawText(t, 0, y + barrierIndex + 1, waning[min(y + barrierIndex + 1, len(waning) - 1)])
        t.present()
        char = t.poll_event()
        if char[1] == 'q':
            break
        elif char[1] == 'j':
            barrierIndex += 1
            if barrierIndex >= height:
                if waningWindowIndex + 1 < numWindows:
                    barrierIndex = -1
                    waningWindowIndex += 1
                else:
                    barrierIndex = height - 1
            elif waningWindowIndex == numWindows - 2 and barrierIndex >= (len(waxing) - 1):
                barrierIndex = len(waxing) - 1
        elif char[1] == 'k':
            barrierIndex -= 1
            if barrierIndex < -1:
                if waningWindowIndex > 0:
                    barrierIndex = height - 1
                    waningWindowIndex -= 1
                else:
                    barrierIndex = -1

    t.close()
