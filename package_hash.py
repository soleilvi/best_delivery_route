class PackageHash:
    def __init__(self, hash_size):
        self.hash = [None] * hash_size

    def load(self, package_data):
        for package in package_data:
            key = int(package.id)
            index = (key - 1) % len(self.hash)  # Division method for hashing
            
            # Initialize with the package if the bucket is empty
            if self.hash[index] is None:
                self.hash[index] = [package]

            # Collision handling (chaining)
            else:
                self.hash[index].append(package)

    def has_package(self, package):
        key = int(package.id)
        index = (key - 1) % len(self.hash)

        if self.hash[index] is None:
            return False
        else:
            if package in self.hash[index]:
                return True
            else:
                return False
    
    def get(self, package):
        if self.has_package(package):
            return package
        else:
            raise ValueError(f"Package with ID {package.id} not in hash, could not retrieve it.")
    
    def remove(self, package):
        key = int(package.id)
        index = (key - 1) % len(self.hash)
        
        if self.has_package(package):
            self.hash[index].remove(package)
            print("removed")
        else:
            raise ValueError("Package with ID {package.id} not in hash, could not remove it.")
            
        