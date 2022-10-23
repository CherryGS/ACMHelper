from dataclasses import dataclass, field
from pathlib import Path
from time import gmtime, perf_counter, strftime
import typer
import os
import yaml
import subprocess
import logging
from loguru import logger

pth: Path = Path(os.getcwd())
app = typer.Typer()
now = strftime(r"%Y-%m-%d", gmtime())
log = pth / "log" / (now + ".log")


@dataclass
class Config:
    gen_link_accept: dict[str, list[str]]
    gen_link_wrong: dict[str, list[str]]
    time_limit: float = 2
    max_time_limit: float = 10
    std: bool = True
    checker: bool = False
    interactor: bool = False
    validator: bool = False


new = {
    "time_limit": 2,
    "max_time_limit": 10,
    "std": True,
    "checker": False,
    "interactor": False,
    "validator": False,
    "gen_link_accept": {"code1.cpp": ["test1.cpp", "test2.py"]},
    "gen_link_wrong": {"code4.py": ["test1.cpp"]},
}

new_dir = [
    "generator",
    "accept",
    "wrong",
    "data/auto/in",
    "data/auto/out",
    "data/auto/wa",
    "data/hand/in",
    "data/hand/out",
    "data/hand/wa",
    "log",
]


@app.command()
def create():
    """Create a problem with base files."""
    name = typer.prompt("Problem name")
    pth1: Path = pth / name
    if pth1.exists():
        logging.error("Problem already exists.")
        raise typer.Exit(1)
    for i in new_dir:
        os.makedirs(pth1 / i)
    with open(pth1 / "config.yaml", "w") as f:
        yaml.dump(new, f)
    with open(pth1 / "std.cpp", "w"):
        pass


@app.command()
def run():
    logger.add(log)
    logger.info("Start.")
    if not os.path.exists(pth / "config.yaml"):
        logger.error("Config doesn't exist.")
        raise typer.Exit(1)

    logger.info("Loading config.")
    with open(pth / "config.yaml", "r") as f:
        c = yaml.load(f, yaml.FullLoader)
        c = Config(**c)

    logger.info("Collecting info.")
    l = ["std", "checker", "interactor", "validator"]
    cf: list[Path] = list()
    for i in l:
        if c.__getattribute__(i) == True and not os.path.exists(pth / f"{i}.cpp"):
            logger.error(f"{i[0].upper()+i[1:]} doesn't exist.")
            raise typer.Exit(1)
        if c.__getattribute__(i) == True:
            cf.append(pth / f"{i}.cpp")
    l = ["generator", "accept", "wrong"]
    t: dict[str, list[Path]] = dict()
    for j in l:
        t[j] = []
        for i in os.listdir(pth / j):
            t[j].append(pth / j / i)
            if j.split(".")[-1] == "cpp":
                cf.append(pth / j / i)

    logger.info("Compiling...")
    s = perf_counter()
    for i in cf:
        res = subprocess.run(f"g++ -std=c++17 -O2 -Wall {i} -o {str(i)[:-3]}.exe")
        if res.stderr is not None:
            logger.error(f"Got error when compile {i.name}")
            raise typer.Exit(1)
        i = i.parent / (i.name[:-3] + "exe")
    logger.info(f"Compile in {perf_counter()-s:.3} seconds.")

    logger.info("Finished.")


@app.command()
def qrun():
    print(pth)


@app.command()
def output_data():
    pass


@app.command()
def init_config():
    """Init config"""
    with open(Path(os.getcwd()) / "config.yaml", "w") as f:
        yaml.dump(new, f)


@app.command()
def clear():
    """Clear exe."""
