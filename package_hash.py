class PackageHash:
    """
    Hash table used to store and retrieve packages.

    Attributes
    ----------
    hash : list
        List that holds the packages

    Methods
    -------
    load(package_data)
        Loads the packages into the hash
    has_package(package)
        Checks if the package is in the hash
    get(package)
        Returns the package in the hash
    get_through_id(package_id)
        Returns the package in the hash, but searches it through its ID
    remove(package)
        Removes the package from the hash
    """

    def __init__(self, hash_size):
        """
        Parameters
        ----------
        hash_size : int
            The size of the list being initialized
        """

        self.hash = [None] * hash_size

    def load(self, package_data):
        """Loads the packages into the hash.

        Parameters
        ----------
        package_data : list
            A list of the packages that will be loaded into the hash

        Raises
        ------
        N/A
        """
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
        """Checks if the package is in the hash.

        Parameters
        ----------
        package : Package
            The package that the user wants to check is in the hash.

        Raises
        ------
        N/A
        """

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
        """Returns the package in the hash.

        Parameters
        ----------
        package : Package
            The package that the user wants to retrieve from the hash.

        Raises
        ------
        ValueError
            If the package is not found in the hash.
        """

        if self.has_package(package):
            return package
        else:
            raise ValueError(f"Package not in hash, could not retrieve it.")
    
    def get_through_id(self, package_id):
        """Returns the package in the hash, but searches it through its ID.

        Parameters
        ----------
        package : int
            The ID of the package that the user wants to retrieve from the hash.

        Raises
        ------
        ValueError
            If the package is not found in the hash.
        """

        key = package_id
        index = (key - 1) % len(self.hash)

        if self.hash[index] is None:
            raise ValueError(f"Package not in hash, could not retrieve it.")
        else:
            for package in self.hash[index]:
                if int(package.id) == package_id:
                    return package
        raise ValueError(f"Package not in hash, could not retrieve it.")
    
    def remove(self, package):
        """Removes the package from the hash

        Parameters
        ----------
        package : Package
            The package that the user wants to remove from the hash.

        Raises
        ------
        ValueError
            If the package is not found in the hash.
        """

        key = int(package.id)
        index = (key - 1) % len(self.hash)
        
        if self.has_package(package):
            self.hash[index].remove(package)

            # If there are no other packages in the bucket at the current index 
            if not self.hash[index]:
                self.hash[index] = None
            
        else:
            raise ValueError("Package not in hash, could not remove it.")
            
        