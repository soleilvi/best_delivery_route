from .timemod import TimeMod

class Package: 
    """
    A class used to represent a package

    Attributes
    ----------
    id : int
        The unique ID of the package
    address : str
        The address of the place to which the package should be delivered
    city : str
        The city where the delivery place is located
    state : str
        The state where the delivery place is located
    zip : str
        The zip code of the delivery place
    weight : str
        The weight of the package (in kilos)
    notes : str
        Notes with special delivery instructions
    deadline : TimeMod
        The time limit for the package's delivery

    Methods
    -------
    __le__(other_package)
        Overloads the <= comparison operator
    __lt__(other_package)
        Overloads the < comparison operator
    """

    def __init__(self, id, address, city, state, zip, deadline, weight,
                 notes=None):
        """
        Parameters
        ----------
        id : int
            The unique ID of the package
        address : str
            The address of the place to which the package should be delivered
        city : str
            The city where the delivery place is located
        state : str
            The state where the delivery place is located
        zip : str
            The zip code of the delivery place
        weight : str
            The weight of the package (in kilos)
        notes : str
            Notes with special delivery instructions
        deadline : str
            The time limit for the package's delivery (as just a written time)
        """

        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.weight = weight
        self.notes = notes if notes is not None else []

        if deadline == "EOD":
            self.deadline = TimeMod(23, 59)
        else:
            self.deadline = TimeMod()
            self.deadline.str_to_time(deadline)

    # Operator overloading to make heapq.heapify() work with package sorting
    def __le__(self, other_package):
        """Overloads the <= comparison operator.

        Parameters
        ----------
        other_package : Package
           The package that is being compared with the current package

        Raises
        ------
        N/A
        """

        if self.deadline <= other_package.deadline:
            return True
        return False
    
    def __lt__(self, other_package):
        """Overloads the < comparison operator.

        Parameters
        ----------
        other_package : Package
           The package that is being compared with the current package

        Raises
        ------
        N/A
        """

        if self.deadline < other_package.deadline:
            return True
        return False