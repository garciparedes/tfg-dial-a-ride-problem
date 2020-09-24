import jinete as jit

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
            partialjit.GraphPlotStorer, file_path=file_path.parent / f"{file_path.name}.png"),
            partial(jit.FileStorer, file_path=file_path.parent / f"{file_path.name}.output"),
        }
    },
)
result = solver.solve()