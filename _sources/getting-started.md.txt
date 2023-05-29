# Getting started with toml_dataclass

Toml and Python Dataclass serialization.

## Features

- Preserve the in-memory representation of Python dataclasses

## Examples

### Creating a dataclass with support to toml serialization.

```python
>>> from danoan.toml_dataclass import TomlDataClassIO
>>> from dataclasses import dataclass

>>> @dataclass
... class Plugin(TomlDataClassIO):
...    name: str
...    version: str
...    description: str


>>> jpg_plugin = Plugin("image-jpg", "1.0", "Conversion functions to jpg type.")
>>> with open("jpg-plugin.toml", "w") as fw:
...     jpg_plugin.write(fw)

```

Here it is what it looks like the written toml.

```python
>>> with open("jpg-plugin.toml", "r") as fr:
...     print(fr.read())
name = "image-jpg"
version = "1.0"
description = "Conversion functions to jpg type." 

```

### Preserve the in-memory representation of Python dataclasses after reading.

```python
>>> from pprint import pprint
>>> @dataclass
... class Configuration(TomlDataClassIO):
...     project_name: str
...     plugin: Plugin

>>> config = Configuration("image-reader", jpg_plugin)
>>> with open("config.toml", "w") as fw:
...     config.write(fw)

>>> with open("config.toml", "r") as fr:
...     config_from_file = Configuration.read(fr)
>>> pprint(config_from_file)
Configuration(project_name='image-reader',
              plugin=Plugin(name='image-jpg',
                            version='1.0',
                            description='Conversion functions to jpg type.'))

>>> pprint(f"Plugin name: {config_from_file.plugin.name}")
'Plugin name: image-jpg'

```

Notice how it differs from the ouptut of the `toml` library.

```python
>>> import toml
>>> pprint(toml.load("config.toml"))
{'plugin': {'description': 'Conversion functions to jpg type.',
            'name': 'image-jpg',
            'version': '1.0'},
 'project_name': 'image-reader'}

```

### Preserve in-memory representation with toml tables.

```python
>>> from danoan.toml_dataclass import TomlTableDataClassIO
>>> from typing import List

>>> @dataclass
... class PluginTable(TomlTableDataClassIO):
...     list_of_plugins: List[Plugin]

>>> png_plugin = Plugin("image-png", "1.0", "Conversion functions to png type.")
>>> plugin_table = PluginTable([jpg_plugin, png_plugin])
>>> with open("plugin-table.toml", "w") as fw:
...     plugin_table.write(fw)

>>> with open("plugin-table.toml", "r") as fr:
...     plugin_table_from_file = PluginTable.read(fr)
>>> pprint(plugin_table_from_file)
PluginTable(list_of_plugins=[Plugin(name='image-jpg', 
                                    version='1.0', 
                                    description='Conversion functions to jpg '
                                                'type.'), 
                             Plugin(name='image-png', 
                                    version='1.0', 
                                    description='Conversion functions to png '
                                                'type.')])

```

Notice how it differs from the ouptut of the `toml` library.

```python
>>> pprint(toml.load("plugin-table.toml"))
{'list_of_plugins': [{'description': 'Conversion functions to jpg type.',
                      'name': 'image-jpg',
                      'version': '1.0'},
                     {'description': 'Conversion functions to png type.',
                      'name': 'image-png',
                      'version': '1.0'}]}

```

Here it is what looks like the written toml.

```python
>>> with open("plugin-table.toml", "r") as f:
...     print(f.read())
[[list_of_plugins]]
name = "image-jpg"
version = "1.0"
description = "Conversion functions to jpg type."
<BLANKLINE>
[[list_of_plugins]]
name = "image-png"
version = "1.0"
description = "Conversion functions to png type."
<BLANKLINE>
<BLANKLINE>

```

