from typing import List, TYPE_CHECKING
import json
import os.path as path

from src import PingData, Date

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
    return PingData(begining, pings, fileName, ["pingNumber", "timeSinceLastPing", "averagePing"])

def readMainFile(fileName : str, dataController : 'DataController'):
    """
    Read a the file from a file and updates the dataController with necessary information. Does not directly read the ping data.
    """
    dirname = path.dirname(fileName)
    with open(fileName, "r") as f:
        data = json.load(f)
    pingDataFileNames : List[str] = [path.join(dirname,fileName) for fileName in data["pingDataFileNames"]]
    dataController.pingDataFilePaths = pingDataFileNames
    