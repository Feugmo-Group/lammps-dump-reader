from enum import Enum
from typing import Generator
import yaml

# unDumped = [{'TIMESTEP':int, 'NUMBER OF ATOMS':int, 'BOX BOUNDS':dict, 'ATOMS':[dict specific to dump style]}]


class Modes(Enum):
    TIME = 1
    NUM = 2
    BOUNDS = 3
    ATOM = 4


def read_classic(file: str) -> Generator[dict[str:any], None, None]:
    """Generator object that yields one frame of the file at a time for classic style lammp dump files"""

    unDumped = {}
    loopCount = 0

    with open(file, "r") as myfile:
        for line in myfile:
            loopCount += 1
            if "TIMESTEP" in line:
                loopCount = 0
                mode = Modes.TIME
                checkLoop = loopCount
                unDumped = {"ATOMS": []}
            if mode == Modes.TIME and (loopCount - checkLoop) == 1:
                unDumped["TIMESTEP"] = int(line)
            if "NUMBER OF ATOMS" in line:
                mode = Modes.NUM
                checkLoop = loopCount
            if mode == Modes.NUM and (loopCount - checkLoop) == 1:
                unDumped["NUMBER OF ATOMS"] = int(line)
                frameLength = int(line)
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
                lengthCheck = 0
                v_line = line.split()
            if mode == Modes.ATOM and (loopCount - checkLoop) >= 1:
                lengthCheck += 1
                s_line = line.split()
                paraCount = 0
                atomDict = {}
                for para in v_line:
                    if para != "ATOMS" and para != "ITEM:":
                        atomDict[para] = s_line[paraCount]
                        paraCount += 1
                unDumped["ATOMS"].append(atomDict)
            if mode == Modes.ATOM and lengthCheck == frameLength and unDumped:
                yield unDumped


def read_yaml(file: str) -> Generator[dict[str:any], None, None]:
    """Generator object that yields one frame of the file at a time for yaml style lammp dump files"""
    unDumped = {}
    with open(file, "r") as yams:
        for line in yaml.safe_load_all(yams):
            unDumped["TIMESTEP"] = line["timestep"]
            unDumped["NUMBER OF ATOMS"] = line["natoms"]
            unDumped["BOX BOUNDS"] = {}
            unDumped["BOX BOUNDS"]["x"] = line["box"][
                0
            ]  # this might not always be at the 0th entry, test other dump files to see whether true or not
            unDumped["BOX BOUNDS"]["y"] = line["box"][1]
            unDumped["BOX BOUNDS"]["z"] = line["box"][2]
            unDumped["ATOMS"] = []
            paraList = line["keywords"]
            for val in range(len(line["data"])):
                atomDict = {}
                paraNum = 0
                for para in paraList:
                    atomDict[para] = line["data"][val][paraNum]
                    paraNum += 1
                unDumped["ATOMS"].append(atomDict)
            yield unDumped


def read_dump(file, type=None):
    if type == "yaml":
        read_yaml(file)
    elif type == "classic":
        read_classic(file)
    if type == None:
        if ".yaml" in file:
            read_yaml(file)
        else:
            read_classic(file)


def read_whole_dump(file: str) -> list[dict[str:any]]:
    """read the entire file into an unDumped data structure"""
    return list(read_dump(file))


