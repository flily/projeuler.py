# projeuler.py

[![Check](https://github.com/flily/projeuler.py/actions/workflows/ci.yaml/badge.svg)](https://github.com/flily/projeuler.py/actions/workflows/ci.yaml)

![GitHub License](https://img.shields.io/github/license/flily/projeuler.py)
![GitHub top language](https://img.shields.io/github/languages/top/flily/projeuler.py)
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

### Command `create`

Create a new problem solution template.


## Solution structure

Each problem solution is a python module in `problems` directory, and filename MUST BE format like
`pXXXX.py`. Module level variable `PID` is legacy used to identify the problem, and no longer used.

Solver method functions MUST BE defined at less one, whose function name is `solve` or starts with
`solve_`. All solver method will be run to evaluate, and at least one solver method function
returns correct answer in timeout limit makes the framework treats this problem is solved correctly.

If `ANSWER` is `None` or not presented, the solution will not be checked.

```python
#!/usr/bin/env python3
# coding: utf-8


ANSWER = 42


def solve():
    return 42


def solve_method_1():
    """
    Description to method 1. (Show in report)

    Detail description to method 1. (Not show in report)
    """
    return 42


def solve_method_2():
    return 42


```

The following module level configure variables are supported:
- `PID`: Problem ID, legacy used to identify the problem, and no longer used.
- `ANSWER`: Answer of the problem, optional.
- `TIMEOUT_EXT`:
  - an `int` or `float`, Extra timeout (in milliseconds) for the problem, optional.
  - a `dict[str, int | float]`, Extra timeout (in milliseconds) for each method, optional.
    + If key is actually the same to method name, the extra timeout will be applied to this method.
    + If key starts with `*`, the extra timeout will be applied to all methods whose name contains
      the string after `*`. For example, `{"*cache": 2500.0}`, all method whose name contains
      `cache`, like `solve_with_cache_set` and `solve_with_cache_dict` will get extra timeout 2500ms.
    + If key is `*`, the extra timeout will be applied to all methods, which has no specific
      extra timeout by other keys.

## External data loading

In some problems, like [problem 22](problems/p0022.py), external data is required to
solve the problem. The framework provides an automatic way to load external data, with the
following steps:

1.  Download external data from Project Euler website, and save it to `data` directory.
    The filename in format `pXXXX.txt`, which is exactly the same as problem solution file.
    See example in [data of problem 22](data/p0022.txt).
2.  Write data loading handler, in your solution file in `problems` directory, you can use any name
    for function name of data handler.
    See [data loader of problem 22](problems/p0022.py#L27).
    ```python
    def data_handler(data: str) -> list[str]:
        items = data.split(",")
        result = [x[1:-1] for x in items]   # remove quotes
        return result
    ```
3.  Then in your solution methods in the same file, call `data.load(data_handler)`
    method to load data. See example in [solution of problem 22](problems/p0022.py#).
    ```python
    #!/usr/bin/env python3
    # coding: utf-8
    # problems/example.py
    
    
    from data import load
    
    
    ANSWER = 42
    
    def data_handler(data: str) -> list[str]:
        items = data.split(",")
        result = [x[1:-1] for x in items]   # remove quotes
        return result
    
    
    def solve():
        data = load(data_handler)
        return sum(data)
    ```
