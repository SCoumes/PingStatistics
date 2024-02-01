import os.path as path
from src import Date, PingData

def writePingData(pingData: PingData):
    """
    Write the ping data to a file.
    """
    with open(pingData.filePath, "w") as file:
        file.write(getPingDataJson(pingData))

def getPingDataJson(pingData: PingData) -> str:
    """
    Get the json text for the ping data.
    """
    text = "{"
    text += f"\"begining\": \"{pingData.begining.toText()}\","
    text += "\"pings\": ["
    text += ",".join([f"\"{ping.toText()}\"" for ping in pingData.pingList])
    text += "]"
    text += ",\"statsToShow\": ["
    text += ",".join([f"\"{statName}\"" for statName in pingData.statsToShow])
    text += "]"
    text += ",\"color\": \"" + pingData.color + "\""
    text += "}"
    return text

import os.path as path

def writeMainFile(filePath: str, pingDataFilePaths: list[str]):
    """
    Write the main file.
    """
    with open(filePath, "w") as file:
        text = """{ "pingDataFileNames" : [""" + ",".join(["\"" + path.basename(pingDataFilePath) + "\"" for pingDataFilePath in pingDataFilePaths]) + "]}"
        file.write(text)