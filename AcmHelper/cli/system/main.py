import json
import os
import shutil
import zipfile as zip
from dataclasses import asdict
from itertools import chain
from time import perf_counter

import typer
from loguru import logger

from .config import *
from .utils import *


def load_config() -> Config:
    try:
        f = open(pth / "config.json", "r")
        c = json.load(f)
        c = Config(**c)
        if c.std == False:
            raise NotImplementedError()
        return c
    except:
        logger.error("Get error when load config.json.")
        raise typer.Exit(1)


@app.command()
def init():
    """Init a problem with base files."""
    if list(pth.iterdir()) != []:
        logger.error("Folder is not empty.")
        raise typer.Exit(1)
    for i in new_dir:
        os.makedirs(i)
    init_config()
    if typer.confirm("Copy 'testlib.h' ?"):
        shutil.copy(default_path / "testlib.h", pth / "testlib.h")
    l = ["std.cpp", "checker.cpp", "interactor.cpp", "validator.cpp"]
    for i in l:
        shutil.copy(default_path / f"template_{i}", pth / f"{i}")


@app.command()
def run(
    strict: bool = typer.Option(
        False,
        help="If it's enabled, the process will be interrupted when program gets invalid returncode.",
    ),
    save: bool = typer.Option(
        False, help="Run in save folder without generating new testcase."
    ),
    table: bool = typer.Option(
        True, help="Print the table of generation result if enable."
    ),
    rich: bool = typer.Option(
        True, help="Show rich information by rich.(No implement.)"
    ),
):
    """Generate data.(Overwrite)"""
    logger.add(log)
    logger.info("Start.")

    logger.info("Loading config.")
    c = load_config()

    logger.info("Collecting info.")

    std = Runner(pth, c.std)
    chc = Checker(pth, c.checker)
    ine = Interactor(pth, c.interactor)
    vai = Validator(pth, c.validator)

    gen = [Runner(gen_path, i) for i in c.gen_list]
    ac = [Runner(ac_code_path, i) for i in c.accept_list]
    wa = [Runner(wa_code_path, i) for i in c.wrong_list]

    logger.info("Compiling...")
    s = perf_counter()
    [i.compile(c) for i in chain(gen, ac, wa, [std, chc, ine, vai])]
    logger.info(f"Compile all files in {perf_counter()-s:.3} seconds.")

    logger.info("Generating data sets...")
    data_cnt = 1
    data_set: list[Path] = list()
    used_time: dict[tuple[str, str], int | float] = dict()
    for i in gen:
        logger.info(f"Using generator {i}...")
        for _ in range(c.gen_data_num[i.stem]):
            logger.info(f"Test case {data_cnt}.")
            data = IO(data_cnt)
            data_set.append(i.f_in(data_cnt))
            data_cnt += 1
            o = i.run(c)[0]
            # TODO: Validate input
            data.w_input(i, o)
            for j in chain(ac, wa, [std]):
                if j.stem in c.gen_link_code[i.stem]:
                    res = j.run(c, o)
                    data.w_output(j, res[0])
                    used_time[(i.stem, j.stem)] = res[1]
    info: dict[str, dict[str, int]] = dict()
    # TODO: Simplify
    for n in range(1, data_cnt):
        d = data_set[n - 1]
        r = d.name.split(".")[1]
        info[d.name] = {}
        logger.info(f"Running test case {d.name}")
        for i in ac:
            if i.stem not in c.gen_link_code[r]:
                info[d.name][i.stem] = Status._ign
                continue
            res = chc.check(d, i.f_out(n), std.f_out(n), c)
            info[d.name][i.stem] = res[0]
            if strict:
                if res[0] != Status._ok:
                    raise ValueError(
                        f"In Test {n}, accept code got error {Status(res[0]).name}. Info: {res[1]}. "
                    )
            if res[0] == Status._ok and used_time.get((r, i.stem), 0) >= c.time_limit:
                info[d.name][i.stem] = Status._tle
        for i in wa:
            if i.stem not in c.gen_link_code[r]:
                info[d.name][i.stem] = Status._ign
                continue
            res = chc.check(d, i.f_out(n), std.f_out(n), c)
            info[d.name][i.stem] = res[0]
            if strict:
                if res[0] == Status._fail:
                    raise ValueError(
                        f"In Test {n}, wrong code got error {Status(res[0]).name}. Info: {res[1]}. "
                    )
            if res[0] == Status._ok and used_time.get((r, i.stem), 0) >= c.time_limit:
                info[d.name][i.stem] = Status._tle
    logger.info("Rendering the result...")
    if table:
        print_run_status([i.stem for i in chain(ac, wa)], info)
    logger.info("Finished.")


@app.command("btf")
def beautify_data():
    """Renumber the data sets in save folder(from 1)."""
    raise NotImplementedError()


@app.command("output")
def output_data(spj: str = typer.Argument("", help="The name of checker you need.")):
    """Rename and zip data(in save folder). Zipped file will be in output folder."""
    sav: dict[str, int] = dict()
    cnt = 1
    c = load_config()
    f = zip.ZipFile(temp_path / "data.zip", "w")
    for i in data_save_in.iterdir():
        idx = i.name.split(".")[0]
        if idx in sav:
            raise ValueError("Duplicated input file.")
        sav[idx] = cnt
        f.write(i, f"{cnt}.in")
        cnt += 1
    for i in data_save_out.iterdir():
        [idx, fr] = i.name.split(".")[0:2]
        if fr != "std":
            continue
        if idx not in sav:
            raise ValueError(f"Std output {idx} has not input file.")
        f.write(i, f"{sav[idx]}.out")
        sav.pop(idx)
    if len(sav) != 0:
        raise ValueError(f"Input file {sav.keys()} has not std output.")
    if c.checker:
        chc = Checker(pth, c.checker)
        f.write(chc.file, f"{spj if spj else chc.file.name}")
    shutil.copy(temp_path / "data.zip", outp_path / "data.zip")
    f.close()


@app.command("add")
def add_data(
    lis: list[int] = [],
    all: bool = typer.Option(True, "--all", "-a", help="Add all test cases."),
):
    """Add data from auto to save"""
    num = max([int(i.name.split(".")[0]) for i in list(data_save_in.iterdir())] + [0])
    for i in data_auto_in.iterdir():
        idx = int(i.name.split(".")[0])
        if all or idx in lis:
            new = i.name.split(".")
            new[0] = str(int(new[0]) + num)
            des = data_save_in / ".".join(new)
            old_std = data_auto_out / f"{idx}.std.out"
            new_std = data_save_out / f"{new[0]}.std.out"
            shutil.copy(i, des)
            shutil.copy(old_std, new_std)
            logger.info(f"Move {i.relative_to(pth)} to {des.relative_to(pth)}")
            logger.info(
                f"Move {old_std.relative_to(pth)} to {new_std.relative_to(pth)}"
            )


@app.command()
def init_config():
    """Init config"""
    logger.add(log)
    res = True
    if os.path.isfile(pth / "config.json"):
        res = typer.confirm("Override the current config?")
        if res:
            logger.warning("Config is overwritten.")
        else:
            logger.info("Interrupted.")
            raise typer.Exit()
    if res:
        with open(pth / "config.json", "w") as f:
            json.dump(asdict(Config()), f)
