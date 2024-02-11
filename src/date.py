from typing import List, Dict, Tuple, Union, Optional
from dataclasses import dataclass

from datetime import datetime, timezone

class Date:
    """
    Store information for dates and times.
    """
    datetimeObj : datetime

    def __init__(self, text : str) -> None:
        """
        Should only be called with a full isoformat string that includes the timezone.
        """
        self.datetimeObj = datetime.fromisoformat(text)

    def toText(self) -> str:
        """
        Convert the date object to a string.
        """
        return self.datetimeObj.isoformat()

    def minus(self, other: 'Date') -> float:
        """
        Subtract the other date from this date.
        @return: The difference between the two dates as a decimal number of days.
        """
        return (self.datetimeObj - other.datetimeObj).total_seconds() / (60 * 60 * 24)
    
    def getDayStr(self):
        """
        Get the day as a string.
        """
        return self.datetimeObj.strftime("%d%m%Y")

    @classmethod
    def now(cls):
        """
        Get the current time.
        """
        return cls(datetime.now(cls._getLocalTimezone()).isoformat())
    
    @classmethod
    def fromNaive(cls, date: datetime):
        """
        Create a Date object from a naive datetime object.
        """
        return cls(date.replace(tzinfo=cls._getLocalTimezone()).isoformat())
        
    @classmethod
    def _getLocalTimezone(cls) -> timezone:
        """
        Get the local timezone.
        """
        return datetime.now(timezone.utc).astimezone().tzinfo

    def __str__(self) -> str:
        return self.toText()

    def __lt__(self, other: 'Date') -> bool:
        return self.datetimeObj < other.datetimeObj
    
    def __eq__(self, other: 'Date') -> bool:
        return self.datetimeObj == other.datetimeObj