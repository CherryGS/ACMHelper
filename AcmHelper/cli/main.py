import os
import subprocess
from dataclasses import asdict
from enum import Enum
from itertools import chain, filterfalse
from pathlib import Path
from time import perf_counter

import typer
import yaml
from loguru import logger

from .config import *


def load_config() -> Config:
    try:
        f = open(pth / "config.yaml", "r")
        c = yaml.load(f, yaml.FullLoader)
        c = Config(**c)
        if c.std == False:
            raise NotImplementedError()
        return c
    except:
        logger.error("Get error when load config.yaml.")
        raise typer.Exit(1)


@app.command()
def init():
    """Init a problem with base files."""
    if list(pth.iterdir()) != []:
        logger.error("Folder is not empty.")
        raise typer.Exit(1)
    typer.confirm("Please copy 'testlib.h' into root folder.")
    for i in new_dir:
        os.makedirs(i)
    init_config()
    l = ["std.cpp", "checker.cpp", "interactor.cpp", "validator.cpp"]
    for i in l:
        with open(pth / i, "w"):
            pass


@app.command()
def run():
    """Generate data.(Overwrite)"""
    logger.add(log)
    logger.info("Start.")

    logger.info("Loading config.")
    c = load_config()

    logger.info("Collecting info.")
    l = ["std", "checker", "interactor", "validator"]

    std = MyFile(pth, "std")
    chc = MyFile(pth, "checker")
    ine = MyFile(pth, "interactor")
    vai = MyFile(pth, "validator")

    gen = [MyFile(gen_path, i) for i in c.gen_list]
    ac = [MyFile(ac_code_path, i) for i in c.accept_list]
    wa = [MyFile(wa_code_path, i) for i in c.warong_list]

    logger.info("Compiling...")
    s = perf_counter()
    [i.compile(c) for i in chain(gen, ac, wa, [std, chc, ine, vai])]
    logger.info(f"Compile all files in {perf_counter()-s:.3} seconds.")

    logger.info("Generate data sets.")
    data_cnt = 1
    for i in gen:
        for _ in range(c.gen_data_num[i.stem]):
            data = IO(data_cnt)
            data_cnt += 1
            o = i.run(c)
            # TODO: Validate input
            data.w_input(i, o)
            for j in chain(ac, wa):
                if j.stem in c.gen_link_code[i.stem]:
                    data.w_input(j, j.run(c, o))

    logger.info("Finished.")


@app.command()
def qrun():
    print(pth)


@app.command("odata")
def output_data():
    """Restructure data sets."""


@app.command()
def init_config():
    """Init config"""
    logger.add(log)
    res = True
    if os.path.exists(pth / "config.yaml"):
        res = typer.confirm("Override the current config?")
    if res:
        logger.warning("Config is overwritten.")
        with open(pth / "config.yaml", "w") as f:
            yaml.dump(asdict(Config()), f)


@app.command()
def clear():
    """Clear exe."""
    raise NotImplementedError("test")


class MyFile:
    def __init__(self, path: Path, name: str) -> None:
        res = list(filterfalse(lambda x: name != x.stem, path.iterdir()))
        if len(res) > 1:
            raise ValueError(f"Duplicated files {res}.")
        elif len(res) == 0:
            raise ValueError(f"Path {path} doesn't have target file.")
        self.file = res[0]
        self.exec_path: Path | None = None
        self.exec_cmd: str = ""
        self._link()
        self.stem = self.file.stem

    def _link(self):
        file = self.file
        if file.suffix == ".py":
            self.exec_cmd = "python"

    def _in(self, cnt: int):
        return data_auto_in / f"{cnt}.{self.file.stem}.in"

    def _out(self, cnt: int):
        return data_auto_out / f"{cnt}.{self.file.stem}.out"

    def compile(self, c: Config):
        file = self.file
        if file.suffix == ".cpp":
            res = subprocess.run(
                f"g++ -std=c++17 -O2 -Wall {file} -o {exec_path/file.stem}.exe",
                timeout=c.max_time_limit,
                capture_output=True,
            )
            if res.stderr is not None:
                raise ValueError(f"Got err when compiling {self.exec_path}")
            self.exec_path = exec_path / (file.stem + ".exe")
        else:
            self.exec_path = file

    def run(self, c: Config, input: str = ""):
        if self.exec_path is None:
            raise ValueError("Empty exec path.")
        cmd = f"{self.exec_cmd} {self.exec_path}"
        res = subprocess.run(
            cmd,
            timeout=c.max_time_limit,
            input=input,
            encoding="utf8",
            capture_output=True,
        )
        o, e = [res.stdout, res.stderr]
        if e is not None:
            raise ValueError(f"Got err when running {self.exec_path}")
        return o


class IO:
    def __init__(self, cnt: int) -> None:
        self.cnt = cnt

    def w_input(self, file: MyFile, o: str):
        with open(file._in(self.cnt), "w") as f:
            f.write(o)

    def w_output(self, file: MyFile, o: str):
        with open(file._out(self.cnt), "w") as f:
            f.write(o)


class Status(Enum):
    wa = "Wrong Anwser"
    ac = "Accept"
    tle = "Time Limited Exceeded."
