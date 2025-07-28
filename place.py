class Place:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        self.distances = []

    # Overloading comparison operator <=
    def __le__(self, other_place):
        if self.id <= other_place.id:
            return True
        return False
    
    # Overloading comparison operator <
    def __lt__(self, other_place):
        if self.id < other_place.id:
            return True
        return False