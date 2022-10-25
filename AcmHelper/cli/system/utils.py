import subprocess
from enum import IntEnum
from itertools import filterfalse
from time import perf_counter

from rich import print
from rich.console import Console
from rich.table import Table

from .config import *


class MyFile:
    def __init__(self, path: Path, name: str) -> None:
        res = list(filterfalse(lambda x: name != x.stem, path.iterdir()))
        if len(res) > 1:
            raise ValueError(f"Duplicated files {res}.")
        elif len(res) == 0:
            raise ValueError(f"Path {path} doesn't have target file.")
        self.file = res[0]
        self.exec_cmd: str = ""
        self.exec_path = None
        self.stem = self.file.stem
        self._calc_suffix()
        # self._link_to_exec()

    def __repr__(self) -> str:
        return f"{self.file}"

    def _calc_suffix(self):
        file = self.file
        if file.suffix == ".py":
            self.exec_cmd = "python"

    def _link_to_exec(self):
        ext = self.file.suffix
        if ext == ".py":
            self.exec_path = self.file
        elif ext == ".cpp":
            self.exec_path = exec_path / f"{self.file.stem}.exe"
            if not self.exec_path.is_file():
                self.exec_path = None

    def f_in(self, cnt: int):
        return data_auto_in / f"{cnt}.{self.file.stem}.in"

    def f_out(self, cnt: int):
        return data_auto_out / f"{cnt}.{self.file.stem}.out"

    def compile(self, c: Config) -> bool:
        if self.exec_path:
            return False
        file = self.file
        if file.suffix == ".cpp":
            res = subprocess.run(
                f"g++ -std=c++{c.gcc_version} -O2 -Wall {file} -o {exec_path/file.stem}.exe ",
                timeout=c.max_time_limit,
                encoding="utf8",
                capture_output=True,
            )
            e = res.stderr
            if e or res.returncode != 0:
                print(e) if e else ...
                raise ValueError(f"Got err when compiling {file}")
            self.exec_path = exec_path / (file.stem + ".exe")
        else:
            self.exec_path = file
        return True


class Runner(MyFile):
    def run(self, c: Config, input: str = ""):
        if not self.exec_path:
            raise ValueError("Empty exec path.")
        cmd = f"{self.exec_cmd} {self.exec_path}".strip()
        t = perf_counter()
        res = subprocess.run(
            cmd,
            timeout=c.max_time_limit,
            input=input,
            encoding="UTF-8",
            capture_output=True,
        )
        t = perf_counter() - t
        o, e = res.stdout, res.stderr
        if e or res.returncode != 0:
            print(e) if e else ...
            raise ValueError(f"Got err when running {self.exec_path}")
        return (o, t)


class Checker(MyFile):
    def __init__(self, path: Path = Path("."), name: str = "") -> None:
        if not name:
            super().__init__(default_path, "checker")
        else:
            super().__init__(path, name)

    def check(self, input: Path, output: Path, ans: Path, c: Config):
        if self.exec_path is None:
            raise ValueError("Empty exec path.")
        cmd = f"{self.exec_cmd} {self.exec_path} {input} {output} {ans}".strip()
        res = subprocess.run(
            cmd,
            timeout=c.max_time_limit,
            encoding="utf8",
            capture_output=True,
        )
        e, r = res.stderr, res.returncode
        return (r, e)


class Validator(MyFile):
    def __init__(self, path: Path = Path("."), name: str = "") -> None:
        if not name:
            super().__init__(default_path, "validator")
        else:
            super().__init__(path, name)


class Interactor(MyFile):
    def __init__(self, path: Path = Path("."), name: str = "") -> None:
        if not name:
            super().__init__(default_path, "interactor")
        else:
            super().__init__(path, name)


class IO:
    def __init__(self, cnt: int) -> None:
        self.cnt = cnt

    def w_input(self, file: MyFile, o: str):
        with open(file.f_in(self.cnt), "w") as f:
            f.write(o)

    def w_output(self, file: MyFile, o: str):
        with open(file.f_out(self.cnt), "w") as f:
            f.write(o)

    def r_input(self, file: MyFile, o: str):
        with open(file.f_in(self.cnt), "r") as f:
            return f.read()

    def r_output(self, file: MyFile, o: str):
        with open(file.f_out(self.cnt), "r") as f:
            return f.read()


class Status(IntEnum):
    passed = 0
    unpassed = 1
    sys_fail = 3
    tle = 20
    ignore = 21


def print_run_status(col: list[str], data: dict[str, dict[str, int]]):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Test data")
    for i in col:
        table.add_column(i)
    for i in data:
        r = data[i]
        lis = [i]
        for j in r:
            e = data[i][j]
            if e == Status.passed:
                lis.append("🟢")
            elif e == Status.unpassed:
                lis.append("🔴")
            elif e == Status.tle:
                lis.append("⛔")
            elif e == Status.ignore:
                lis.append("🏳️")
            elif e == Status.sys_fail:
                lis.append("❗")
            else:
                lis.append("❓")
        table.add_row(*lis)
    console = Console()
    console.print(table)
