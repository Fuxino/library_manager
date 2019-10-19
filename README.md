library_manager
==============
Library_manager is a simple program I wrote to manage my Library database.

## Build
To manually install the program, first clone the repository:

```bash
git clone https://github.com/Fuxino/library_manager.git
cd library_manager
```

Then as root:

```bash
python3 setup.py install --optimize=1
python3 setup.py clean --all
```

For Arch Linux, a PKGBUILD that automates this process is provided.

## Usage
Library_manager works with the Library database I created to manage my books. I included the Sql file that allows to recreate the database structure.

## Dependencies
The program is written in `Python3` and uses `PyQt5` for the GUI. `QtSql` is used to connect to the database (only MySQL is supported).
