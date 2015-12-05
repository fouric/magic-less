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
    windowIndex = 0
    windows = [[] for i in range(numWindows)]
    for i in range(len(lines)):
        windows[getWindowToPutLineInto(i, height)].append(tabConvert(lines[i]))

    barrierIndex = 0

    while True:
        t.clear()
        startingIndex = windowIndex * height
        upper = windows[windowIndex]
        lower = windows[windowIndex + 1 % numWindows]
        for y in range(barrierIndex):
            drawText(t, 0, y, lower[y])
        drawText(t, 0, barrierIndex, '-' * width)
        for y in range(height - barrierIndex - 1):
            drawText(t, 0, y + barrierIndex + 1, upper[y + barrierIndex + 1])
        t.present()
        char = t.poll_event()
        if char[1] == 'q':
            break
        elif char[1] == 'j':
            #windowIndex = (windowIndex + 1) % numWindows
            barrierIndex += 1
            if barrierIndex >= height:
                windowIndex = windowIndex + 1 % numWindows
                barrierIndex = 0
        elif char[1] == 'k':
            #windowIndex = (windowIndex - 1) % numWindows
            barrierIndex -= 1
            if barrierIndex < 0:
                windowIndex = windowIndex - 1 % numWindows
                barrierIndex = height - 1

    t.close()
