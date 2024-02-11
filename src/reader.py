from typing import List, TYPE_CHECKING, Optional
import json
import os.path as path

from src import PingData, Date
from src.writer import initMainFile

if TYPE_CHECKING:
    from src.controllers import DataController

def readPingData(dirName : str, fileName: str) -> PingData:
    """
    Read a ping data from a file.
    """
    filePath = path.join(dirName, fileName)
    with open(filePath, "r") as f:
        data = json.load(f)
    begining = Date(data["begining"])
    pings = [Date(ping) for ping in data["pings"]]
    statsToShow = data["statsToShow"]
    color = data["color"]
    name = data["name"]
    if "transitiveTowards" in data:
        transitivity = data["transitiveTowards"]
    else :
        transitivity = None

    return PingData(begining, pings, fileName, statsToShow, color, name, transitivity)

def readMainFile(fileName : str | None, dataController : 'DataController'):
    """
    Read a the file from a file and updates the dataController with necessary information. Does not directly read the ping data.
    """
    if fileName == None:
        dataController.pingDataFileNames = []
        return
    if not path.exists(fileName):
        initMainFile(fileName)
    with open(fileName, "r") as f:
        data = json.load(f)
    pingDataFileNames : List[str] = data["pingDataFileNames"] 
    dataController.pingDataFileNames = pingDataFileNames

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