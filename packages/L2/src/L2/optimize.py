from .constant_folding import constant_folding_term
from .constant_propagation import constant_propagation_term
from .dead_code_elimination import dead_code_elim_term
from .syntax import Program


def optimize_program(
    program: Program,
) -> Program:
    match program:
        case Program(parameters=parameters, body=body):
            newBody = body
            changes = 1

            while changes > 0:
                changes = 0
                newBody = constant_propagation_term(newBody)
                newBody = constant_folding_term(newBody)
                newBody = dead_code_elim_term(newBody)

                if newBody != body:
                    body = newBody
                    changes += 1

            return Program(parameters=parameters, body=body)
