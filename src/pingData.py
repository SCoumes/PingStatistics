from typing import List, Dict, Tuple, Union, Optional
from dataclasses import dataclass
from collections import Counter

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
    color : str
    name : str

    @classmethod
    def getNew(cls, filePath : str):
        """
        Create a new PingData object.
        """
        return cls(Date.now(), [], filePath, ["pingNumber", "timeSinceLastPing", "averagePing"], "#ffffff", "New ping stat collector")
    
    def setColor(self, color : str):
        """
        Set the color of the ping stat collector.
        """
        self.color = color

    def ping(self, date : Date):
        self.pingList.append(date)
        self.pingList.sort()

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
            days = round(self.getTimeSinceLastPing())
            hours = round((self.getTimeSinceLastPing() - days) * 24)
            minutes = round(((self.getTimeSinceLastPing() - days) * 24 - hours) * 60)
            return "Last ping : " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes"
        if statName == "averagePing":
            return "Pings per day : " + str(round(self.getAveragePing(), 2))
        if statName == "frequencyInDay":
            return "Fraction of days with a ping : " + str(round(self.getFrequencyInDay(), 2))
        if statName == "maxInDay":
            return "Maximum day : " + str(self.getMaxInDay())
        if statName == "medianDay":
            return "Median day : " + str(self.getMedianDay())
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
    
    def getFrequencyInDay(self):
        """
        Calculate the fraction of days with a ping.
        """
        days = len(set([ping.getDayStr() for ping in self.pingList]))
        days = max(Date.now().minus(self.begining), 1)
        return self.getPingNumber() / days
    
    def _getOrderedPingsInDays(self)->List[int]:
        """
        Get a list containing numbers of ping in a day, for all days since the begining.
        """
        begin = self.begining
        end = max(Date.now(), max(self.pingList, default=begin))
        days = [0] * (int(end.minus(begin)) + 1)
        for ping in self.pingList:
            days[int(ping.minus(begin))] += 1
        return sorted(days)
        #return list(Counter([ping.getDayStr() for ping in self.pingList]).values()).sort()

    def getMaxInDay(self):
        """
        Calculate the maximum number of pings in a day.
        """
        if len(self._getOrderedPingsInDays()) == 0:
            return 0
        return self._getOrderedPingsInDays()[-1]
    
    def getMedianDay(self):
        """
        Calculate the day with the median number of pings.
        """
        if len(self._getOrderedPingsInDays()) == 0:
            return 0
        return self._getOrderedPingsInDays()[len(self._getOrderedPingsInDays())//2]

