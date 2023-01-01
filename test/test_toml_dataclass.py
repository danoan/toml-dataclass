from dataclasses import dataclass
from typing import List, Optional

import pytest

from danoan.utils.toml_dataclass import TomlDataClassIO, TomlTableDataClassIO


@dataclass
class Plugin(TomlDataClassIO):
    name: str
    description: str
    version: Optional[str] = None


@dataclass
class PluginTable(TomlTableDataClassIO):
    list_of_plugins: List[Plugin]


@dataclass
class Configuration(TomlDataClassIO):
    project_name: str
    location_folder: str
    plugins: PluginTable


def test_read_write_file_toml_data_class_io(tmp_path):
    original_p = Plugin("image-jpg", "Conversion functions to jpg type.", "1.0")

    toml_filepath = tmp_path.joinpath("plugin.toml")
    original_p.write(toml_filepath)

    loaded_p = Plugin.read(toml_filepath)
    assert loaded_p == original_p


def test_read_write_stream_toml_data_class_io(tmp_path):
    original_p = Plugin("image-jpg", "Conversion functions to jpg type.", "1.0")

    toml_filepath = tmp_path.joinpath("plugin.toml")
    with open(toml_filepath, "w") as f:
        original_p.write_stream(f)

    with open(toml_filepath, "r") as f:
        loaded_p = Plugin.read_stream(f)

    assert loaded_p == original_p


def test_read_write_file_toml_table_data_class_io(tmp_path):
    p1 = Plugin("image-jpg", "1.0", "Conversion functions to jpg type.")
    p2 = Plugin("image-jpg", "1.0", "Conversion functions to png type.")

    original_list_of_plugins = PluginTable([p1, p2])
    toml_filepath = tmp_path.joinpath("list-of-plugins.toml")
    original_list_of_plugins.write(toml_filepath)

    loaded_list_of_plugins = PluginTable.read(toml_filepath)
    assert loaded_list_of_plugins == original_list_of_plugins


def test_read_write_stream_toml_table_data_class_io(tmp_path):
    p1 = Plugin("image-jpg", "1.0", "Conversion functions to jpg type.")
    p2 = Plugin("image-png", "1.0", "Conversion functions to png type.")

    original_list_of_plugins = PluginTable([p1, p2])
    toml_filepath = tmp_path.joinpath("list-of-plugins.toml")

    with open(toml_filepath, "w") as f:
        original_list_of_plugins.write_stream(f)

    with open(toml_filepath, "r") as f:
        loaded_list_of_plugins = PluginTable.read_stream(f)

    assert loaded_list_of_plugins == original_list_of_plugins


def test_read_write_file_complex(tmp_path):
    p1 = Plugin("image-jpg", "1.0", "Conversion functions to jpg type.")
    p2 = Plugin("image-png", "1.0", "Conversion functions to png type.")

    original_configuration = Configuration(
        "image-library", "/users/bentinho/image-library", PluginTable([p1, p2])
    )
    toml_filepath = tmp_path.joinpath("list-of-plugins.toml")
    original_configuration.write(toml_filepath)

    loaded_configuration = Configuration.read(toml_filepath)
    assert loaded_configuration == original_configuration
