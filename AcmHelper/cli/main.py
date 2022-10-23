import typer
import subprocess


def main(test: str, test1: int = 123, flag: bool = False):
    print(test)


# nono

if __name__ == "__main__":
    typer.run(main)
