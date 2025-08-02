# Formats time in a 24-hour format
class TimeMod: 
    def __init__(self, hour=0, minutes=0):
        self.hour = hour % 24
        self.minutes = minutes % 60

    def distance_to_time(self, distance, mph):
        self.hour = int(distance/mph) %  24
        self.minutes = int(distance/mph * 60) % 60
    
    def time_to_str(self):
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
        # If it's just a single number, like 9:30 for the hour, add a space before it so that processing it is easier
        if time_str[1] == ':':
            time_str = " " + time_str

        self.hour = int(time_str[:2])
        self.minutes = int(time_str[3:5])
        if time_str[-2:] == "pm":
            self.hour += 12

    # TODO: Delete theses methods once you have changed to operators in all the other files
    def is_less_than(self, another_time):
        if self.hour < another_time.hour or (self.hour == another_time.hour and self.minutes < another_time.minutes):
            return True
        return False
    
    def is_equal_to(self, another_time):
        if self.hour == another_time.hour and self.minutes == another_time.minutes:
            return True
        return False
    
    # Overloading comparison operator <
    def __lt__(self, another_time):
        if self.hour < another_time.hour or (self.hour == another_time.hour and self.minutes < another_time.minutes):
            return True
        return False
    
    # Overloading comparison operator ==
    def __eq__(self, another_time):
        if self.hour == another_time.hour and self.minutes == another_time.minutes:
            return True
        return False
    
    # Overloading comparison operator <=
    def __le__(self, another_time):
        if self.__lt__(another_time) or self.__eq__(another_time):
            return True
        return False
    
    def add_time(self, time_to_add):
        added_hours = (self.hour + time_to_add.hour) % 24
        added_minutes = self.minutes + time_to_add.minutes

        if added_minutes > 60:
            added_hours += int(added_minutes/60)
            added_minutes = (self.minutes + time_to_add.minutes) % 60
        
        return TimeMod(added_hours, added_minutes)