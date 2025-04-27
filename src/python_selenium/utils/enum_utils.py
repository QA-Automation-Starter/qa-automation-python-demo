from typing import Type



class EnumBaseEx:
    """
    A base class for enums, enabling instantiation from a number.
    """

    @classmethod
    def from_[T:EnumBaseEx](cls: Type[T], value: int) -> T:
        """
        Converts a given value to the corresponding enum member.

        Args:
            cls: The enum class itself (Type[T:EnumEx]).
            value: The value to be converted, which can be either a string
                   or an integer.

        Returns:
            T: The enum member that matches the provided value.

        Raises:
            ValueError: If the provided value does not match any enum member's value.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"the value {value} is not a valid {cls.__name__}")
