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
        return False
        
    def is_empty(self):
        if len(self.packages) == 0:
            return True
        return False
        
    def load_package(self, package):
        if self.is_full():
            raise OverflowError(f"The truck is already full, could not load package.")
        else:
            self.packages.add(package)
    
    def load_packages(self, package_set):
        self.packages.update(package_set)
        if self.is_full():
            self.packages.discard(package_set)
            raise OverflowError(f"Truck is full. Maximum size is {self.capacity}, current load is {len(self.packages)}")
        
    def unload_package(self, package):
        if not self.packages:
            raise KeyError(f"The truck is empty, could not remove package.")
        elif not self.has_package(package):
            raise KeyError(f"The package set to be unloaded is not in the truck.")
        else:
            self.packages.remove(package)

    def has_package(self, package):
        if isinstance(package, int):
            for _package in self.packages:
                if _package.id == package:
                    return True
        else:
            if package in self.packages:
                return True
        return False
    
    def get_package(self, package):
        if isinstance(package, int):
            for _package in self.packages:
                if _package.id == package:
                    return _package
        else:
            if package in self.packages:
                return package
        raise KeyError(f"The package you are looking for is not in the truck.")
