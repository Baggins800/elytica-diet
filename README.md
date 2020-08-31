# The Diet Problem
Make sure you use `python --version` >= 3.7
## Install Required Packages
Install the required packages with `pip` by running:
```
 pip install tk configparser pandas pandastable elytica-dss xlsxwriter
```
### Ubuntu module error
Should you get the ``ModuleNotFoundError: No module named 'tkinter'`` in Ubuntu 18+, try installing the `python3-tk` distro library:
```
sudo apt install python3-tk
```
If you are not using Ubuntu and you get this error, make sure that you have `Tcl/Tk` libraries installed. Refer to the [TkDocs](https://tkdocs.com/tutorial/install.html#installlinux) for additional instructions

## Run the Program
If you are running the program from a shell, use:

```
python DietProblem.py
```
Otherwise, if you are using an IDE like PyCharm, select `DietProblem.py` as the script to run.

On operating systems where both Python2.7 and Python3 is installed it might be necessary to run using `python3`:
```
python3 DietProblem.py
```
