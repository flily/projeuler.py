# projeuler.py

[![Check](https://github.com/flily/projeuler.py/actions/workflows/ci.yaml/badge.svg)](https://github.com/flily/projeuler.py/actions/workflows/ci.yaml)

Code solutions for Project Euler problems


## Usage
```bash
$ python3 projeuler.py [COMMAND] [OPTIONS ...] [PROBLEMS ...]
```

### Command `list`

Show problems solved, show full problem content  with argument `-f` or `--full`.

### Command `run`

Run specified problem solutions. Check answer, if a non-none value is given, with argument `-c` or `--check`.

## Solution structure

Each problem solution is a python module in `problems` directory. Only two module level variables `PID` for problem ID and `ANSWER` for answer of the problem and a function `solve` for solution are required for the module.

If `ANSWER` is `None`, the solution will not be checked.

```python
#!/usr/bin/env python3
# coding: utf-8


PID = 1
ANSWER = 42


def solve():
    return 42

```

