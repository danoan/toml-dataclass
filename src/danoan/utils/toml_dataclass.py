"""
toml_dataclass.py

Manipulate toml and Python dataclass interchangeably.

"""
import copy
import toml
from typing import Any, Dict, Optional, TextIO, TypeVar, Type


class TomlDataClassIO:
    """
    Base class for a simple dataclass (i.e. with no mapping types)
    """

    T = TypeVar("T", bound="TomlDataClassIO")

    @classmethod
    def read(cls: Type[T], filepath: str) -> Optional[T]:
        """
        Create an instance of the derived class from a toml file.

        Args:
            filepath: Path to a toml file.

        Returns:
            Instance of the type of cls.
        """
        with open(filepath, "r") as f:
            return cls.read_stream(f)
        return None

    @classmethod
    def read_stream(cls: Type[T], stream_in: TextIO) -> T:
        """
        Create an instance of the derived class from a toml file.

        Args:
            stream_in: Stream object serving toml data.

        Returns:
            Instance of the type of cls.
        """
        d = toml.load(stream_in)
        return cls._from_dict(d)

    def write(self, filepath: str):
        """
        Write the dataclass as a toml file.

        Args:
            filepath: Path to the output toml file.
        """
        with open(filepath, "w") as f:
            self.write_stream(f)

    def write_stream(self, stream_out: TextIO):
        """
        Write the dataclass as a toml file.

        Args:
            stream_out: Stream object where the toml string is output.
        """
        toml.dump(self._as_dict(), stream_out)

    @classmethod
    def _from_dict(cls: Type[T], d: Dict[str, Any]) -> T:
        """
        Create an instance of the derived class from a toml dict.

        The toml library internally encodes toml data as a python dictionary.
        This method is not supposed to be called directly, but internally it
        should be used in a way similar to the following:

        Example:
            toml_data = toml.load(toml_filepath)
            my_instance = MyDataClass._from_dict(toml_data)

        Important:
            Notice that the output of this method can be different from the output
            of toml.load

        Example:
            @dataclass
            class Plugin:
                name: str

            @dataclass
            class Configuration:
                name: str
                list_of_plugins: List[Plugin]

            original_c = Configuration( "my-config", [Plugin("image-jpg"), Plugin("image-png")])
            original_c.write(toml_filepath)

            print(original_c)
            # Configuration(name='my-configuration', list_of_plugins=[Plugin(name='image-jpg'),Plugin('image-png')])

            toml_loaded_c = toml.load(toml_filepath)
            print(toml_loaded_c)
            # Configuration(name='my-configuration', list_of_plugins=[{'name':'image-jpg'},{'name': 'image-png'}])

            loaded_c = Configuration.read(toml_filepath)
            print(loaded_c)
            # Configuration(name='my-configuration', list_of_plugins=[Plugin(name='image-jpg'),Plugin('image-png')])

        Important:
            Use ::read or ::read_stream instead.

        Args:
            d: Python dictionary output by toml.load
        """
        _d = copy.deepcopy(d)
        for attr_name, attr_type in cls.__annotations__.items():
            has_mro = getattr(attr_type, "mro", None) is not None
            if has_mro and (
                TomlDataClassIO in attr_type.mro() or TomlTableDataClassIO in attr_type.mro()
            ):
                _d[attr_name] = attr_type._from_dict(_d[attr_name])

        return cls(**_d)

    def _as_dict(self) -> Dict[str, Any]:
        """
        Create a pure Python dict representation of the derived class.

        The dictionary returned by this method is similar to the one returned
        by the toml.load method.

        Returns:
            Python dictionary that encodes the dataclass.
        """
        d = copy.deepcopy(self.__dict__)
        for attr_name, attr_value in d.items():
            if isinstance(attr_value, TomlDataClassIO) or isinstance(
                attr_value, TomlTableDataClassIO
            ):
                d[attr_name] = attr_value._as_dict()

        return d


class TomlTableDataClassIO(TomlDataClassIO):
    T = TypeVar("T", bound="TomlDataClassIO")

    @classmethod
    def _from_dict(cls: Type[T], d: Dict[str, Any]) -> T:
        """
        Create an instance of the derived class from a toml dict.

        See Also:
            ::TomlDataClassIO._from_dict
        """
        (table_name,) = cls.__annotations__.keys()
        entry_type = list(cls.__annotations__.values())[0].__args__[0]

        my_table = []
        for entry in d[table_name]:
            my_table.append(entry_type._from_dict(entry))

        return cls(**{table_name: my_table})

    def _as_dict(self) -> Dict[str, Any]:
        """
        Create a pure Python dict representation of the derived class.

        See Also:
            ::TomlDataClassIO._as_dict
        """
        (table_name,) = self.__annotations__.keys()
        return {table_name: [entry._as_dict() for entry in self.__dict__[table_name]]}
