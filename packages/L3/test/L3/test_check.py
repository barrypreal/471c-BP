import pytest
from L3.check import Context, check_program, check_term
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
    Program,
    Reference,
    Store,
)

# Abstract


def test_check_term_abstract():
    term = Abstract(
        parameters=["x"],
        body=Immediate(value=1),
    )

    context: Context = {}

    check_term(term, context)


def test_check_term_abstract_dupllicates():
    term = Abstract(
        parameters=["x", "x"],
        body=Immediate(value=1),
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


# Allocate


def test_check_term_allocate():
    term = Allocate(count=0)

    context: Context = {}

    check_term(term, context)


def test_check_term_allocate_less_than_0():
    term = Allocate(count=-1)

    context: Context = {}

    check_term(term, context)


# Apply


def test_check_term_apply():
    objectA = Reference(name="x")
    argA = Immediate(value=0)

    term = Apply(target=objectA, arguments=[argA])

    context: Context = {
        "x": None,
    }

    check_term(term, context)


# Begin


def test_check_term_begin():
    objectA = Immediate(value=1)
    argA = Immediate(value=0)

    term = Begin(effects=[argA], value=objectA)

    context: Context = {}

    check_term(term, context)


# Branch


def test_check_term_branch():
    op = "=="
    objA = Immediate(value=1)
    objB = Immediate(value=1)

    ifOp = Immediate(value=0)
    elseOp = Immediate(value=2)

    term = Branch(operator=op, left=objA, right=objB, consequent=ifOp, otherwise=elseOp)

    context: Context = {}

    check_term(term, context)


# Immediate


def test_check_term_immediate():
    term = Immediate(value=5)

    context: Context = {}

    check_term(term, context)


# Let


def test_check_term_let():
    term = Let(
        bindings=[
            ("x", Immediate(value=0)),
            ("y", Immediate(value=1)),
        ],
        body=Reference(name="x"),  # any other term
    )

    context: Context = {}

    check_term(term, context)


def test_check_term_let_duplicates():
    term = Let(
        bindings=[
            ("x", Immediate(value=0)),
            ("x", Immediate(value=1)),
        ],
        body=Reference(name="x"),  # any other term
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


def test_check_term_let_ref_error():
    term = Let(
        bindings=[
            ("x", Immediate(value=0)),
            ("y", Reference(name="x")),
        ],
        body=Immediate(value=0),
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


def test_check_term_let_ref_but_good():
    term = Let(
        bindings=[
            ("y", Reference(name="x")),
            ("x", Immediate(value=0)),
        ],
        body=Immediate(value=0),
    )

    context: Context = {}

    check_term(term, context)


# LetRec


def test_check_term_letrec_ref():
    term = LetRec(
        bindings=[
            ("x", Immediate(value=0)),
            ("y", Reference(name="x")),
        ],
        body=Immediate(value=0),
    )

    context: Context = {}

    check_term(term, context)


def test_check_term_letrec_scope():
    term = LetRec(
        bindings=[
            ("y", Reference(name="x")),
            ("x", Immediate(value=0)),
        ],
        body=Reference(name="x"),
    )

    context: Context = {}

    check_term(term, context)


def test_check_term_letrec_duplicate_binders():
    term = LetRec(
        bindings=[
            ("x", Immediate(value=0)),
            ("x", Immediate(value=1)),
        ],
        body=Reference(name="x"),
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


# Load


def test_check_term_load():
    item = Reference(name="x")

    term = Load(
        base=item,
        index=1,
    )

    context: Context = {
        "x": None,
    }

    check_term(term, context)


# Primitive


def test_check_term_primitive():
    objA = Immediate(value=1)
    objB = Immediate(value=1)
    op = "+"

    term = Primitive(operator=op, left=objA, right=objB)

    context: Context = {}

    check_term(term, context)


# Reference


def test_check_term_reference_bound():
    term = Reference(name="x")

    context: Context = {
        "x": None,
    }

    check_term(term, context)


def test_check_term_reference_free():
    term = Reference(name="x")

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


# Store
def test_check_term_store():
    item = Reference(name="x")
    val = Immediate(value=1)

    term = Store(
        base=item,
        index=1,
        value=val,
    )

    context: Context = {}

    check_term(term, context)


# Program


def test_check_program():
    program = Program(
        parameters=["x", "y"],
        body=Immediate(value=0),
    )

    check_program(program)


def test_check_program_duplicates():
    program = Program(
        parameters=["x", "x"],
        body=Immediate(value=0),
    )

    with pytest.raises(ValueError):
        check_program(program)
