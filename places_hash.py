class PlacesHash: 
    """
    Hash table used to store and retrieve places.

    Attributes
    ----------
    hash : list
        List that holds the places

    Methods
    -------
    load(places_data)
        Loads places into the hash
    address_to_place(address)
        Looks up a place through its address and returns it
    has_package(place)
        Checks if the place is in the hash
    get(place)
        Returns the places in the hash
    remove(place)
        Removes the places from the hash
    """

    def __init__(self, hash_size):
        """
        Parameters
        ----------
        hash_size : int
            The size of the list being initialized
        """
         
        self.hash = [None] * hash_size

    def load(self, places_data):
        """Loads places into the hash.

        Assumes that any address apart from the hub starts with either 3 or 4 
        number digits. Depending on how many collisions there are in your data 
        set, you may want to use the last 3 digits instead of the first 3 
        digits.

        Parameters
        ----------
        places_data : list
            A list of the places that will be loaded into the hash

        Raises
        ------
        N/A
        """

        for place in places_data:
            # Extract the first 3 digits of the address as a key. The first 
            # digit is a space.
            key = ''.join(num for num in place.address[:4] if num.isdigit())
            if key == '':  # This is for the hub 
                key = 0
            else:
                key = int(key)
                
            index = key % len(self.hash)  # Division method for hashing.
            
            # Initialize with the place if the bucket is empty.
            if self.hash[index] is None:
                self.hash[index] = [place]

            # Collision handling (chaining)
            else:
                # Print statement for determining index insertion method.
                print("collision detected")  
                self.hash[index].append(place)

    def address_to_place(self, address):
        """Looks up a place through its address and returns it.

        Parameters
        ----------
        address : str
            The address of the place that the user wants to look up.

        Raises
        ------
        ValueError
            If the place is not found in the hash.
        """

        # [:3] instead of [:4] because the address format in a package object 
        # excludes the space at the beginning.
        key = ''.join(num for num in address[:3] if num.isdigit()) 
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
        """Checks if the place is in the hash.

        Parameters
        ----------
        place : Place
            The place that the user wants to check is in the hash.

        Raises
        ------
        N/A
        """

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
        """Returns the place in the hash.

        Parameters
        ----------
        place : Place
            The place that the user wants to retrieve from the hash.

        Raises
        ------
        ValueError
            If the place is not found in the hash.
        """

        if self.has_place(place):
            return place
        else:
            raise ValueError(f"Place not in hash, could not retrieve it.")
    
    def remove(self, place):
        """Removes the place from the hash

        Parameters
        ----------
        place : Place
            The place that the user wants to remove from the hash.

        Raises
        ------
        ValueError
            If the place is not found in the hash.
        """

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