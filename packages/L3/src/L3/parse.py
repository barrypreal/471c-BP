from ast import Lambda
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

from lark import Lark, Token, Transformer
from lark.visitors import v_args  # pyright: ignore[reportUnknownVariableType]

from .syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Identifier,
    Immediate,
    Let,
    LetRec,
    Load,
    Nat,
    Primitive,
    Program,
    Reference,
    Store,
    Term,
)


class AstTransformer(Transformer[Token, Program | Term]):
    @v_args(inline=True)
    def program(
        self,
        _program: Token,
        parameters: Sequence[Identifier],
        body: Term,
    ) -> Program:
        return Program(
            parameters=parameters,
            body=body,
        )

    def parameters(
        self,
        parameters: Sequence[Identifier],
    ) -> Sequence[Identifier]:
        return parameters

    @v_args(inline=True)
    def term(
        self,
        term: Term,
    ) -> Term:
        return term

    @v_args(inline=True)
    def let(
        self,
        _let: Token,
        bindings: Sequence[tuple[Identifier, Term]],
        body: Term,
    ) -> Term:
        return Let(
            bindings=bindings,
            body=body,
        )

    @v_args(inline=True)
    def letrec(
        self,
        _letrec: Token,
        bindings: Sequence[tuple[Identifier, Term]],
        body: Term,
    ) -> Term:
        return LetRec(
            bindings=bindings,
            body=body,
        )

    def bindings(
        self,
        bindings: Sequence[tuple[Identifier, Term]],
    ) -> Sequence[tuple[Identifier, Term]]:
        return bindings

    @v_args(inline=True)
    def binding(
        self,
        name: Identifier,
        value: Term,
    ) -> tuple[Identifier, Term]:
        return name, value

    @v_args(inline=True)
    def reference(
        self,
        name: Identifier,
    ) -> Term:
        return Reference(name=name)

    @v_args(inline=True)
    def abstract(self, _lam: Lambda, parameters: Sequence[Identifier], body: Term) -> Term:
        return Abstract(parameters=parameters, body=body)

    @v_args(inline=True)
    def apply(self, target: Term, arguments: Sequence[Term]) -> Term:
        return Apply(target=target, arguments=arguments)

    def arguments(
        self,
        arguments: Sequence[Term],
    ) -> Sequence[Term]:
        return arguments

    @v_args(inline=True)
    def argument(self, argument: Term) -> Term:
        return argument

    @v_args(inline=True)
    def immediate(
        self,
        value: int,
    ) -> Term:
        return Immediate(value=value)

    @v_args(inline=True)
    def primitive(
        self,
        operator: Literal[
            "+",
            "-",
            "*",
        ],
        left: Term,
        right: Term,
    ) -> Term:
        return Primitive(operator=operator, left=left, right=right)

    @v_args(inline=True)
    def branch(self, operator: Literal["==", "<"], left: Term, right: Term, consequent: Term, otherwise: Term) -> Term:
        return Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    @v_args(inline=True)
    def allocate(self, count: Nat) -> Term:
        return Allocate(count=count)

    @v_args(inline=True)
    def load(self, base: Term, index: Nat) -> Term:
        return Load(base=base, index=index)

    @v_args(inline=True)
    def store(self, base: Term, index: Nat, value: Term) -> Term:
        return Store(base=base, index=index, value=value)

    @v_args(inline=True)
    def begin(self, effects: Sequence[Term], value: Term) -> Term:
        return Begin(effects=effects, value=value)

    @v_args(inline=True)
    def value(self, value: Term) -> Term:
        return value

    def effects(
        self,
        effects: Sequence[Term],
    ) -> Sequence[Term]:
        return effects

    @v_args(inline=True)
    def effect(self, effect: Term) -> Term:
        return effect


def parse_term(source: str) -> Term:
    grammar = Path(__file__).with_name("L3.lark").read_text()
    parser = Lark(grammar, start="term")
    tree = parser.parse(source)  # pyright: ignore[reportUnknownMemberType]
    return AstTransformer().transform(tree)  # pyright: ignore[reportReturnType]


def parse_program(source: str) -> Program:
    grammar = Path(__file__).with_name("L3.lark").read_text()
    parser = Lark(grammar, start="program")
    tree = parser.parse(source)  # pyright: ignore[reportUnknownMemberType]
    return AstTransformer().transform(tree)  # pyright: ignore[reportReturnType]
