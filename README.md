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

Run specified problem solutions. Check answer, if a non-none value is given, with argument `-c` or
`--check`.

## Solution structure

Each problem solution is a python module in `problems` directory. Only two module level variables
`PID` for problem ID and `ANSWER` for answer of the problem.

Solver method functions MUST BE defined at less one, whose function name is `solve` or starts with
`solve_`. All solver method will be run to evaluate, and at least one solver method function
returns correct answer in timeout limit makes the framework treats this problem is solved correctly.

If `ANSWER` is `None` or not presented, the solution will not be checked.

```python
#!/usr/bin/env python3
# coding: utf-8


PID = 1
ANSWER = 42


def solve():
    return 42


def solve_method_1():
    return 42


def solve_method_2():
    return 42


```

The following module level configure variables are supported:
- `PID`: Problem ID, required.
- `ANSWER`: Answer of the problem, optional.
- `TIMEOUT_EXT`: Extra timeout (in milliseconds) for the problem, optional.


## External data loading

In some problems, like [problem 22](problems/p0022.py), external data is required to
solve the problem. The framework provides an automatic way to load external data, with the
following steps:

1.  Download external data from Project Euler website, and save it to `data` directory.
2.  Write data loading module, store in `data` directory, with the filename exactly the same as
    the filename of problem solution file. A method `load()` MUST BE implemented in the module, and
    return the load data. See example in [data of problem 22](data/p0022.txt) and
    [data loader of problem 22](data/p0022.py).
    ```python
    #!/usr/bin/env python3
    # coding: utf-8
    # data/example.py
    
    
    def load():
        result = []
        with open("data/example.txt", "r") as fd:
            for line in fd:
                result.append(int(line))
    ```
3.  In the solution module of problem, import the data loading module, and call `data.load()`
    method to load data. See example in [solution of problem 22](problems/p0022.py).
    ```python
    #!/usr/bin/env python3
    # coding: utf-8
    # problems/example.py
    
    
    from data import load
    
    
    PID = 0
    ANSWER = 42
    
    
    def solve():
        data = load()
        return sum(data)
    ```
