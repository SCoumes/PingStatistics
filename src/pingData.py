from typing import List, Dict, Tuple, Union, Optional
from math import floor
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
    fileName : str
    statsToShow : List[str] 
    color : str
    name : str
    transitivity : str | None

    @classmethod
    def getNew(cls, fileName : str):
        """
        Create a new PingData object.
        """
        return cls(Date.now(), [], fileName, ["pingNumber", "timeSinceLastPing", "averagePing"], "#ffffff", "New ping stat collector", None)
    
    def setColor(self, color : str):
        """
        Set the color of the ping stat collector.
        """
        self.color = color

    def ping(self, date : Date):
        if date < self.begining:
            self.begining = date
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
        """
        Compute and format the text to display to the user for a given stat.
        @param statName : The string identifier for the stat to get the text for.
        @return : The text to display to the user for the stat.
        """
        if statName == "timeSinceLastPing":
            timeSinceLastPing = self.getTimeSinceLastPing()
            days = floor(timeSinceLastPing)
            hours = floor((timeSinceLastPing - days) * 24)
            minutes = floor(((timeSinceLastPing - days) * 24 - hours) * 60)
            return "Last ping : " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes"
        if statName == "pingNumber":
            return "Pings : " + str(self.getPingNumber())
        if statName == "averagePing":
            return "Pings per day : " + str(round(self.getAveragePing(), 2))
        if statName == "frequencyInDay":
            return "Fraction of days with a ping : " + str(round(self.getFrequencyInDay(), 2))
        if statName == "maxInDay":
            return "Maximum day : " + str(self.getMaxInDay())
        if statName == "medianDay":
            return "Median day : " + str(self.getMedianDay())
        if statName == "last30days":
            return "Pings in the last 30 days : " + str(self.getLast30days())
        if statName == "averagePing30days":
            return "Pings per day in the last 30 days : " + str(round(self.getAveragePing30days(), 2))
        if statName == "frequencyInDay30days":
            return "Fraction of days with a ping in the last 30 days : " + str(round(self.getFrequencyInDay30days(), 2))
        if statName == "maxInDay30days":
            return "Maximum day in the last 30 days : " + str(self.getMaxInDay30days())
        if statName == "medianDay30days":
            return "Median day in the last 30 days : " + str(self.getMedianDay30days())
        assert False, "Invalid stat name"
    
    def getTimeSinceLastPing(self) -> float:
        """
        Get the number of days since the last ping.
        Return 0 if there are no pings.
        """
        if self.getPingNumber() == 0:
            return 0.0
        return Date.now().minus(self.pingList[-1])

    def getPingNumber(self):
        return len(self.pingList)
 
    def getLast30days(self):
        """
        Get the number of pings in the last 30 days.
        """
        return len([ping for ping in self.pingList if Date.now().minus(ping) < 30])

    def getAveragePing(self):
        """
        Calculate the average number of pings per day.
        """
        val = self.getPingNumber() / max(Date.now().minus(self.begining), 1)
        return val
    
    def getAveragePing30days(self):
        """
        Calculate the average number of pings in the last 30 days.
        """
        return self.getLast30days() / 30
    
    def getFrequencyInDay(self):
        """
        Calculate the fraction of days with a ping.
        """
        days = len(set([ping.getDayStr() for ping in self.pingList]))
        days = max(Date.now().minus(self.begining), 1)
        return self.getPingNumber() / days
    
    def getFrequencyInDay30days(self):
        """
        Calculate the fraction of days with a ping in the last 30 days.
        """
        days = len(set([ping.getDayStr() for ping in self._getPings30days()]))
        return days/30
    
    def _getOrderedPingsInDays(self)->List[int]:
        """
        Get a list containing numbers of ping in a day, for all days since the begining.
        """
        begin = self.begining
        end = max(Date.now(), max(self.pingList, default=begin))
        days = [0] * (int(end.minus(begin)) + 1)
        for ping in self.pingList:
            days[int(ping.minus(begin))] += 1
        return days
        #return list(Counter([ping.getDayStr() for ping in self.pingList]).values()).sort()

    def getMaxInDay(self):
        """
        Calculate the maximum number of pings in a day.
        """
        daysNumberPings = self._getOrderedPingsInDays()
        if len(daysNumberPings) == 0:
            return 0
        return sorted(daysNumberPings)[-1]
    
    def getMaxInDay30days(self):
        """
        Calculate the maximum number of pings in a day in the last 30 days.
        """
        daysNumberPings = self._getOrderedPingsInDays()
        if len(daysNumberPings) == 0:
            return 0
        if len(daysNumberPings) < 30:
            return sorted(daysNumberPings)[-1]
        return sorted(daysNumberPings[-30:])[-1]
    
    def getMedianDay(self):
        """
        Calculate the day with the median number of pings.
        """
        daysNumberPings = self._getOrderedPingsInDays()
        if len(daysNumberPings) == 0:
            return 0
        return sorted(daysNumberPings)[len(daysNumberPings)//2]

    def getMedianDay30days(self):
        """
        Calculate the day with the median number of pings in the last 30 days.
        """
        daysNumberPings = self._getOrderedPingsInDays()
        if len(daysNumberPings) == 0:
            return 0
        if len(daysNumberPings) < 30:
            return sorted(daysNumberPings)[len(daysNumberPings)//2]
        return sorted(daysNumberPings[-30:])[15]
    
    def _getPings30days(self):
        """
        Get the pings in the last 30 days.
        """
        return [ping for ping in self.pingList if Date.now().minus(ping) < 30]

