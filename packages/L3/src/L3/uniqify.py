from collections.abc import Callable, Mapping
from functools import partial

from util.sequential_name_generator import SequentialNameGenerator

from .syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Immediate,
    Let,
    LetRec,
    Load,
    Primitive,
    Program,
    Reference,
    Store,
    Term,
)

type Context = Mapping[str, str]


def uniqify_term(
    term: Term,
    context: Context,
    fresh: Callable[[str], str],
) -> Term:
    _term = partial(uniqify_term, context=context, fresh=fresh)

    match term:
        case Let(bindings=bindings, body=body):
            return Let(bindings=([(fresh(name), _term(value)) for name, value in bindings]), body=_term(body))

        case LetRec(bindings=bindings, body=body):
            return LetRec(bindings=([(fresh(name), _term(value)) for name, value in bindings]), body=_term(body))

        case Reference(name=name):
            for id, value in context.items():
                if id == name:
                    context = dict(context)
                    del context[id]
                    return Reference(name=value)

            return Reference(name=fresh(name))

        case Abstract(parameters=parameters, body=body):
            return Abstract(parameters=parameters, body=_term(body))

        case Apply(target=target, arguments=arguments):
            return Apply(target=_term(target), arguments=[_term(argument) for argument in arguments])

        case Immediate(value=value):
            return Immediate(value=value)

        case Primitive(operator=operator, left=left, right=right):
            return Primitive(operator=operator, left=_term(left), right=_term(right))

        case Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return Branch(
                operator=operator,
                left=_term(left),
                right=_term(right),
                consequent=_term(consequent),
                otherwise=_term(otherwise),
            )

        case Allocate(count=count):
            return Allocate(count=count)

        case Load(base=base, index=index):
            return Load(base=_term(base), index=index)

        case Store(base=base, index=index, value=value):
            return Store(base=_term(base), index=index, value=_term(value))

        case Begin(effects=effects, value=value):  # pragma: no branch
            return Begin(effects=[_term(effect) for effect in effects], value=_term(value))


def uniqify_program(
    program: Program,
) -> tuple[Callable[[str], str], Program]:  # pragma: no cover
    fresh = SequentialNameGenerator()

    _term = partial(uniqify_term, fresh=fresh)

    match program:
        case Program(parameters=parameters, body=body):  # pragma: no branch
            local = {parameter: fresh(parameter) for parameter in parameters}
            return (
                fresh,
                Program(
                    parameters=[local[parameter] for parameter in parameters],
                    body=_term(body, local),
                ),
            )
