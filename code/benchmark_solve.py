import logging
import sys
import traceback
from functools import partial
from pathlib import Path
import coloredlogs
import jinete as jit

level = logging.INFO
logging.basicConfig(level=level)
coloredlogs.install(level=level)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting...")
    file_path = Path(sys.argv[1])
    solver = jit.Solver(
        loader_kwargs={"file_path": file_path},
        algorithm=jit.GraspAlgorithm,
        algorithm_kwargs={
            "first_solution_kwargs": {
                "episodes": 1,
                "randomized_size": 2,
            },
            "episodes": 5,
        },
        storer=jit.StorerSet,
        storer_kwargs={
            "storer_cls_set": {
                jit.PromptStorer,
                partial(
                    jit.GraphPlotStorer, file_path=file_path.parent / f"{file_path.name}.png"
                ),
                partial(
                    jit.FileStorer, file_path=file_path.parent / f"{file_path.name}.output"
                ),
            }
        },
    )
    result = solver.solve()  # noqa
    logger.info("Finished...")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        traceback.print_exc()
        raise exc
