from timemod import TimeMod

class Truck:
    def __init__(self, id, depart_time = TimeMod(8, 0)):
        self.id = id
        self.depart_time = depart_time
        self.speed = 18
        self.capacity = 16
        self.packages = set()

    def is_full(self):
        if len(self.packages) >= self.capacity:
            return True
        else:
            return False
        
    def load_package(self, package):
        if self.is_full():
            raise OverflowError(f"Truck is full. Maximum size is {self.capacity}")
        else:
            self.packages.add(package)
    
    def load_packages(self, package_set):
        if self.is_full():
            raise OverflowError(f"Truck is full. Maximum size is {self.capacity}")
        elif len(self.packages) + len(package_set) > self.capacity:
            raise OverflowError(f"Truck cannot load the packages because it will be too full. Maximum size is {self.capacity}")
        else:
            self.packages.update(package_set)

    def has_package(self, package):
        if isinstance(package, int):
            print("PEE")
            for _package in self.packages:
                print(f"package id stuff: {_package.id}")
                if _package.id == package:
                    print("conclusion true")
                    return True
        else:
            if package in self.packages:
                return True
        return False
