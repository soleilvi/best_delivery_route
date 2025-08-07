class Place:
    """
    A class used to represent a place

    Attributes
    ----------
    id : int
        The unique ID of the place
    name : str
        The name of the place
    address : str
        The address of the place
    distances : list
        A list containing the distances of paths leading to other places

    Methods
    -------
    __le__(other_package)
        Overloads the <= comparison operator
    __lt__(other_package)
        Overloads the < comparison operator
    """

    def __init__(self, id, name, address):
        """
        Parameters
        ----------
        id : int
            The unique ID of the place
        name : str
            The name of the place
        address : str
            The address of the place
        """

        self.id = id
        self.name = name
        self.address = address
        self.distances = []

    # Operator overloading to make heapq.heapify() work with package sorting
    def __le__(self, other_place):
        """Overloads the <= comparison operator.

        Parameters
        ----------
        other_place : Package
           The place that is being compared with the current place

        Raises
        ------
        N/A
        """

        if self.id <= other_place.id:
            return True
        return False
    
    # Overloading comparison operator <
    def __lt__(self, other_place):
        """Overloads the < comparison operator.

        Parameters
        ----------
        other_place : Package
           The place that is being compared with the current place

        Raises
        ------
        N/A
        """

        if self.id < other_place.id:
            return True
        return False