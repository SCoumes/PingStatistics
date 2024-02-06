from typing import List, TYPE_CHECKING, Optional
import json
import os.path as path

from src import PingData, Date
from src.writer import initMainFile

if TYPE_CHECKING:
    from src.controllers import DataController

def readPingData(fileName: str) -> PingData:
    """
    Read a ping data from a file.
    """
    with open(fileName, "r") as f:
        data = json.load(f)
    begining = Date(data["begining"])
    pings = [Date(ping) for ping in data["pings"]]
    statsToShow = data["statsToShow"]
    color = data["color"]
    name = data["name"]
    return PingData(begining, pings, fileName, statsToShow,color,name)

def readMainFile(fileName : str | None, dataController : 'DataController'):
    """
    Read a the file from a file and updates the dataController with necessary information. Does not directly read the ping data.
    """
    if fileName == None:
        dataController.pingDataFilePaths = []
        return
    if not path.exists(fileName):
        initMainFile(fileName)
    dirname = path.dirname(fileName)
    with open(fileName, "r") as f:
        data = json.load(f)
    pingDataFileNames : List[str] = [path.join(dirname,fileName) for fileName in data["pingDataFileNames"]]
    dataController.pingDataFilePaths = pingDataFileNames
    

def readSettingsFile(fileName : str, dataController : 'DataController'):
    """
    Read the settings file.
    """
    try:
        with open(fileName, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # Return default values, a setting file should be created when the user chooses a save location.
        dataController.width = 800
        dataController.height = 600
        dataController.mainFilePath = None
        return
    try : 
        dataController.mainFilePath = data["mainFilePath"]
    except KeyError:
        dataController.mainFilePath = None
    dataController.width = data["width"]
    dataController.height = data["height"]