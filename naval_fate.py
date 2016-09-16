import argparse
import collections
import sys

class Position():
    def __init__(self):
        self.x = 0
        self.y = 0


class PosAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        # when called, values will be a float, and
        # self.dest will be 'x' or 'y', so
        # initialize namespace.pos if not already, and set
        # the correct Position attribute:
        if not hasattr(namespace, "pos"):
            namespace.pos = Position()
        setattr(namespace.pos, self.dest, values)


def configure_position_parser(parser):
    parser.add_argument("x", type=float, action=PosAction)
    parser.add_argument("y", type=float, action=PosAction)


def configure_ship_parser(parser):
    ship_commands = parser.add_subparsers(title="ship commands")
    new_ship = ship_commands.add_parser("new")
    new_ship.add_argument("name")
    new_ship.set_defaults(cmd="new_ship")

    shoot = ship_commands.add_parser("shoot")
    configure_position_parser(shoot)
    shoot.set_defaults(cmd="shoot")

    move_parser = ship_commands.add_parser("move")
    move_parser.add_argument("name")
    configure_position_parser(move_parser)
    move_parser.add_argument("--speed", metavar="<kn>", type=float)
    move_parser.set_defaults(cmd="move_ship")


def configure_mine_parser(parser):
    mine_commands = parser.add_subparsers(title="mine commands")
    for action in ["set", "remove"]:
        parser = mine_commands.add_parser(action)
        parser.set_defaults(cmd="%s_mine" % action)
        configure_position_parser(parser)
        for mine_type in ["moored", "drifting"]:
            parser.add_argument("--%s" % mine_type,
                                action="store_const", const=mine_type,
                                dest="mine_type")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="commands")

    # ship
    ship_parser = subparsers.add_parser("ship")
    configure_ship_parser(ship_parser)

    # mine
    mine_parser = subparsers.add_parser("mine")
    configure_mine_parser(mine_parser)

    args = parser.parse_args(argv)
    return args


if __name__ == "__main__":
    parse_args(sys.argv[1:])
