from timemod import TimeMod

class Truck:
    """
    A class used to represent a truck.

    The trucks at other facilites may have different average speeds and 
    capacities. If that is the case, future developers will need to change the 
    hardcoded values of the speed and capacity attributes in the init method 
    or initialize them with parameters.

    Attributes
    ----------
    id : int
        The unique ID of the truck
    depart_time : TimeMod
        The time at which the truck leaves the facility
    speed : int
        The average speed at which the truck travels
    capacity : int
        How many packages the truck can hold
    packages: set
        A set of the packages in the truck

    Methods
    -------
    is_full()
        Checks if the packages set has reached the truck's maximum capacity
    is_empty()
        Checks if the packages set is empty
    load_package(package)
        Adds a package to the truck's packages set
    load_packages(package_set)
        Adds a set of packages to the truck's packages set
    unload_package(package)
        Removes a package from the truck's packages set
    has_package(package)
        Returns true if the package is in the truck's packages set
    get_package(package)
        Returns the package without unloading it
    """

    def __init__(self, id, depart_time = TimeMod(8, 0)):
        """
        Parameters
        ----------
        id : int
            The unique ID of the truck
        depart_time : TimeMod
            The time at which the truck leaves the facility. Default value is 
            8:00 AM.
        capacity : int
            How many packages the truck can hold
        packages: set
            A set of the packages in the truck
        """
        
        self.id = id
        self.depart_time = depart_time
        self.speed = 18
        self.capacity = 16
        self.packages = set()

    def is_full(self):
        """Checks if the packages set has reached the truck's maximum 
        capacity.

        Parameters
        ----------
        N/A

        Raises
        ------
        N/A
        """

        if len(self.packages) >= self.capacity:
            return True
        return False
        
    def is_empty(self):
        """Checks if the packages set is empty.

        Parameters
        ----------
        N/A

        Raises
        ------
        N/A
        """
        
        if len(self.packages) == 0:
            return True
        return False
        
    def load_package(self, package):
        """Adds a package to the truck's packages set.

        Parameters
        ----------
        package : Package
           The package that should be loaded onto the truck.

        Raises
        ------
        OverflowError
            If the truck is already full.
        """

        if self.is_full():
            raise OverflowError(f"The truck is already full, could not load package.")
        else:
            self.packages.add(package)
    
    def load_packages(self, package_set):
        """Adds a set of packages to the truck's packages set.

        Parameters
        ----------
        package_set: set
            A set containing the packages that should be loaded into the 
            truck.

        Raises
        ------
        OverflowError
            If the truck is already full.
        """

        self.packages.update(package_set)
        if self.is_full():
            self.packages.discard(package_set)
            raise OverflowError(f"Truck is full. Maximum size is {self.capacity}, current load is {len(self.packages)}")
        
    def unload_package(self, package):
        """Removes a package from the truck's packages set.

        Parameters
        ----------
        package : Package
           The package that should be unloaded onto the truck.

        Raises
        ------
        KeyError
            If the package to be unloaded cannot be found in the truck.
        """

        if not self.packages:
            raise KeyError(f"The truck is empty, could not remove package.")
        elif not self.has_package(package):
            raise KeyError(f"The package set to be unloaded is not in the truck.")
        else:
            self.packages.remove(package)

    def has_package(self, package):
        """Returns true if the package is in the truck's packages set.

        Parameters
        ----------
        package : Package
           The package that the user wants to find in the truck.

        Raises
        ------
        N/A
        """

        if isinstance(package, int):
            for _package in self.packages:
                if _package.id == package:
                    return True
        else:
            if package in self.packages:
                return True
        return False
    
    def get_package(self, package):
        """Returns the package without unloading it.

        Parameters
        ----------
        package : Package
           The package that the user wannts to get from the truck.

        Raises
        ------
        KeyError
            If the package to be retrieved cannot be found in the truck.
        """

        if isinstance(package, int):
            for _package in self.packages:
                if _package.id == package:
                    return _package
        else:
            if package in self.packages:
                return package
        raise KeyError(f"The package you are looking for is not in the truck.")
