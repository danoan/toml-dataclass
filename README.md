# Toml Dataclass

Interchangeable representation between toml and Python dataclass.

## Features

- Empower your dataclass with toml representation

## Examples

```python
from danoan.utils.toml_dataclass import TomlDataClassIO, TomlTableDataClassIO

from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class Plugin(TomlDataClassIO):
    name: str
    version: str
    description: str


@dataclass
class PluginTable(TomlTableDataClassIO):
    list_of_plugins: List[Plugin]


@dataclass
class Configuration(TomlDataClassIO):
    project_name: str
    location_folder: str
    plugins: PluginTable


p1 = Plugin("image-jpg", "1.0", "Conversion functions to jpg type.")
p2 = Plugin("image-png", "1.0", "Conversion functions to png type.")

original_configuration = Configuration(
    "image-library", "/users/bentinho/image-library", PluginTable([p1, p2])
)
toml_filepath = Path("").joinpath("example.toml")
original_configuration.write(toml_filepath)

loaded_configuration = Configuration.read(toml_filepath)
assert loaded_configuration == original_configuration

print(original_configuration)
# Configuration(project_name='image-library', location_folder='/users/bentinho/image-library', plugins=PluginTable(list_of_plugins=[Plugin(name='image-jpg', version='1.0', description='Conversion functions to jpg type.'), Plugin(name='image-png', version='1.0', description='Conversion functions to png type.')]))

print(loaded_configuration)
# Configuration(project_name='image-library', location_folder='/users/bentinho/image-library', plugins=PluginTable(list_of_plugins=[Plugin(name='image-jpg', version='1.0', description='Conversion functions to jpg type.'), Plugin(name='image-png', version='1.0', description='Conversion functions to png type.')]))

print(toml.load(toml_filepath))
# {'project_name': 'image-library', 'location_folder': '/users/bentinho/image-library', 'plugins': {'list_of_plugins': [{'name': 'image-jpg', 'version': '1.0', 'description': 'Conversion functions to jpg type.'}, {'name': 'image-png', 'version': '1.0', 'description': 'Conversion functions to png type.'}]}}

```

```toml
# example.toml 

project_name = "image-library"
location_folder = "/users/bentinho/image-library"

[plugins]
[[plugins.list_of_plugins]]
name = "image-jpg"
version = "1.0"
description = "Conversion functions to jpg type."

[[plugins.list_of_plugins]]
name = "image-png"
version = "1.0"
description = "Conversion functions to png type."

```
