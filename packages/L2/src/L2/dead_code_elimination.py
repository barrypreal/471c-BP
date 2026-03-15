from functools import partial

from .syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Identifier,
    Immediate,
    Let,
    Load,
    Primitive,
    Reference,
    Store,
    Term,
)


def clean_vars(
    term: Term,
    refer: Identifier,
) -> bool:
    recur = partial(clean_vars)

    match term:
        case Let(bindings=bindings, body=body):
            for name, value in bindings:
                if name == refer or recur(value, refer):
                    return True
            return recur(body, refer)

        case Reference(name=name):
            return refer == name

        case Abstract(parameters=_parameters, body=body):
            return recur(body, refer)

        case Apply(target=target, arguments=arguments):
            for argument in arguments:
                if recur(argument, refer):
                    return True
            return recur(target, refer)

        case Immediate(value=value):
            return False

        case Primitive(operator=_operator, left=left, right=right):
            return recur(left, refer) or recur(right, refer)

        case Branch(operator=_operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return recur(left, refer) or recur(right, refer) or recur(consequent, refer) or recur(otherwise, refer)

        case Allocate(count=_count):
            return False

        case Load(base=base, index=_index):
            return recur(base, refer)

        case Store(base=base, index=_index, value=value):
            return recur(base, refer) or recur(value, refer)

        case Begin(effects=effects, value=value):  # pragma: no branch
            for effect in effects:
                if recur(effect, refer):
                    return True
            return recur(value, refer)


def dead_code_elim_term(
    term: Term,
) -> Term:
    recur = partial(dead_code_elim_term)

    match term:
        case Let(bindings=bindings, body=body):
            return Let(
                bindings=[(name, recur(value)) for name, value in bindings if (clean_vars(body, name))],
                body=recur(body),
            )

        case Reference(name=name):
            return Reference(name=name)

        case Abstract(parameters=parameters, body=body):
            return Abstract(parameters=parameters, body=recur(body))

        case Apply(target=target, arguments=arguments):
            return Apply(arguments=[recur(argument) for argument in arguments], target=recur(target))

        case Immediate(value=value):
            return Immediate(value=value)

        case Primitive(operator=operator, left=left, right=right):
            return Primitive(operator=operator, left=recur(left), right=recur(right))

        case Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return Branch(
                operator=operator,
                left=recur(left),
                right=recur(right),
                consequent=recur(consequent),
                otherwise=recur(otherwise),
            )

        case Allocate(count=count):
            return Allocate(count=count)

        case Load(base=base, index=index):
            return Load(base=recur(base), index=index)

        case Store(base=base, index=index, value=value):
            return Store(base=recur(base), index=index, value=recur(value))

        case Begin(effects=effects, value=value):  # pragma: no branch
            return Begin(effects=[recur(effect) for effect in effects], value=recur(value))
