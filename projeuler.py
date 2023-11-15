#!/usr/bin/env python3
# coding: utf-8


"""
Main entry, runner of all problem solutions.
"""


import os
import importlib
import argparse
from typing import (
    Callable,
    Generator,
    List,
)
from datetime import datetime


PROBLEM_DIR = "problems"


def _get_parser():
    parser = argparse.ArgumentParser(description="Project Euler problem runner")

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    cmd_list = subparsers.add_parser("list", help="list all problems")
    cmd_list.add_argument(
        "-f", "--full", action="store_true", help="show full information"
    )
    cmd_list.add_argument(
        "id", nargs="*", type=int, help="show specific problem information"
    )

    cmd_run = subparsers.add_parser("run", help="run problems")
    cmd_run.add_argument(
        "-c", "--check", action="store_true", help="check the solution answer"
    )
    cmd_run.add_argument(
        "id", nargs="*", type=int, help="run specific problems"
    )

    return parser


def _add_indent(s: str, indent: str) -> str:
    lines = s.split("\n")
    result = [indent + line for line in lines]
    return "\n".join(result)


class ProblemSolver:
    """
    Base class of problem solution.
    """

    __doc__ = ""

    def __init__(self, pid: int, answer: int, solve: Callable[[], int]):
        self.pid = pid
        self.answer = answer
        self.solve = solve
        self.title = ""
        self.content = ""

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


def find_problem_solvers(
    dirname: str, id_list: List[int] = None
) -> Generator[ProblemSolver, None, None]:
    """
    Find all problem solvers in given directory.
    """
    target_dir = f"{dirname}"

    id_set = set(id_list or [])
    for filename in os.listdir(target_dir):
        if not filename.endswith(".py"):
            continue

        base_name = filename[0:-3]
        if base_name == "__init__":
            continue

        package_name = dirname.replace("/", ".")
        module_name = f"{package_name}.{base_name}"

        try:
            mod = importlib.import_module(f"{module_name}")
            attrs = ["PID", "ANSWER", "solve"]
            for attr in attrs:
                if not hasattr(mod, attr):
                    raise RuntimeError(f"Missing attribute {attr} in {module_name}")

            solver = ProblemSolver(mod.PID, mod.ANSWER, mod.solve)
            solver.set_document(mod.__doc__)

            if len(id_set) > 0 and solver.pid not in id_set:
                continue

            yield solver

        except ImportError as ex:
            print(f"Failed to import {module_name}: {ex}")

        except SyntaxError as ex:
            print(f"Syntax error in {module_name}/{filename}: {ex}")


def do_list(id_list: List[int], full: bool):
    """
    List problems.
    """
    for problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        print(f"{problem.pid:<5d} {problem.title}")
        if full:
            print(_add_indent(problem.content, "      "))
            print()


def do_run(id_list: List[int], check: bool):
    """
    Run problems.
    """
    for problem in find_problem_solvers(PROBLEM_DIR, id_list=id_list):
        time_start: datetime
        time_finish: datetime

        time_start = datetime.now()

        answer = problem.solve()
        if answer is None:
            print(f"{problem.pid:<5d} {problem.title:.<30} no answer returned")
            return

        time_finish = datetime.now()

        line = [
            f"{problem.pid:<5d} {problem.title:.<30} {answer:<10d}"
        ]

        if check:
            if problem.answer is None:
                result = "not set"
            elif problem.answer == answer:
                result = "correct"
            else:
                result = "wrong"
            line.append(f" {result:8}")

        dt = 1000.0 * (time_finish - time_start).total_seconds()
        line.append(f" {dt:.3f}ms")

        print("".join(line))


def main():
    """
    Main entry.
    """
    parser = _get_parser()
    args = parser.parse_args()

    if args.command == "list":
        do_list(args.id, args.full)

    elif args.command == "run":
        do_run(args.id, args.check)


if __name__ == "__main__":
    main()
