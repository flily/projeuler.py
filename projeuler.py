#!/usr/bin/env python3
# coding: utf-8


"""
Main entry, runner of all problem solutions.
"""


from __future__ import annotations

import os
import sys
import ctypes
import platform
import inspect
import importlib
import argparse
import time
import multiprocessing

from datetime import datetime
from typing import (
    cast,
    Callable,
    Iterable,
    Iterator,
    Mapping,
)


import data


if sys.platform == "win32":
    from ctypes import wintypes

    ON_WINDOWS = True
    WIN_DLL = ctypes.LibraryLoader(ctypes.WinDLL)
else:
    ON_WINDOWS = False
    WIN_DLL = None


PROBLEM_DIR = "problems"
DEFAULT_TIMEOUT = 1000.0

OUTPUT_STREAM = sys.stdout


def _win_get_curse_position(handle) -> tuple[int, int]:
    if not ON_WINDOWS:
        return 0, 0

    class _ScreenBufferInfo(ctypes.Structure):
        # pylint: disable=too-few-public-methods, protected-access, used-before-assignment
        _fields_ = [
            ("dwSize", wintypes._COORD),
            ("dwCursorPosition", wintypes._COORD),
            ("wAttributes", wintypes.WORD),
            ("srWindow", wintypes.SMALL_RECT),
            ("dwMaximumWindowSize", wintypes._COORD),
        ]

    win32api_get_screen_buffer_info = WIN_DLL.kernel32.GetConsoleScreenBufferInfo
    win32api_get_screen_buffer_info.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(_ScreenBufferInfo),
    ]
    win32api_get_screen_buffer_info.restype = wintypes.BOOL

    info = _ScreenBufferInfo()
    win32api_get_screen_buffer_info(handle, ctypes.byref(info))
    x = cast(int, info.dwCursorPosition.X)
    y = cast(int, info.dwCursorPosition.Y)
    return x, y


is_windows_legacy_terminal = False
if sys.platform == "win32":
    _Win32APIGetStdHandle = WIN_DLL.kernel32.GetStdHandle
    _Win32APIGetStdHandle.argtypes = [wintypes.DWORD]
    _Win32APIGetStdHandle.restype = wintypes.HANDLE

    _handle = cast(wintypes.HANDLE, _Win32APIGetStdHandle(-11))
    _x0, _ = _win_get_curse_position(_handle)
    print("\033[D", end="", flush=True)  # move cursor to left
    _x1, _ = _win_get_curse_position(_handle)
    if _x1 - _x0 > 1:
        is_windows_legacy_terminal = True
        print("\b" * (_x1 - _x0), end="", flush=True)


class ProblemId:
    """
    Problem ID.
    """

    pid: int
    method: str

    def __init__(self, pid: int | str):
        if isinstance(pid, str):
            if "." in pid:
                pid, method = pid.split(".")
                self.pid = int(pid)
                self.method = method
            else:
                self.pid = int(pid)
                self.method = None

        elif isinstance(pid, int):
            self.pid = pid
            self.method = None

    def __eq__(self, other: ProblemId | int) -> bool:
        if isinstance(other, int):
            return self.pid == other

        if isinstance(other, ProblemId):
            return self.pid == other.pid and self.method == other.method

        return False

    def problem_name(self) -> str:
        """
        Get the filename of this problem.
        """
        return f"p{self.pid:04d}"


class RunConfigure:
    """
    Run configuration.
    """

    check: bool
    strict: bool
    colour: str
    timeout: float
    extra_timeout_map: bool
    preload: bool
    debug: bool
    id_list: Iterable[ProblemId]

    def __init__(self):
        self.check = False
        self.strict = False
        self.timeout = DEFAULT_TIMEOUT
        self.preload = True
        self.debug = False
        self.id_list = []

    @staticmethod
    def from_parser(result: argparse.Namespace) -> RunConfigure:
        """
        Create a run configuration from parser result.
        """
        conf = RunConfigure()
        conf.check = result.check
        conf.strict = result.strict
        conf.colour = result.colour
        conf.timeout = result.timeout
        conf.extra_timeout_map = result.extra_timeout_map
        conf.preload = not result.no_preload
        conf.id_list = result.id
        conf.debug = result.debug
        if result.no_timeout:
            conf.timeout = 0.0
        return conf


_default_run_configure = RunConfigure()


class _TimeSpanInMs(float):
    """
    Time span in milliseconds.
    """

    def __new__(cls, value: float | str):
        if isinstance(value, str):
            if value.endswith("ms"):
                value = float(value[0:-2])

            elif value.endswith("s"):
                value = float(value[0:-1]) * 1000.0

            else:
                value = float(value)

        return super().__new__(cls, value)


def _get_parser():
    parser = argparse.ArgumentParser(description="Project Euler problem runner")

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    cmd_list = subparsers.add_parser("list", help="list all problems")
    cmd_list.add_argument(
        "-f", "--full", action="store_true", help="show full information"
    )
    cmd_list.add_argument(
        "-m", "--show-missing", action="store_true", help="show missing problems"
    )
    cmd_list.add_argument(
        "id", nargs="*", type=ProblemId, help="show specific problem information"
    )

    cmd_create = subparsers.add_parser("create", help="create solutions of problems")
    cmd_create.add_argument("id", nargs="*", type=int, help="create specific problems")

    cmd_run = subparsers.add_parser("run", help="run problems")
    cmd_run.add_argument(
        "-c", "--check", action="store_true", help="check the solution answer"
    )
    cmd_run.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="run check in strict mode, all methods MUST be correct",
    )
    cmd_run.add_argument(
        "--colour", "--color",
        action="store_true",
        help="force colour output, even if not in TTY",
    )
    cmd_run.add_argument(
        "--no-preload", action="store_true", help="do not preload data"
    )
    cmd_run.add_argument(
        "-t",
        "--timeout",
        type=_TimeSpanInMs,
        default=DEFAULT_TIMEOUT,
        help="timeout for each method of a problem, in milliseconds, "
        + "or with unit like 500ms, 10s, 1m",
    )
    cmd_run.add_argument("-o", "--no-timeout", action="store_true", help="disable timeout")
    cmd_run.add_argument("-e", "--extra-timeout-map", action="store_true",
                         help="use problem specific extra timeout map for each method, "
                              "if not set, use the max extra timeout for all methods")
    cmd_run.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="debug mode, timeout will be disabled in debug mode",)
    cmd_run.add_argument("id", nargs="*", type=ProblemId, help="run specific problems")

    return parser


#               Black   Red     Green   Yellow  Blue    Magenta Cyan    White
# Normal        30      31      32      33      34      35      36      37
# Normal Bg     40      41      42      43      44      45      46      47
# Bright        90      91      92      93      94      95      96      97
# Bright Bg     100     101     102     103     104     105     106     107

#               Normal  Bold    Underline
# Style         0       1       4


COLOUR_MAP = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "on_black": 40,
    "on_red": 41,
    "on_green": 42,
    "on_yellow": 43,
    "on_blue": 44,
    "on_magenta": 45,
    "on_cyan": 46,
    "on_white": 47,
    "brightblack": 90,
    "brightred": 91,
    "brightgreen": 92,
    "brightyellow": 93,
    "brightblue": 94,
    "brightmagenta": 95,
    "brightcyan": 96,
    "brightwhite": 97,
    "on_brightblack": 100,
    "on_brightred": 101,
    "on_brightgreen": 102,
    "on_brightyellow": 103,
    "on_brightblue": 104,
    "on_brightmagenta": 105,
    "on_brightcyan": 106,
    "on_brightwhite": 107
}


def _get_colour_str(s: str, colour: str, is_tty: bool) -> str:
    if not is_tty:
        return s

    if platform.system() == "Windows" and is_windows_legacy_terminal:
        # Legacy Windows command prompt does not support ANSI escape code
        return s

    if colour not in COLOUR_MAP:
        return s

    return f"\033[{COLOUR_MAP[colour]}m{s}\033[0m"


class _StyleMeta(type):
    """
    Style meta class.
    """
    def __getattr__(cls, style):
        def _make_style(is_bold: bool = False, is_underline: bool = False) -> Style:
            if style not in COLOUR_MAP:
                return Style(is_bold=is_bold, is_underline=is_underline)

            return Style(style, is_bold, is_underline)

        return _make_style

class Style(metaclass=_StyleMeta):
    """
    Console string output style.
    """
    def __init__(self, colour: str | int | None = None, is_bold:
                 bool = False, is_underline: bool = False):
        self.colour = self._check_colour(colour)
        self.is_bold = is_bold
        self.is_underline = is_underline

    def _check_colour(self, colour: str | int | None) -> int:
        if colour is None:
            return 0

        if isinstance(colour, str):
            return COLOUR_MAP.get(colour, 0)

        r = 0
        if 30 <= colour <= 37:
            r = colour
        if 40 <= colour <= 47:
            r = colour
        if 90 <= colour <= 97:
            r = colour
        if 100 <= colour <= 107:
            r = colour
        return r

    def bold(self) -> Style:
        """
        Get new style with bold.
        """
        return Style(self.colour, is_bold=True, is_underline=self.is_underline)

    def no_bold(self) -> Style:
        """
        Get new style without bold.
        """
        return Style(self.colour, is_bold=False, is_underline=self.is_underline)

    def underline(self) -> Style:
        """
        Get new style with underline.
        """
        return Style(self.colour, is_bold=self.is_bold, is_underline=True)

    def no_underline(self) -> Style:
        """
        Get new style without underline.
        """
        return Style(self.colour, is_bold=self.is_bold, is_underline=False)

    def background(self) -> Style:
        """
        Get new style with background colour.
        """
        colour = self.colour
        if 30 <= colour <= 37 or 40 <= colour <= 47:
            colour += 10

        return Style(colour, is_bold=self.is_bold, is_underline=self.is_underline)

    def foreground(self) -> Style:
        """
        Get new style with foreground colour.
        """
        colour = self.colour
        if 40 <= colour <= 47 or 100 <= colour <= 107:
            colour -= 10

        return Style(colour, is_bold=self.is_bold, is_underline=self.is_underline)

    def apply(self, s: str, is_tty: bool = True) -> str:
        """
        Apply this style to a string.
        """
        code = self._check_colour(self.colour)
        if not is_tty or code == 0:
            return s

        parts = []
        if self.is_bold:
            parts.append(f"\033[1;{code}m")

        if self.is_underline:
            parts.append(f"\033[4;{code}m")

        if not parts:
            parts.append(f"\033[{code}m")

        parts.append(s)
        parts.append("\033[0m")

        return "".join(parts)

    def __repr__(self) -> str:
        notes = ""
        if self.is_bold:
            notes += " bold"
        if self.is_underline:
            notes += " underline"
        return f"Style(colour={self.colour}{notes})"

class _ColourOutMeta(type):
    """
    Colour output meta class.
    """

    def __getattr__(cls, colour):
        def _colour_print(s: str, is_tty: bool) -> None:
            return _get_colour_str(s, colour, is_tty)

        return _colour_print


class ClrOut(metaclass=_ColourOutMeta):
    """
    Colour output.
    """

    @staticmethod
    def write(s: str, colour: str, is_tty: bool) -> str:
        """
        Write a string with colour.
        """
        return _get_colour_str(s, colour, is_tty)


def _add_indent(s: str, indent: str) -> str:
    lines = s.split("\n")
    result = [indent + line for line in lines]
    return "\n".join(result)


def _make_line(*parts: str) -> str:
    return "| " + " | ".join(parts) + " |"


class _NotRunResult:
    def __repr__(self) -> str:
        return "NOT RUN"

    @staticmethod
    def check(other: object) -> bool:
        return isinstance(other, _NotRunResult)


class _TimeoutResult:
    def __repr__(self) -> str:
        return "TIMEOUT"


class SolutionMethod:
    """
    Solution method
    """

    def __init__(
        self, module_name: str, func: Callable[[], int], name: str, note: str = ""
    ):
        self.module_name = module_name
        self.func = func
        self.name = name
        self.note = note or ""
        self.timeout_ext = 0.0
        self.time_cost = 0.0
        self.result = _NotRunResult()
        self.finished = False

    def _proc_main(self, queue: multiprocessing.Queue):
        result = _NotRunResult()
        time_start = time.perf_counter()
        result = self.func()
        time_finish = time.perf_counter()
        dt = 1000.0 * (time_finish - time_start)

        queue.put((result, dt))

    def solve(self, runner: Runner, conf: RunConfigure, timeout: float = 0.0) -> None:
        """
        Run the solution method.
        """
        total_timeout = timeout
        if timeout > 0:
            total_timeout += self.timeout_ext

        result, timeouted, cost = runner.run_func(
            self.module_name, self.func, conf=conf, timeout=total_timeout
        )
        self.finished = not timeouted
        self.time_cost = cost
        if not timeouted:
            self.result = result

        else:
            self.result = None

    @property
    def title(self) -> str:
        """
        Title of this method.
        """
        result = self.name
        if self.note != "":
            result = self.note.strip().split("\n")[0]

        return result

    def is_timeout(self) -> bool:
        """
        Is solution method timeout
        """
        return not self.finished

    def has_result(self) -> bool:
        """
        Has result or not.
        """
        return not _NotRunResult.check(self.result)

    def print(
        self, pid: str, title: str, answer: int = None, timeout: float = 0.0, is_best: bool = False,
        is_tty: bool = False
    ) -> str:
        """
        Print result of this method.
        """
        if self.result is None:
            ans = f"{'NO RESULT':^30}"

        elif not self.has_result():
            ans = f"{'-':^30}"

        else:
            ans = f"{self.result:^30}"

        if self.is_timeout() and self.result is None:
            rc = "timeout"
            cl = Style.yellow()

        elif answer is None:
            rc = "?"
            cl = Style.yellow()

        elif not self.has_result():
            rc = "-"
            cl = Style.yellow()

        elif answer == self.result:
            rc = "correct"
            cl = Style.green()

        else:
            rc = "wrong"
            cl = Style.red()

        # column 1: PID
        line = [cl.apply(f"{pid:<4}", is_tty)]
        # column 2: title
        if is_best:
            line.append(cl.bold().background().apply(title, is_tty))
        else:
            line.append(cl.apply(title, is_tty))

        line.append(cl.apply(f"{ans:<14}", is_tty))     # column 3: answer
        line.append(cl.apply(f"{rc:^9}", is_tty))       # column 4: result

        # column 5: time cost
        if self.has_result():
            total_timeout = timeout + self.timeout_ext
            cost, style = _make_time_cost(self.time_cost, total_timeout)
            if is_best:
                line.append(style.bold().background().apply(cost, is_tty))
            else:
                line.append(style.apply(cost, is_tty))
        else:
            line.append(Style.cyan().apply(f"{'-':^12}", is_tty))

        # note: timeout extra
        extra = ""
        if self.timeout_ext > 0.0:
            if self.has_result() and self.time_cost < timeout:
                extra_colour = Style.green().bold().background()
            else:
                extra_colour = Style.yellow().bold()

            extra = extra_colour.apply(f" [+ {self.timeout_ext:.0f} ms]", is_tty)

        return _make_line(*line) + extra


def _make_time_cost(time_cost_ms: float, max_timeout_ms: float) -> tuple[str, Style]:
    if time_cost_ms < 0.01:
        return f">>  {time_cost_ms*1000:.3f} µs", Style.green()

    text = f"{time_cost_ms:9.3f} ms"
    if max_timeout_ms > 0:
        prop = time_cost_ms / max_timeout_ms
        if prop < 0.1:
            style = Style.green
        elif prop < 0.2:
            style = Style.blue
        elif prop < 0.3:
            style = Style.cyan
        elif prop < 0.5:
            style = Style.yellow
        elif prop < 0.8:
            style = Style.magenta
        else:
            style = Style.red
    else:
        style = Style.green

    return text, style()


def _pattern_match(pattern: str | None, name: str) -> bool:
    if pattern is None:
        return True

    if pattern.startswith("*") or pattern.startswith("~"):
        return pattern[1:] in name

    return pattern == name


class ProblemSolver:
    """
    Base class of problem solution.
    """

    methods: Mapping[str, SolutionMethod]
    pid: int
    answer: int | None = None
    module_name: str = ""
    timeout_ext: dict[str, float] = {"*": 0.0}
    use_extra_timeout_map: bool = False
    has_extra_data: str = ""
    __doc__ = ""

    def __init__(self, pid: int, module_name: str):
        self.module_name = module_name
        self.pid = pid
        self.answer = None
        self._method_index = []
        self.methods = {}
        self.title = ""
        self.content = ""
        self.timeout_ext = {"*": 0.0}

    def set_document(self, doc: str):
        """
        Set document of this problem.
        """
        self.__doc__ = doc
        lines = doc.strip().split("\n")
        if len(lines) < 2:
            raise RuntimeError("Invalid document format")

        self.title = lines[0].strip()
        self.content = "\n".join(lines[1:]).strip()

    def add_method(self, func: Callable[[], int], name: str, note: str = ""):
        """
        Add a solution method.
        """
        if name in self.methods:
            raise RuntimeError(f"Method {name} already exists")

        method = SolutionMethod(self.module_name, func, name, note)
        method.timeout_ext = self.get_extra_timeout(name)
        self.methods[name] = method
        self._build_index()

    def _build_index(self):
        methods = [(m.title, m.name) for m in self.methods.values()]
        methods.sort()
        self._method_index = [name for _, name in methods]

    def each_methods(self) -> Iterator[tuple[str, SolutionMethod]]:
        """
        Iterate all methods.
        """
        for name in self._method_index:
            yield name, self.methods[name]

    def get_extra_timeout(self, method_name: str) -> float:
        """
        Get extra timeout for a method.
        """
        if not self.use_extra_timeout_map:
            return max(self.timeout_ext.values())

        if method_name in self.timeout_ext:
            return self.timeout_ext[method_name]

        for key, et in self.timeout_ext.items():
            if not key.startswith("*"):
                continue

            pattern = key[1:]
            if pattern in method_name:
                return et

        if "*" in self.timeout_ext:
            return self.timeout_ext["*"]

        return 0.0

    def update_all_extra_timeout(self):
        """
        Update extra timeout for all methods.
        """
        for name, method in self.each_methods():
            method.timeout_ext = self.get_extra_timeout(name)

    def get_total_timeout(self, basic_timeout: float) -> float:
        """
        Get total timeout for this problem.
        """
        total_timeout = 0.0
        for name, _ in self.each_methods():
            timeout_ext = self.get_extra_timeout(name)
            total_timeout += basic_timeout + timeout_ext

        return total_timeout

    def _is_correct(self) -> bool:
        """
        Is the solution correct, should have at less one correct result.
        """
        result = False
        for method in self.methods.values():
            if method.is_timeout():
                continue

            if not method.has_result():
                continue

            if self.answer is not None and method.result != self.answer:
                result = result or False
                continue

            result = result or True

        return result

    def _is_all_correct(self) -> bool:
        """
        Is all methods correct.
        """
        has_correct = False
        for method in self.methods.values():
            if method.is_timeout():
                continue

            if method.result is None:
                continue

            if self.answer is not None and method.result != self.answer:
                return False

            has_correct = True

        return has_correct

    def is_correct(self, strict: bool = False) -> bool:
        """
        Is the solution correct.
        """
        if self.answer is None:
            return False

        if strict:
            return self._is_all_correct()

        return self._is_correct()

    def find_best_solution(self, check: bool = False) -> str:
        """
        Find the best solution.
        """
        cost = None
        best = None
        if self.answer is None:
            return None

        for name, method in self.each_methods():
            if method.is_timeout():
                continue

            if method.result is None:
                continue

            if check and self.answer is not None and method.result != self.answer:
                continue

            if cost is None or method.time_cost < cost:
                cost = method.time_cost
                best = name

        return best

    def print(
        self, timeout: float = 0.0, time_cost: float = 0.0,
        check: bool = False, strict: bool = False, is_tty: bool = False
    ) -> str:
        """
        Print result of a problem solver.
        """
        lines = []

        answer = self.answer
        if not check:
            answer = None

        out_pid_raw = f"{self.pid:>4}"
        out_title_raw = f"{self.title:<40}"
        best = self.find_best_solution(check=check)

        total_timeout = self.get_total_timeout(timeout)

        if len(self.methods) > 1:
            total_cost_ms = 0.0
            for name, method in self.each_methods():
                is_best = name == best
                if is_best:
                    title = f"* {method.title or 'default':<38}"
                else:
                    title = f"+ {method.title or 'default':<38}"
                line = method.print("", title, answer=answer, is_best=is_best,
                                    timeout=timeout, is_tty=is_tty)
                lines.append(line)
                total_cost_ms += method.time_cost

            overhead_ms = time_cost - total_cost_ms
            _, overhead_style = _make_time_cost(overhead_ms, timeout)
            overhead = overhead_style.apply(f" +~> {overhead_ms:.3f} ms", is_tty)
            cost, cost_style = _make_time_cost(time_cost, total_timeout)
            cost_text = cost_style.apply(cost, is_tty)
            answer_empty = " " * 30

            result_style = Style()
            correct = "unknown"
            if check:
                if self.is_correct(strict=strict):
                    result_style = Style.green()
                    correct = "correct"
                else:
                    result_style = Style.red()
                    correct = "wrong"
            out_pid = result_style.apply(out_pid_raw, is_tty)
            out_title = result_style.apply(out_title_raw, is_tty)
            out_correct = result_style.apply(f"{correct:^9}", is_tty)
            line = _make_line(out_pid, out_title, answer_empty, out_correct, cost_text)
            lines.insert(0, line + overhead)

        elif len(self.methods) == 1:
            method = list(self.methods.values())[0]
            is_best = best == method.name
            line = method.print(out_pid_raw, out_title_raw, answer=answer, is_best=is_best,
                                timeout=timeout, is_tty=is_tty)
            lines.append(line)

        else:
            red = Style.red().bold().background()
            line = _make_line(red.apply(out_pid_raw, is_tty), red.apply(out_title_raw, is_tty),
                              red.apply(f"{'NO SOLUTION':^30}", is_tty),
                              red.apply(f"{'-':^9}", is_tty), red.apply(f"{'-':^12}", is_tty))
            lines.append(line)

        return "\n".join(lines)

    def solve(self, runner: Runner, conf: RunConfigure, pattern: str = None) -> float:
        """
        Solve the problem.
        """
        t1 = datetime.now()
        for key, method in self.each_methods():
            if pattern is not None and not _pattern_match(pattern, key):
                continue

            params = {}
            if conf.timeout > 0.0:
                params["timeout"] = conf.timeout
            method.solve(runner, conf=conf, **params)

        t2 = datetime.now()
        dtms = (t2 - t1).total_seconds() * 1000.0

        data.reset()
        return dtms


def _return_zero() -> int:
    return 0


class Job:
    """
    Run job
    """

    def __init__(self, module_name: str, func: Callable[[], int]):
        self.func = func
        self.module_name = module_name
        self.preload = True

    def run(self) -> tuple[int, float]:
        """
        Run function
        """
        data.try_preload(self.module_name)
        if not self.preload:
            data.reset()

        result = _NotRunResult()
        time_start = time.perf_counter()
        try:
            result = self.func()
            time_finish = time.perf_counter()
            dt = 1000.0 * (time_finish - time_start)
            return result, dt

        except KeyboardInterrupt:
            return result, 0.0


class Runner:
    """
    Runner of all problem solvers, with managed process pool.
    """

    pool: multiprocessing.Pool

    def __init__(self):
        self.pool = None
        self.debug = False

    def close(self) -> None:
        """
        Close the process pool.
        """
        if self.pool is not None:
            self.pool.terminate()
            self.pool.close()
            self.pool = None

    def reset_pool(self) -> None:
        """
        Reset the process pool.
        """
        self.close()
        self.pool = multiprocessing.Pool(processes=1)
        self.run_func(
            "", _return_zero, _default_run_configure
        )  # warm up worker process

    def run_func_in_process(
        self, name: str, func: Callable[[], int], conf: RunConfigure, timeout: float = 0.0
    ) -> tuple[int, bool, float]:
        """
        Run a function in process.
        """
        job = Job(name, func)
        job.preload = conf.preload

        is_timeout = False
        result = _NotRunResult()
        time_start = time.perf_counter()
        get_params = {}
        if timeout > 0.0:
            get_params["timeout"] = timeout / 1000.0

        try:
            r = self.pool.apply_async(job.run)
            result, dt = r.get(**get_params)

        except multiprocessing.TimeoutError:
            time_finish = time.perf_counter()
            result = _TimeoutResult()
            dt = 1000.0 * (time_finish - time_start)
            self.reset_pool()
            is_timeout = True

        return result, is_timeout, dt

    def run_func(
        self, name: str, func: Callable[[], int], conf: RunConfigure, timeout: float = 0.0
    ) -> tuple[int, bool, float]:
        if not self.debug:
            return self.run_func_in_process(name, func, conf, timeout)

        time_start = time.perf_counter()
        result = func()
        time_finish = time.perf_counter()
        dt = 1000.0 * (time_finish - time_start)
        return result, False, dt


def _natural_filename(filename: str) -> Iterable[str | int]:
    parts = []
    i = 0
    buf, flag = [], "char"
    while i < len(filename):
        c = filename[i]
        cf = "digit" if c.isdigit() else "char"
        if cf != flag:
            n = "".join(buf)
            if flag == "digit":
                n = int(n)

            parts.append(n)
            flag = cf
            buf = []

        buf.append(c)
        i += 1

    if len(buf) > 0:
        n = "".join(buf)
        if flag == "digit":
            n = int(n)

        parts.append(n)

    return parts


def import_solver(module_name: str, base_name: str) -> ProblemSolver:
    """
    Import a problem solver.
    """
    mod = importlib.import_module(f"{module_name}")
    try:
        pid = int(base_name[1:])

    except ValueError as ex:
        raise ValueError(
            f"Invalid problem name: '{base_name}', "
            + "should be pXXXX which XXXX is a number"
        ) from ex

    solver = ProblemSolver(pid, base_name)
    solver.set_document(mod.__doc__)

    if hasattr(mod, "ANSWER"):
        solver.answer = mod.ANSWER

    if hasattr(mod, "TIMEOUT_EXT"):
        if isinstance(mod.TIMEOUT_EXT, (int, float)):
            solver.timeout_ext = {"*": float(mod.TIMEOUT_EXT)}
        else:
            solver.timeout_ext = mod.TIMEOUT_EXT

    for name, func in inspect.getmembers(mod, inspect.isfunction):
        # inspect.getmembers() returns all members sorted by name
        if name == "solve":
            solver.add_method(func, "", func.__doc__)

        elif len(name) > 6 and name.startswith("solve_"):
            solver.add_method(func, name[6:], func.__doc__)

        else:
            continue

    return solver


def check_extra_data(module_name: str) -> bool:
    """
    Check if there is extra data for a problem.
    """
    try:
        mod = importlib.import_module(f"{module_name}")
        if not hasattr(mod, "load"):
            return False

        return True

    except ImportError:
        return False


def find_problem_solvers(
    dirname: str, id_list: Iterable[ProblemId] = None
) -> Iterator[tuple[ProblemId | None, ProblemSolver]]:
    """
    Find all problem solvers in given directory.
    """
    target_dir = f"{dirname}"

    id_map = {pid.pid: pid for pid in (id_list or [])}
    if id_list is not None and len(id_list) > 0:
        file_list = [f"{pid.problem_name()}.py" for pid in id_list]
    else:
        file_list = os.listdir(target_dir)

    file_natural_list = [
        (filename, _natural_filename(filename)) for filename in file_list
    ]
    file_natural_list.sort(key=lambda x: x[1])
    for filename, _ in file_natural_list:
        if not filename.endswith(".py"):
            continue

        base_name = filename[0:-3]
        if base_name == "__init__":
            continue

        package_name = dirname.replace("/", ".")
        module_name = f"{package_name}.{base_name}"
        data_name = base_name

        try:
            solver = import_solver(module_name, base_name)
            id_selector = id_map.get(solver.pid, None)
            if len(id_map) > 0 and id_selector is None:
                continue

            if check_extra_data(data_name):
                solver.has_extra_data = data_name

            yield id_selector, solver

        except ImportError as ex:
            print(f"Failed to import {module_name}: {ex}")

        except SyntaxError as ex:
            print(f"Syntax error in {module_name}/{filename}: {ex}")


def do_list(id_list: Iterable[ProblemId], full: bool, show_missing: bool):
    """
    List problems.
    """
    last = None
    for _, problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        if show_missing and last is not None and problem.pid - last > 1:
            if problem.pid - last == 2:
                print(f"...   {last + 1}")
            else:
                print(f"...   {last + 1} ~ {problem.pid - 1}")

        last = problem.pid

        print(f"{problem.pid:<5d} {problem.title}")
        if full:
            print(_add_indent(problem.content, "      "))
            print()


def do_create(id_list: Iterable[int]):
    """
    Create solution of a problem.
    """
    for pid in id_list:
        filename = f"p{pid:04d}.py"
        filepath = os.path.join(PROBLEM_DIR, filename)
        if os.path.exists(filepath):
            print(f"File {filepath} already exists")
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(
                "#!/usr/bin/env python3\n"
                "# coding: utf-8\n"
                "\n"
                "\n"
                '"""\n'
                "Problem title\n"
                "\n"
                "Problem description\n"
                '"""\n'
                "\n"
                "\n"
                "ANSWER = None\n"
                "\n"
                "\n"
                "def solve() -> int:\n"
                "    return 0\n"
            )

OUTPUT_SEPLINE = "".join(["+",
    "-" * (4 + 2) + "+",    # PID
    "-" * (40 + 2) + "+",   # Title
    "-" * (30 + 2) + "+",   # Answer
    "-" * (9 + 2) + "+",    # Result
    "-" * (12 + 2) + "+",   # Time cost
])

def do_run(conf: RunConfigure):
    """
    Run problems.
    """
    runner = Runner()
    runner.debug = conf.debug
    runner.reset_pool()

    retcode = 0
    success, count, methods = 0, 0, 0
    time_start = datetime.now()
    is_tty = sys.stdout.isatty() or conf.colour

    print(OUTPUT_SEPLINE)
    print(f"| {'PID':>4} | {'Title / Solution':<40} "
          f"| {'Answer':^30} | {'Result':^9} | {'Time':^12} |")
    print(OUTPUT_SEPLINE)

    try:
        for selector, problem in find_problem_solvers(PROBLEM_DIR, id_list=conf.id_list):
            name = None
            if selector is not None:
                name = selector.method

            problem.use_extra_timeout_map = conf.extra_timeout_map
            problem.update_all_extra_timeout()

            cost = problem.solve(runner, conf=conf, pattern=name)
            line = problem.print(timeout=conf.timeout, time_cost=cost,
                                 check=conf.check, strict=conf.strict, is_tty=is_tty)
            if conf.check:
                if problem.is_correct(strict=conf.strict):
                    success += 1
                else:
                    retcode = 1

            print(line)
            count += 1
            methods += len(problem.methods)

    except KeyboardInterrupt:
        print("Interrupted by user")
        retcode = 1

    finally:
        time_finish = datetime.now()
        print(OUTPUT_SEPLINE)

        dt = (time_finish - time_start).total_seconds()
        if conf.check:
            print(f"Solved {success}/{count} problems in {dt:.3f}s")
        else:
            print(f"Solved {count} problems solved in {dt:.3f}s")

        runner.close()

    sys.exit(retcode)


def main():
    """
    Main entry.
    """
    parser = _get_parser()
    args = parser.parse_args()

    if args.command == "list":
        do_list(args.id, args.full, args.show_missing)

    elif args.command == "create":
        do_create(args.id)

    elif args.command == "run":
        conf = RunConfigure.from_parser(args)
        do_run(conf)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
