class PlacesHash: 
    def __init__(self, hash_size):
        self.hash = [None] * hash_size

    # assumes that any address apart from the hub starts with either 3 or 4 number digits 
    # depending on how many collisions there are in your data set, you may want to use the first 3 digits or the last 3 digits. 
    def load(self, places_data):
        for place in places_data:
            key = ''.join(num for num in place.address[:4] if num.isdigit()) # Extract the first 3 digits of the address as a key. The first digit is a space.
            if key == '':  # This is for the hub 
                key = 0
            else:
                key = int(key)
                
            index = key % len(self.hash)  # Division method for hashing
            
            # Initialize with the place if the bucket is empty
            if self.hash[index] is None:
                self.hash[index] = [place]

            # Collision handling (chaining)
            else:
                print("collision detected")  # for determining index insertion method
                self.hash[index].append(place)

    def address_to_place(self, address):
        key = ''.join(num for num in address[:3] if num.isdigit())  # [:3] instead of [:4] because the address format in a package object excludes the space at the beginning
        if key == '': 
            key = 0
        else:
            key = int(key)  

        index = key % len(self.hash)  

        for place in self.hash[index]:
            if address[:4] in place.address[:5]:
                return place

        raise ValueError(f"Could not find a match for {address}.")

    def has_place(self, place):
        key = ''.join(num for num in place.address[:4] if num.isdigit())
        if key == '': 
            key = 0
        else:
            key = int(key)  
        index = key % len(self.hash)  

        if self.hash[index] is None:
            return False
        else:
            if place in self.hash[index]:
                return True
            else:
                return False
    
    def get(self, place):
        if self.has_place(place):
            return place
        else:
            raise ValueError(f"Place not in hash, could not retrieve it.")
    
    def remove(self, place):
        key = ''.join(num for num in place.address[:4] if num.isdigit())
        if key == '': 
            key = 0
        else:
            key = int(key)
        index = key % len(self.hash)  
        
        if self.has_place(place):
            self.hash[index].remove(place)
            if not self.hash[index]:
                self.hash[index] = None
        else:
            raise ValueError(f"Place not in hash, could not remove it.")