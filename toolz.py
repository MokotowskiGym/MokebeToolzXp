import datetime
import math
# import numpy as np
import pandas as pd
import os
import datetime as dt
import sys
import pdb
from enum import Enum
from datetime import date, time
from dataclasses import dataclass
import typing as ty
# import mokebeCsvProcessing.settingsGeneral as s
import ctypes as ct
import tkinter as tk
from tkinter import filedialog
from enum import Enum
# dfdfg sdfsdf

strDateTimeFormat = "%Y-%m-%d %H%M%S"
strDateFormat = "%Y-%m-%d"
strTimeFormat = "%H:%M:%S"
strTimeFormat_df = "%H:%M"


class gluPathMode(Enum):
    absolute = 101
    relative = 102


class gluCreateFolderMode(Enum):
    overwrite = 1
    ignoreIfExists = 2
    breakIfExists = 3





def createFolder(folderParts, mode: gluCreateFolderMode):
    path = buildFolderPath(folderParts)

    if mode == gluCreateFolderMode.overwrite:
        # exist_ok = False
        raise Exception(666)
    elif mode == gluCreateFolderMode.breakIfExists:
        # exist_ok = False
        raise Exception(666)
    elif mode == gluCreateFolderMode.ignoreIfExists:
        exist_ok = True
    else:
        raise Exception(666)

    os.makedirs(path, exist_ok=exist_ok)

    if not os.path.isdir(path):
        raise Exception(f"Folder\n'{path}'\ndoes not exist")


def saveCsv(
        df: pd.DataFrame,
        folderParts: list,
        fileName: str, sep=";",
        createFolderMode: gluCreateFolderMode = gluCreateFolderMode.ignoreIfExists,
        returnPathMode: gluPathMode = gluPathMode.absolute
) -> str:
    folderPath = buildFolderPath(folderParts)
    createFolder(folderPath, createFolderMode)
    csvPath = "/".join([folderPath, fileName])

    df.to_csv(path_or_buf=csvPath, encoding="utf-8", index=False, sep=sep, decimal=".", quotechar="'")
    # print(absolutizePath("sdf.csv", gluPathMode.absolute))
    return absolutizePath(csvPath , returnPathMode)


def buildFolderPath(folderParts: list) -> str:
    if isContainer(folderParts):
        path = folderParts
    else:
        path = "/".join(folderParts)

    return path


def absolutizePath(path: str, pathMode: gluPathMode):
    if pathMode == pathMode.absolute:
        path_safe = os.path.abspath(path)
    elif pathMode == pathMode.relative:
        path_safe == path
    else:
        raise Exception
    return path_safe


def typeName(sth) -> str:
    return sth.__class__.__name__


def isContainer(sth):
    tn = typeName(sth)
    if tn == "str":
        container = True
    elif tn == "list":
        container = False
    else:
        raise Exception("Unhandled type '{tn}'")
    return container


def nowStr():
    return dt.datetime.now().strftime(strDateTimeFormat)


def returnNullSafe(value, valueIfNull):
    if math.isnan(value):
        return valueIfNull
    else:
        return value


def getProjectFolder():
    path = os.getcwd()
    return path


def returnDateTime(
        xDate: dt.date,
        xTimeStr: str,
        timeFormat: str = "HH:MM"
) -> dt.datetime:
    xTime = returnTimeDelta(xTimeStr, timeFormat)
    xDateTime = dt.datetime.combine(xDate, dt.time(0, 0, 0)) + xTime
    return xDateTime


def returnTelemetricDate(
        xDate: dt.date,
        timeDelta: dt.timedelta
) -> dt.date:
    hours = timeDelta.seconds / 3600

    if hours >= 24:
        offset = 1
    else:
        offset = 0

    return xDate + dt.timedelta(days=offset)





def returnTimeDelta(
        timeStr: str,
        timeFormat: str = "HH:MM"
):
    if timeFormat == "HH:MM":
        timeArr = timeStr.split(":")
        hours = int(timeArr[0])
        minutes = int(timeArr[1])
        seconds = 0
    else:
        raise Exception(f'Unknown format {format_}')

    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)


@dataclass
class XlDate:
    xDateTime: dt.datetime
    xDate: dt.date
    xTime: dt.time

    def __init__(self, xDate: datetime.date, timeStr: str = None, xTime: dt.time = None, timeFormat: str = "HH:MM"):
        if (timeStr is None) == (xTime is None):
            raise Exception("Najebane z argumentami")
        self.xDateTime = returnDateTime(xDate, timeStr, timeFormat=timeFormat)
        self.xDate = self.xDateTime.date()
        self.xTime = self.xDateTime.time()

    def printDateTime(self):
        print(self.xTime)


def gluStop() -> None:
    if s.debugMode() == s.gluDebugMode.debug:
        breakpoint()

def addErr(errMsg:str):
    print(errMsg)
    raise Exception(errMsg)


def msgBox(title, text, style=0):
    return ct.windll.user32.MessageBoxW(0, text, title,   style)




class FileType(Enum):
    ALL_FILES = ("All Files", "*.*")
    DAT_FILES = ("DAT Files", "*.dat")
    NO_EXTENSION_FILES = ("No Extension Files", "*.")
    EXCEL_FILES = ("Excel Files", "*.xlsx;*.xlsm")

import tkinter as tk
from tkinter import filedialog
from enum import Enum

class FileType(Enum):
    ALL_FILES = ("All Files", "*.*")
    DAT_FILES = ("DAT Files", "*.dat")
    NO_EXTENSION_FILES = ("No Extension Files", "*.")
    EXCEL_FILES = ("Excel Files", "*.xlsx;*.xlsm")

def returnFile(file_type:FileType, initialdir="."):
    """
    Shows a file dialog and returns the selected file path.

    :param file_type: Enum value representing the file types to filter. Defaults to FileType.ALL_FILES.
    :param initialdir: String representing the folder in which the dialog starts. Defaults to the current directory.
    :return: The selected file path.
    :raises: ValueError if no file was selected.
    """
    root = tk.Tk()
    root.withdraw()

    file_types = [file_type.value]

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=file_types,
        initialdir=initialdir
    )

    if not file_path:
        raise ValueError("No file was selected")

    return file_path