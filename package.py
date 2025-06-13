class Package: 
    def __init__(self, id, address, city, state, zip, deadline, weight, dependencies=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.dependencies = dependencies if dependencies is not None else []
