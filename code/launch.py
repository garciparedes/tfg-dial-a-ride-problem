import logging
import traceback
from concurrent import futures
from pathlib import Path
from subprocess import check_output, TimeoutExpired, STDOUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATASETS_PATH = Path(__file__).absolute().parent
INSTANCE_TIMEOUT = 7200


def main():
    with futures.ProcessPoolExecutor() as executor:
        for file_path in DATASETS_PATH.glob("*.txt"):
            executor.submit(run_one, file_path)


def run_one(file_path):
    try:
        command = ["python3", "solve.py", str(file_path.absolute())]
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
