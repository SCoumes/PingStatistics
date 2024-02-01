from typing import List, Dict, Tuple, Union, Optional
from dataclasses import dataclass

from src.date import Date

@dataclass
class PingData:
    """
    Data class for all the stored information related to a ping stat collector. Does not link to the controller for the main file.
    """
    begining : Date
    pingList : List[Date] # All pings sorted chronologically
    filePath : str
    statsToShow : List[str] 

    @classmethod
    def getNew(cls, filePath : str):
        """
        Create a new PingData object.
        """
        return cls(Date.now(), [], filePath, ["pingNumber", "timeSinceLastPing", "averagePing"])

    def ping(self, date : Date):
        self.pingList.append(date)

    def setStatsToShow(self, statsToShow : List[str]):
        """
        Sets the stats to show when presenting the data in a pingStat presenter widget.
        """
        self.statsToShow = statsToShow

    def getStatsToShow(self) -> List[str]:
        """
        Get the stats to show when presenting the data in a pingStat presenterw widget.
        """
        return self.statsToShow
    
    def getStatText(self, statName : str) -> str:
        if statName == "pingNumber":
            return "Ping number : " + str(self.getPingNumber())
        if statName == "timeSinceLastPing":
            return "Time since last ping : " + str(self.getTimeSinceLastPing())
        if statName == "averagePing":
            return "Average ping : " + str(self.getAveragePing())
        assert False, "Invalid stat name"
    
    def getPingNumber(self):
        return len(self.pingList)
    
    def getTimeSinceLastPing(self) -> float:
        """
        Get the number of days since the last ping.
        Return 0 if there are no pings.
        """
        if self.getPingNumber() == 0:
            return 0.0
        return Date.now().minus(self.pingList[-1])

    def getAveragePing(self):
        """
        Calculate the average number of pings per day.
        """
        val = self.getPingNumber() / max(Date.now().minus(self.begining), 1)
        return val
    

