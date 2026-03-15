from L2.constant_folding import constant_folding_term
from L2.constant_propagation import constant_propagation_term
from L2.dead_code_elimination import dead_code_elim_term
from L2.optimize import optimize_program
from L2.syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Immediate,
    Let,
    Load,
    Primitive,
    Program,
    Reference,
    Store,
)


def test_optimize_program():
    program = Program(
        parameters=[],
        body=Primitive(
            operator="+",
            left=Immediate(value=1),
            right=Immediate(value=1),
        ),
    )

    expected = Program(
        parameters=[],
        body=Immediate(value=2),
    )

    actual = optimize_program(program)

    assert actual == expected


def test_constant_folding_prim_left():
    term = Primitive(
        operator="+",
        left=Immediate(value=2),
        right=Immediate(value=1),
    )

    expected = Immediate(value=3)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_folding_prim_right():
    term = Primitive(
        operator="+",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    expected = Immediate(value=3)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_folding_prim_zero():
    term = Primitive(
        operator="+",
        left=Immediate(value=0),
        right=Immediate(value=2),
    )

    expected = Immediate(value=2)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_folding_prim_recur():
    term = Primitive(
        operator="+",
        left=Primitive(operator="+", left=Immediate(value=1), right=Immediate(value=1)),
        right=Primitive(operator="+", left=Immediate(value=1), right=Immediate(value=2)),
    )

    expected = Immediate(value=5)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_folding_prim_sub():
    term = Primitive(
        operator="-",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    expected = Primitive(
        operator="-",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_folding_prim_mult():
    term = Primitive(
        operator="*",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    expected = Primitive(
        operator="*",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_folding_let():
    term = Let(bindings=[], body=Immediate(value=1))

    expected = Let(bindings=[], body=Immediate(value=1))

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_prim():
    term = Primitive(
        operator="+",
        left=Primitive(operator="+", left=Immediate(value=2), right=Reference(name="x")),
        right=Primitive(operator="+", left=Immediate(value=2), right=Reference(name="y")),
    )

    expected = Primitive(
        operator="+",
        left=Immediate(value=4),
        right=Primitive(operator="+", left=Reference(name="x"), right=Reference(name="y")),
    )

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_prim_right():
    term = Primitive(
        operator="+",
        left=Immediate(value=0),
        right=Reference(name="x"),
    )

    expected = Reference(name="x")

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_prim_swap():
    term = Primitive(
        operator="+",
        left=Reference(name="x"),
        right=Immediate(value=1),
    )

    expected = Primitive(operator="+", left=Immediate(value=1), right=Reference(name="x"))

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_branch_invalid_lt():
    operator = "<"
    left = Reference(name="x")
    right = Immediate(value=2)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Immediate(value=4)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_branch_cons():
    operator = "=="
    left = Immediate(value=1)
    right = Immediate(value=1)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Immediate(value=3)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_branch_other():
    operator = "=="
    left = Immediate(value=1)
    right = Immediate(value=2)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Immediate(value=4)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_branch_lessthan():
    operator = "<"
    left = Immediate(value=1)
    right = Immediate(value=2)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Immediate(value=3)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_branch_lessthan_other():
    operator = "<"
    left = Immediate(value=1)
    right = Immediate(value=1)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Immediate(value=4)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_allocate():
    term = Allocate(count=4)

    expected = Allocate(count=4)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_load():
    term = Load(base=Immediate(value=0), index=1)

    expected = Load(base=Immediate(value=0), index=1)

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_store():
    term = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    expected = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_begin():
    term = Begin(effects=[], value=Immediate(value=0))

    expected = Begin(effects=[], value=Immediate(value=0))

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_abstract():
    term = Abstract(parameters=[], body=Immediate(value=0))

    expected = Abstract(parameters=[], body=Immediate(value=0))

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_fold_apply():
    term = Apply(arguments=[], target=Immediate(value=0))

    expected = Apply(arguments=[], target=Immediate(value=0))

    actual = constant_folding_term(term)

    assert actual == expected


def test_constant_propagation_prim():
    term = Primitive(
        operator="+",
        left=Immediate(value=2),
        right=Immediate(value=1),
    )

    expected = Primitive(
        operator="+",
        left=Immediate(value=2),
        right=Immediate(value=1),
    )

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_let():
    term = Let(bindings=[], body=Immediate(value=1))

    expected = Let(bindings=[], body=Immediate(value=1))

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_let_prim():
    term = Let(
        bindings=[("x", Immediate(value=1))],
        body=Primitive(operator="+", left=Reference(name="x"), right=Reference(name="x")),
    )

    expected = Let(
        bindings=[("x", Immediate(value=1))],
        body=Primitive(operator="+", left=Immediate(value=1), right=Immediate(value=1)),
    )

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_branch():
    operator = "=="
    left = Immediate(value=1)
    right = Immediate(value=1)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_allocate():
    term = Allocate(count=4)

    expected = Allocate(count=4)

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_load():
    term = Load(base=Immediate(value=0), index=1)

    expected = Load(base=Immediate(value=0), index=1)

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_store():
    term = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    expected = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_begin():
    term = Begin(effects=[], value=Immediate(value=0))

    expected = Begin(effects=[], value=Immediate(value=0))

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_abstract():
    term = Abstract(parameters=[], body=Immediate(value=0))

    expected = Abstract(parameters=[], body=Immediate(value=0))

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_apply():
    term = Apply(arguments=[], target=Immediate(value=0))

    expected = Apply(arguments=[], target=Immediate(value=0))

    actual = constant_propagation_term(term)

    assert actual == expected


def test_constant_propagation_reference():
    term = Reference(name="x")

    expected = Reference(name="x")

    actual = constant_propagation_term(term)

    assert actual == expected


def test_dead_code_elim_prim():
    term = Primitive(
        operator="+",
        left=Immediate(value=2),
        right=Immediate(value=1),
    )

    expected = Primitive(
        operator="+",
        left=Immediate(value=2),
        right=Immediate(value=1),
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let():
    term = Let(bindings=[], body=Immediate(value=1))

    expected = Let(bindings=[], body=Immediate(value=1))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_branch():
    operator = "=="
    left = Immediate(value=1)
    right = Immediate(value=1)
    consequent = Immediate(value=3)
    otherwise = Immediate(value=4)
    term = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    expected = Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise)

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_allocate():
    term = Allocate(count=4)

    expected = Allocate(count=4)

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_load():
    term = Load(base=Immediate(value=0), index=1)

    expected = Load(base=Immediate(value=0), index=1)

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_store():
    term = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    expected = Store(base=Immediate(value=0), index=1, value=Immediate(value=0))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_begin():
    term = Begin(effects=[], value=Immediate(value=0))

    expected = Begin(effects=[], value=Immediate(value=0))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_abstract():
    term = Abstract(parameters=[], body=Immediate(value=0))

    expected = Abstract(parameters=[], body=Immediate(value=0))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_apply():
    term = Apply(arguments=[], target=Immediate(value=0))

    expected = Apply(arguments=[], target=Immediate(value=0))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_reference():
    term = Reference(name="x")

    expected = Reference(name="x")

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_true():
    term = Let(bindings=[("x", Immediate(value=0))], body=Reference(name="x"))

    expected = Let(bindings=[("x", Immediate(value=0))], body=Reference(name="x"))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_false():
    term = Let(bindings=[("x", Immediate(value=0))], body=Immediate(value=0))

    expected = Let(bindings=[], body=Immediate(value=0))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_let_bindings():
    term = Let(
        bindings=[("x", Immediate(value=0))], body=Let(bindings=[("y", Reference(name="x"))], body=Reference(name="y"))
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))], body=Let(bindings=[("y", Reference(name="x"))], body=Reference(name="y"))
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_let_body():
    term = Let(bindings=[("x", Immediate(value=0))], body=Let(bindings=[], body=Reference(name="x")))

    expected = Let(bindings=[("x", Immediate(value=0))], body=Let(bindings=[], body=Reference(name="x")))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_abstract():
    term = Let(bindings=[("x", Immediate(value=0))], body=Abstract(parameters=[], body=Reference(name="x")))

    expected = Let(bindings=[("x", Immediate(value=0))], body=Abstract(parameters=[], body=Reference(name="x")))

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_apply_target():
    term = Let(
        bindings=[("x", Immediate(value=0))], body=Apply(target=Reference(name="y"), arguments=[Reference(name="x")])
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))], body=Apply(target=Reference(name="y"), arguments=[Reference(name="x")])
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_apply_arguments():
    term = Let(
        bindings=[("y", Immediate(value=0))], body=Apply(target=Reference(name="y"), arguments=[Reference(name="x")])
    )

    expected = Let(
        bindings=[("y", Immediate(value=0))], body=Apply(target=Reference(name="y"), arguments=[Reference(name="x")])
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_primitive_left():
    term = Let(
        bindings=[("y", Immediate(value=0))],
        body=Primitive(operator="+", left=Reference(name="y"), right=Reference(name="x")),
    )

    expected = Let(
        bindings=[("y", Immediate(value=0))],
        body=Primitive(operator="+", left=Reference(name="y"), right=Reference(name="x")),
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_primitive_right():
    term = Let(
        bindings=[("x", Immediate(value=0))],
        body=Primitive(operator="+", left=Reference(name="y"), right=Reference(name="x")),
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))],
        body=Primitive(operator="+", left=Reference(name="y"), right=Reference(name="x")),
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_branch_left():
    term = Let(
        bindings=[("x", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )
    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_branch_right():
    term = Let(
        bindings=[("y", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )

    expected = Let(
        bindings=[("y", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )
    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_branch_consequent():
    term = Let(
        bindings=[("z", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )

    expected = Let(
        bindings=[("z", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )
    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_branch_othrwise():
    term = Let(
        bindings=[("w", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )

    expected = Let(
        bindings=[("w", Immediate(value=0))],
        body=Branch(
            operator="==",
            left=Reference(name="x"),
            right=Reference(name="y"),
            consequent=Reference(name="z"),
            otherwise=Reference(name="w"),
        ),
    )
    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_allocate():
    term = Let(
        bindings=[("x", Immediate(value=0))],
        body=Allocate(count=0),
    )

    expected = Let(
        bindings=[],
        body=Allocate(count=0),
    )
    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_load():
    term = Let(
        bindings=[("x", Immediate(value=0))],
        body=Load(base=Reference(name="x"), index=0),
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))],
        body=Load(base=Reference(name="x"), index=0),
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_store_base():
    term = Let(
        bindings=[("x", Immediate(value=0))],
        body=Store(base=Reference(name="x"), index=0, value=Reference(name="y")),
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))],
        body=Store(base=Reference(name="x"), index=0, value=Reference(name="y")),
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_store_value():
    term = Let(
        bindings=[("y", Immediate(value=0))],
        body=Store(base=Reference(name="x"), index=0, value=Reference(name="y")),
    )

    expected = Let(
        bindings=[("y", Immediate(value=0))],
        body=Store(base=Reference(name="x"), index=0, value=Reference(name="y")),
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_begin_effects():
    term = Let(
        bindings=[("x", Immediate(value=0))], body=Begin(effects=[(Reference(name="x"))], value=Reference(name="y"))
    )

    expected = Let(
        bindings=[("x", Immediate(value=0))], body=Begin(effects=[(Reference(name="x"))], value=Reference(name="y"))
    )

    actual = dead_code_elim_term(term)

    assert actual == expected


def test_dead_code_elim_let_nested_begin_value():
    term = Let(
        bindings=[("y", Immediate(value=0))], body=Begin(effects=[(Reference(name="x"))], value=Reference(name="y"))
    )

    expected = Let(
        bindings=[("y", Immediate(value=0))], body=Begin(effects=[(Reference(name="x"))], value=Reference(name="y"))
    )

    actual = dead_code_elim_term(term)

    assert actual == expected
