from L3.syntax import (
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
    Reference,
    Store,
)
from L3.uniqify import Context, uniqify_term
from util.sequential_name_generator import SequentialNameGenerator


def test_uniqify_term_reference():
    term = Reference(name="x")

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh=fresh)

    expected = Reference(name="y")

    assert actual == expected


def test_uniqify_immediate():
    term = Immediate(value=42)

    context: Context = dict[str, str]()
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Immediate(value=42)

    assert actual == expected


def test_uniqify_term_let():
    term = Let(
        bindings=[
            ("x", Immediate(value=1)),
            ("y", Reference(name="x")),
        ],
        body=Apply(
            target=Reference(name="x"),
            arguments=[
                Reference(name="y"),
            ],
        ),
    )

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Let(
        bindings=[
            ("x0", Immediate(value=1)),
            ("y0", Reference(name="y")),
        ],
        body=Apply(
            target=Reference(name="y"),
            arguments=[
                Reference(name="y1"),
            ],
        ),
    )

    assert actual == expected


def test_uniqify_term_letrec():
    term = LetRec(
        bindings=[
            ("x", Immediate(value=1)),
            ("y", Reference(name="x")),
        ],
        body=Apply(
            target=Reference(name="x"),
            arguments=[
                Reference(name="y"),
            ],
        ),
    )

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = LetRec(
        bindings=[
            ("x0", Immediate(value=1)),
            ("y0", Reference(name="y")),
        ],
        body=Apply(
            target=Reference(name="y"),
            arguments=[
                Reference(name="y1"),
            ],
        ),
    )

    assert actual == expected


def test_uniqify_term_abstract():
    term = Abstract(parameters=[], body=Immediate(value=0))

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Abstract(parameters=[], body=Immediate(value=0))
    assert actual == expected


def test_uniqify_term_primitive():
    term = Primitive(operator="+", left=Immediate(value=0), right=Immediate(value=0))

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Primitive(operator="+", left=Immediate(value=0), right=Immediate(value=0))
    assert actual == expected


def test_uniqify_term_branch():
    term = Branch(
        operator="<",
        left=Immediate(value=0),
        right=Immediate(value=0),
        consequent=Immediate(value=0),
        otherwise=Immediate(value=0),
    )

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Branch(
        operator="<",
        left=Immediate(value=0),
        right=Immediate(value=0),
        consequent=Immediate(value=0),
        otherwise=Immediate(value=0),
    )
    assert actual == expected


def test_uniqify_term_allocate():
    term = Allocate(count=0)

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Allocate(count=0)
    assert actual == expected


def test_uniqify_term_load():
    term = Load(base=Immediate(value=0), index=1)

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Load(base=Immediate(value=0), index=1)
    assert actual == expected


def test_uniqify_term_store():
    term = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))
    assert actual == expected


def test_uniqify_term_begin():
    term = Begin(effects=[], value=Immediate(value=0))

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Begin(effects=[], value=Immediate(value=0))
    assert actual == expected
