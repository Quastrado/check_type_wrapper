# Check Type Wrapper


This is a simple function decorator that takes data types as parameters. These types must match the types of the arguments to the function. In case of type mismatch, an exception is thrown informing about the mismatch of the expected type with the received function


# Installation


Сreate a virtual environment in the project folder using the venv tool
```bash
$ python3 -m venv env
```
Activate the virtual environment
```bash
$ . env/bin/activate
```
Using PIP, install the third party decorator package
```bash
$ pip install Quastrado_check_type_wrapper
```


# Usage


Import the decorator. Write a simple function and wrap
```python
from check_type_wrapper import check_type

@check_type(int, int)
def func(arg1, arg2):
    return a + b

result = func('1', '2')
```
By passing parameters to the decorator, we indicate that the arguments that the function will accept must be of a numeric type. But, when calling the function, we will pass it two strings

Having run the code, in the terminal we should see the following in the terminal
```bash
...
    raise TypeMissMatchException(discrepancies)
check_type_wrapper.exception.TypeMissMatchException: 
Invalid type of argument 1. Expect int, not str
Invalid type of argument 2. Expect int, not str
```


# Status


Still in development
