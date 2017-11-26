# Editor for [fatraceschool][url_fatraceschool]
**UI of this app is not completed, you can execute the script through CLI.**

A editor to reduce repeated works on recording ingredients information of lunch for students.

* Requirement  
Python 2.7 (for Windows users, [WinPython][url_winpython] is recommended)


## Usage
* Generate ingredient sheets from menu.
```bash
> python main.py parse -f [menu.xlsx] [-o [output_directory] --db [path_of_database]]
```

* Insert new dish into database.
```bash
> python main.py update_db -d [dish_name] -i [ingredient_01 ingredient_02 ...] [--force [True/False] --db [path_of_database]]
```

[url_fatraceschool]: https://fatraceschool.moe.gov.tw/ "fatraceschool"

[url_winpython]: https://sourceforge.net/projects/winpython/files/WinPython_2.7/2.7.10.3/ "WinPython 2.7"
