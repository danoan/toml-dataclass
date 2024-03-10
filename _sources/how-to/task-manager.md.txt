# Task Manager System

Let us use the `TomlDataClassIO` and `TomlTableClassIO` to create an interface between Python classes and toml files used in a task manager system.

## System Configuration File

We start by creating a configuration file that stores information such as
the default folder where to store tasks.


``` python
>>> from danoan.toml_dataclass import TomlDataClassIO

>>> import io
>>> from dataclasses import dataclass

>>> @dataclass
... class ConfigurationFile(TomlDataClassIO):
...    default_folder: str

>>> config = ConfigurationFile("/home/user/task-manager")

```

The `TomlDataClassIO` equips their derived classes with the methods `read` and
`write` that does the interface between in-memory Python objects and toml
files.

We can use the method `write` to store the configuration file.

```python
>>> with open("config.toml", "w") as f:
...     config.write(f)

```

We can use the method `read` to read the contents of the toml file to create
an instance of the corresponding Python object.

```python
>>> from pprint import pprint
>>> with open("config.toml", "r") as f:
...     config_from_file = ConfigurationFile.read(f)

>>> pprint(config_from_file)
ConfigurationFile(default_folder='/home/user/task-manager')

```

Here it what looks like the stored toml file

```toml
default_folder = "/home/user/task-manager"
```

## Storing the task table

Now we create our class to represent a task.

```python
>>> import datetime
>>> @dataclass
... class Task(TomlDataClassIO):
...     name: str
...     creation_date: datetime.datetime
...     command: str

```

Next, let us register some tasks and store them in a toml table. In order to
do that, we need the `TomlTableClassIO`.

```python
>>> from danoan.toml_dataclass import TomlTableDataClassIO
>>> from typing import List

>>> @dataclass
... class TaskTable(TomlTableDataClassIO):
...     list_of_tasks: List[Task]

>>> t1 = Task("init-service", datetime.datetime.fromtimestamp(1676194367.101537, datetime.timezone.utc).isoformat(), "init-service.sh" )
>>> t2 = Task("run-tests", datetime.datetime.fromtimestamp(1676194367.101537, datetime.timezone.utc).isoformat(), "run-tests.sh")
>>> with open("task-table.toml", "w") as fw:
...     TaskTable([t1,t2]).write(fw)

```

Notive that we passed the filepath to the `write` method. This will open a file
stream in write mode. To read the table, we use the method `read`.

```python
>>> with open("task-table.toml", "r") as fr:
...     task_table = TaskTable.read(fr)
>>> pprint(task_table)
TaskTable(list_of_tasks=[Task(name='init-service',
creation_date='2023-02-12T09:32:47.101537+00:00',
                              command='init-service.sh'),
                         Task(name='run-tests',
                         creation_date='2023-02-12T09:32:47.101537+00:00',
                              command='run-tests.sh')])

```

Here it what looks like the stored toml file

```toml
[[list_of_tasks]]
name = "init-service"
creation_date = "2023-02-12T10:32:47.101537"
command = "init-service.sh"

[[list_of_tasks]]
name = "run-tests"
creation_date = "2023-02-12T10:32:47.101537"
command = "run-tests.sh"

```
