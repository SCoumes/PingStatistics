import os
import json
from src import PingData, Date
from src.reader import readPingData
from src.writer import writePingData

def test_WriteAndRead():
    testDir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test", "testFiles")
    begining = Date.now()
    pings = [Date.now(), Date.now()]
    fileName = os.path.join(testDir, "test1.json")
    pingData = PingData(begining, pings, fileName)
    writePingData(pingData)
    result = readPingData(fileName)
    assert result.begining.toText() == begining.toText()
    for ping, resultPing in zip(pings, result.pingList):
        assert ping.toText() == resultPing.toText()
    assert result.fileName == fileName