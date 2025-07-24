from timemod import TimeMod

# Operator overloading to make heapq.heapify() work with package sorting
class Package: 
    def __init__(self, id, address, city, state, zip, deadline, weight, notes=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.weight = weight
        self.notes = notes if notes is not None else []

        if deadline == "EOD":
            self.deadline = TimeMod(23, 59)
        else:
            self.deadline = TimeMod()
            self.deadline.str_to_time(deadline)

    # Overloading comparison operator <=
    def __le__(self, other_package):
        if self.deadline.is_less_than(other_package.deadline) or self.deadline.is_equal_to(other_package.deadline):
            return True
        return False
    
    # Overloading comparison operator <
    def __lt__(self, other_package):
        if self.deadline.is_less_than(other_package.deadline):
            return True
        return False