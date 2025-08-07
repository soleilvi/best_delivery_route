class TimeMod: 
    """
    A class used to represent time. It uses a 24-hour format.

    Attributes
    ----------
    hour : int
        The hour at the desired time
    minutes : int
        The minutes at the desired time

    Methods
    -------
    distance_to_time(distance, mph)
        Converts speed and distance into time and sets the time to its result
    time_to_str()
        Returns a string version of the time object
    str_to_time(time_str)
        Converts a string into a time object
    __le__(another_time)
        Overloads the <= comparison operator
    __lt__(another_time)
        Overloads the < comparison operator
    __eq__(another_time)
        Overloads the == comparison operator
    add_time(time_to_add)
        Returns the sum of the current time and another time
    """
    def __init__(self, hour=0, minutes=0):
        """
        Parameters
        ----------
        hour : int
            The hour at the desired time (default 0)
        minutes : int
            The minutes at the desired time (default 0)
        """

        self.hour = hour % 24
        self.minutes = minutes % 60

    def distance_to_time(self, distance, mph):
        """Converts speed and distance into time and sets the time to its 
        result.

        Parameters
        ----------
        distance : float
            The distance travelled
        mph : int
            The speed at which the distance was travelled

        Raises
        ------
        N/A
        """

        self.hour = int(distance/mph) %  24
        self.minutes = int(distance/mph * 60) % 60
    
    def time_to_str(self):
        """Returns a string version of the time object.

        Parameters
        ----------
        N/A

        Raises
        ------
        N/A
        """

        time_str = ""
        if self.hour < 10:
            time_str += "0" + str(self.hour) + ":"
        else:
            time_str += str(self.hour) + ":"

        if self.minutes < 10:
            time_str += "0" + str(self.minutes)
        else:
            time_str += str(self.minutes)
            
        return time_str
    
    def str_to_time(self, time_str):
        """Converts a string into a time object.

        Parameters
        ----------
        time_str : str
           The string to be converted into a time object

        Raises
        ------
        N/A
        """

        # If it's just a single number, like 9:30 for the hour, add a space before it so that processing it is easier
        if time_str[1] == ':':
            time_str = " " + time_str

        self.hour = int(time_str[:2])
        self.minutes = int(time_str[3:5])
        if time_str[-2:] == "pm":
            self.hour += 12

    def __le__(self, another_time):
        """Overloads the <= comparison operator.

        Parameters
        ----------
        another_time : TimeMod
           The time that is being compared with the current time

        Raises
        ------
        N/A
        """

        if self.__lt__(another_time) or self.__eq__(another_time):
            return True
        return False
    
    def __lt__(self, another_time):
        """Overloads the < comparison operator.

        Parameters
        ----------
        another_time : TimeMod
           The time that is being compared with the current time

        Raises
        ------
        N/A
        """

        if self.hour < another_time.hour or (self.hour == another_time.hour and self.minutes < another_time.minutes):
            return True
        return False
    
    def __eq__(self, another_time):
        """Overloads the == comparison operator.

        Parameters
        ----------
        another_time : TimeMod
           The time that is being compared with the current time

        Raises
        ------
        N/A
        """

        if self.hour == another_time.hour and self.minutes == another_time.minutes:
            return True
        return False
    
    def add_time(self, time_to_add):
        """Returns the sum of the current time and another time.

        Parameters
        ----------
        time_to_add : Package
           The time to add to the current time

        Raises
        ------
        N/A
        """

        added_hours = (self.hour + time_to_add.hour) % 24
        added_minutes = self.minutes + time_to_add.minutes

        if added_minutes > 60:
            added_hours += int(added_minutes/60)
            added_minutes = (self.minutes + time_to_add.minutes) % 60
        
        return TimeMod(added_hours, added_minutes)