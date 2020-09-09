import logging
import traceback
from concurrent import futures
from pathlib import Path
import coloredlogs
from subprocess import check_output, TimeoutExpired, STDOUT

level = logging.INFO
logging.basicConfig(level=level)
coloredlogs.install(level=level)
logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).absolute().parents[2]
DATASETS_PATH = BASE_PATH / "res" / "datasets" / "cordeau-laporte"
INSTANCE_TIMEOUT = 7200


def main():
    with futures.ProcessPoolExecutor() as executor:
        for file_path in DATASETS_PATH.glob("*.txt"):
            executor.submit(run_one, file_path)


def run_one(file_path):
    try:
        command = ["python3", "benchmark_solve.py", str(file_path.absolute())]
        print(f'COMMAND: "{" ".join(command)}"')
        try:
            output = check_output(
                command,
                timeout=INSTANCE_TIMEOUT,
                stderr=STDOUT,
                cwd=Path(__file__).parent
            ).decode()
        except TimeoutExpired as exc:
            print(exc)
            output = exc.output.decode()
        with (file_path.parent / f"{file_path.name}.log").open("w") as file:
            file.write(output)
    except Exception as exc:
        traceback.print_exc()
        raise exc


if __name__ == '__main__':
    main()
