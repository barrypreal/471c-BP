from collections.abc import Callable, Sequence
from functools import partial

from L0 import syntax as L0

from L1 import syntax as L1

lifted: list[L0.Procedure] = []


def free_variables(
    term: L1.Statement,
    fvs: list[L1.Identifier],
) -> Sequence[L1.Identifier]:
    for field in dir(term):
        atr = getattr(term, field)
        if atr is L1.Identifier:
            if atr not in fvs:
                fvs.extend(atr)
        elif atr is L1.Statement:
            fvs.extend(free_variables(term=atr, fvs=fvs))

    return fvs


def lift_var(
    term: L0.Procedure,
) -> None:
    lifted.append(term)


def close_term(
    statement: L1.Statement,
    lift: Callable[[L0.Procedure], None],
    fresh: Callable[[str], str],
) -> L0.Statement:
    recur = partial(close_term, lift=lift, fresh=fresh)

    match statement:
        case L1.Abstract(destination=destination, parameters=parameters, body=body, then=then):
            # 1. Close the abstract / lift to top level

            env_p = fresh("env")
            name = fresh("proc")

            fvs: list[L1.Identifier] = []

            fvs = list(set(free_variables(body, fvs)) - set(parameters))

            result = recur(body)
            for i, fv in enumerate(fvs):
                result = L0.Load(destination=fv, base=env_p, index=i, then=result)

            p = L0.Procedure(name=name, parameters=[*parameters, env_p], body=result)

            lift(p)

            # 2. Create the closure
            env = fresh("env")
            L0.Allocate(destination=env, count=len(fvs), then=recur(then))

            code = fresh("code")

            L0.Address(
                destination=code,
                name=name,
                then=L0.Allocate(
                    destination=destination,
                    count=2,
                    then=L0.Store(
                        base=destination,
                        index=0,
                        value=code,
                        then=L0.Store(base=destination, index=1, value=env, then=recur(then)),
                    ),
                ),
            )

            return L0.Allocate(destination=env, count=len(fvs), then=result)

        case L1.Apply(target=target, arguments=arguments):
            # 1. Seperate code and environment from the enclosure
            # Call the code with the arguments, and then environment
            code = fresh("code")
            env = fresh("env")

            return L0.Load(
                destination=code,
                base=target,
                index=0,
                then=L0.Load(
                    destination=env,
                    base=target,
                    index=0,
                    then=L0.Load(
                        destination=env,
                        base=target,
                        index=0,
                        then=L0.Call(target=target, arguments=arguments),
                    ),
                ),
            )

        case L1.Copy(destination=destination, source=source, then=then):
            return L0.Copy(destination=destination, source=source, then=recur(then))

        case L1.Immediate(destination=destination, value=value, then=then):
            return L0.Immediate(destination=destination, value=value, then=recur(then))

        case L1.Primitive(destination=destination, operator=operator, left=left, right=right, then=then):
            return L0.Primitive(destination=destination, operator=operator, left=left, right=right, then=recur(then))

        case L1.Branch(operator=operator, left=left, right=right, then=then, otherwise=otherwise):
            return L0.Branch(operator=operator, left=left, right=right, then=recur(then), otherwise=recur(otherwise))

        case L1.Allocate(destination=destination, count=count, then=then):
            return L0.Allocate(destination=destination, count=count, then=recur(then))

        case L1.Load(destination=destination, base=base, index=index, then=then):
            return L0.Load(destination=destination, base=base, index=index, then=recur(then))

        case L1.Store(base=base, index=index, value=value, then=then):
            return L0.Store(base=base, index=index, value=value, then=recur(then))

        case L1.Halt(value=value):
            return L0.Halt(value=value)


def close_program(program: L1.Program, fresh: Callable[[str], str]):
    match program:
        case L1.Program(parameters=parameters, body=body):
            procedures = list[L0.Procedure]()

            body = close_term(
                body,
                procedures.append,
                fresh,
            )

            procedures.extend(lifted)

            return L0.Program(procedures=[*procedures, L0.Procedure(name="l0", parameters=parameters, body=body)])
