from enum import Enum
from typing import Generator

# unDumped = [{'TIMESTEP':int, 'NUMBER OF ATOMS':int, 'BOX BOUNDS':dict, 'ATOMS':[dict specific to dump style]}]


class Modes(Enum):
    TIME = 1
    NUM = 2
    BOUNDS = 3
    ATOM = 4


def read_dump(file: str) -> Generator[dict[str:any], None, None]:
    """Generator object that yields one frame of the file at a time"""

    unDumped = {}
    loopCount = 0

    with open(file, "r") as myfile:
        for line in myfile:
            loopCount += 1
            if "TIMESTEP" in line:
                loopCount = 0
                mode = Modes.TIME
                checkLoop = loopCount
                if unDumped:
                    yield unDumped
                unDumped = {"ATOMS": []}
            if mode == Modes.TIME and (loopCount - checkLoop) == 1:
                unDumped["TIMESTEP"] = int(line)
            if "NUMBER OF ATOMS" in line:
                mode = Modes.NUM
                checkLoop = loopCount
            if mode == Modes.NUM and (loopCount - checkLoop) == 1:
                unDumped["NUMBER OF ATOMS"] = int(line)
            if "BOX BOUNDS" in line:
                mode = Modes.BOUNDS
                checkLoop = loopCount
                unDumped["BOX BOUNDS"] = {"x": [], "y": [], "z": []}
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 1:
                unDumped["BOX BOUNDS"]["x"] = line.split()
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 2:
                unDumped["BOX BOUNDS"]["y"] = line.split()
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 3:
                unDumped["BOX BOUNDS"]["z"] = line.split()
            if "ITEM: ATOMS" in line:
                mode = Modes.ATOM
                checkLoop = loopCount
                v_line = line.split()
            if mode == Modes.ATOM and (loopCount - checkLoop) >= 1:
                s_line = line.split()
                paraCount = 0
                atomDict = {}
                for para in v_line:
                    if para != "ATOMS" and para != "ITEM:":
                        atomDict[para] = s_line[paraCount]
                        paraCount += 1
                unDumped["ATOMS"].append(atomDict)


def read_whole_dump(file: str) -> list[dict[str:any]]:
    """read the entire file into an unDumped data structure"""
    return list(read_dump(file))


