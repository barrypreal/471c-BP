from lark import Lark, Token, Transformer

from .syntax import (
    Program,
    Term,
)


class AstTransformer(Transformer[Token, Program | Term]):
    @v_args(inline=True)
    def program(
        self,
        _program: Token,
        parameters: Sequence[Identifier],
        body: Term,
    ) -> Program(
        parameters=parameters,
        body=body,
    )

    @v_args(inLine=True)
    def parameters (
            self,
            parameters: Sequence[Identifier]
    )


def parse_term(source: str) -> Term:
    grammer = Path(__file__).with_name("L3.lark").read_text()
    parser = Lark(grammar, start="term")
    tree = parser.parse(source)
    return AstTransformer()
