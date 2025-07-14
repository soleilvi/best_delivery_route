class TimeMod: 
    def __init__(self, hour=0, minutes=0):
        self.hour = hour % 24
        self.minutes = minutes % 60

    def distance_to_time(self, distance, mph):
        self.hour = int(distance/mph) %  24
        self.minutes = int(distance/mph * 60) % 60
    
    def format_time(self):
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