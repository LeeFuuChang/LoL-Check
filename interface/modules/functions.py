from .constants import *
import os


def indexOf(string, target, idx=0):
    try:
        return string.index(target, idx)
    except ValueError:
        return -1


def getLastEdit(path):
    try:
        return os.path.getmtime(path)
    except:
        return 0


def listdir(path):
    try:
        return sorted(
            [os.path.join(path, d) for d in os.listdir(path)],
            key = getLastEdit, reverse = True
        )
    except:
        return []


def FindLoLPath():
    for i in range(26):
        rootChr = chr(65+i)
        print(rootChr)
        if not os.path.exists(f"{rootChr}:\\"): continue

        now = []
        nxt = []
        for child in listdir(f"{rootChr}:\\"):
            if os.path.isdir(child):
                now.append(child)

        while(len(now) != 0):
            for path in now:
                if (LOL_PATH_TARGET1 in path) or (LOL_PATH_TARGET2 in path):
                    return path

                for child in listdir(path):
                    if os.path.isdir(child):
                        nxt.append(child)

            now = nxt
            nxt = []
    return ""
