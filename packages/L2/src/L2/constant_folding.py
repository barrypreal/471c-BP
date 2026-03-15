from functools import partial

from .syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Immediate,
    Let,
    Load,
    Primitive,
    Reference,
    Store,
    Term,
)


def constant_folding_term(
    term: Term,
) -> Term:
    recur = partial(constant_folding_term)

    match term:
        case Let(bindings=bindings, body=body):
            return Let(bindings=[(name, recur(value)) for name, value in bindings], body=recur(body))

        case Reference(name=name):
            return Reference(name=name)

        case Abstract(parameters=parameters, body=body):
            return Abstract(parameters=parameters, body=recur(body))

        case Apply(target=target, arguments=arguments):
            return Apply(arguments=[recur(argument) for argument in arguments], target=recur(target))

        case Immediate(value=value):
            return Immediate(value=value)

        case Primitive(operator=operator, left=left, right=right):
            match operator:
                case "+":
                    match recur(left), recur(right):
                        case Immediate(value=i1), Immediate(value=i2):
                            return Immediate(value=i1 + i2)

                        case Immediate(value=0), right:
                            return right

                        case Primitive(operator="+", left=Immediate(value=i1), right=left1), Primitive(
                            operator="+", left=Immediate(value=i2), right=right1
                        ):
                            return Primitive(
                                operator="+",
                                left=Immediate(value=i1 + i2),
                                right=Primitive(
                                    operator="+",
                                    left=left1,
                                    right=right1,
                                ),
                            )

                        case left, Immediate() as right:
                            return Primitive(operator="+", left=right, right=left)

                        case left, right:
                            return Primitive(operator="+", left=left, right=right)

                case "-":
                    return Primitive(operator="-", left=left, right=right)

                case "*":
                    return Primitive(operator="*", left=left, right=right)

        case Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            match operator:
                case "==":
                    match recur(left) == recur(right):
                        case True:
                            return recur(consequent)
                        case False:
                            return recur(otherwise)

                case "<":
                    match left, right:
                        case Immediate(value=value1), Immediate(value=value2):
                            if value1 < value2:
                                return recur(consequent)
                            else:
                                return recur(otherwise)
                        case _:
                            return recur(otherwise)

        case Allocate(count=count):
            return Allocate(count=count)

        case Load(base=base, index=index):
            return Load(base=recur(base), index=index)

        case Store(base=base, index=index, value=value):
            return Store(base=recur(base), index=index, value=recur(value))

        case Begin(effects=effects, value=value):  # pragma: no branch
            return Begin(effects=[recur(effect) for effect in effects], value=recur(value))
