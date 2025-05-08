class SwagTag:
    """
    A class that stores information about tags relating to api endpoints.

    Attributes
    ----------
    name : str
        the name of the tag.
    desc : str
        a description about the tag.
    """
    
    def __init__(self, name: str, desc: str):
        self.__name: str = name
        self.__desc: str = desc

    def to_doc(self) -> dict[str, str]:
        return {
            "name": self.name,
            "description": self.desc
        }

    @property
    def name(self) -> str:
        return self.__name

    @property
    def desc(self) -> str:
        return self.__desc

