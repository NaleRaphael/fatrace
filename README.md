# Editor for [fatraceschool][url_fatraceschool]
**UI of this app is not completed, so you have to execute this by editing the variables in `main.py` and running a Python process.**

A editor to reduce repeated works on recording ingredients information of lunch for students.

* Requirement  
Python 2.7 (for Windows users, [WinPython][url_winpython] is recommended)


## Usage
1. Edit the file path of `menu` and `database` in `main.py`.
```python
# @line 27, 28
fpath = r'path\of\your\menu.xlsx'
dbpath = r'path\of\ingredient_database.json' # default: db_ingr.json
```

2. Execute this script, and output files will locates in the working directory.
```bash
$ cd fatrace
$ python main.py
```

[url_fatraceschool]: https://fatraceschool.moe.gov.tw/ "fatraceschool"

[url_winpython]: https://sourceforge.net/projects/winpython/files/WinPython_2.7/2.7.10.3/ "WinPython 2.7"
