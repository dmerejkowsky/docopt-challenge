import naval_fate_docopt

import pytest

def parse(cmd):
    return naval_fate_docopt.parse_args(cmd.split())


def test_new_ship():
    opts = parse("ship new bounty")
    assert opts["<name>"] == ["bounty"]
    assert opts["ship"] is True
    assert opts["new"] is True


def test_move_ship():
    # need to escape the minus for a negative value
    opts = parse("ship bounty move 10.5 \\-5 --speed 42")
    assert opts["ship"] is True
    assert opts["move"] is True
    assert opts["<name>"]== ["bounty"] # note : still a list!
    assert opts["<x>"] == "10.5" # a string
    assert opts["<y>"] == "\\-5" # backslash still here
    assert opts["--speed"] == "42"


def test_shoot():
    opts = parse("ship shoot 1 2")
    assert opts["ship"] is True
    assert opts["shoot"] is True
    assert opts["<x>"] == "1"
    assert opts["<y>"] == "2"


def test_set_mine():
    opts = parse("mine set 0 \\-1 --moored")
    assert opts["mine"] is True
    assert opts["set"] is True
    assert opts["<x>"] == "0"
    assert opts["<y>"] == "\\-1"
    assert opts["--moored"] is True
