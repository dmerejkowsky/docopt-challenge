import naval_fate_argparse

import pytest

def parse(cmd):
    return naval_fate_argparse.parse_args(cmd.split())


def test_help():
    with pytest.raises(SystemExit) as e:
        parse("--help")
    assert e.value.code == 0


def test_new_ship():
    args = parse("ship new bounty")
    assert args.cmd == "new_ship"
    assert args.name == "bounty"


def test_move_ship():
    args = parse("ship move bounty 10.5 -5 --speed 42")
    assert args.cmd == "move_ship"
    assert args.name == "bounty"
    assert args.pos.x == 10.5
    assert args.pos.y == -5
    assert args.speed == 42


def test_shoot():
    args = parse("ship shoot 1 2")
    assert args.cmd == "shoot"
    assert args.pos.x == 1
    assert args.pos.y == 2


def test_set_mine():
    args = parse("mine set 0 -1 --moored")
    assert args.cmd == "set_mine"
    assert args.pos.x == 0
    assert args.pos.y == -1
    assert args.mine_type == "moored"
