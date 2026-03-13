from functools import partial

from .syntax import Program


def optimize_program(
    program: Program,
) -> Program:
    recur = partial(optimize_program)

    case

    return program
