# projeuler.py

[![Check](https://github.com/flily/projeuler.py/actions/workflows/ci.yaml/badge.svg)](https://github.com/flily/projeuler.py/actions/workflows/ci.yaml)
![GitHub repo file count (file extension)](https://img.shields.io/github/directory-file-count/flily/projeuler.py/problems?label=Solved)

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

If `ANSWER` is `None` or not presented, the solution will not be checked.

```python
#!/usr/bin/env python3
# coding: utf-8


PID = 1
ANSWER = 42


def solve():
    return 42

```

The following module level configure variables are supported:
- `PID`: Problem ID, required.
- `ANSWER`: Answer of the problem, optional.
- `TIMEOUT_EXT`: Extra timeout (in milliseconds) for the problem, optional.
