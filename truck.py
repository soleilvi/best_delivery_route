class Truck:
    def __init__(self, id):
        self.id = id
        self.speed = 18
        self.packages = []

    def is_full(self):
        if len(self.packages) == 16:
            return True
        else:
            return False
