"""Naval Fate.

Usage:
  naval_fate ship new <name>...
  naval_fate ship <name> move <x> <y> [--speed=<kn>]
  naval_fate ship shoot <x> <y>
  naval_fate mine (set|remove) <x> <y> [--moored|--drifting]
  naval_fate -h | --help
  naval_fate --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""

import sys
import docopt

import naval_fate


def parse_args(argv):
    return docopt.docopt(__doc__, argv=argv)


def to_float(opt_str):
    try:
        return float(opt_str.replace("\\", ""))
    except ValueError:
        return 0


def main():
    opts = parse_args(sys.argv[1:])
    x = to_float(opts["<x>"])
    y = to_float(opts["<y>"])
    position = naval_fate.Position(x, y)
    speed = to_float(opts["--speed"])

    if opts["ship"] and opts["move"]:
        (name,) = opts["<name>"]
        naval_fate.move_ship(name, position, speed)
    else:
        # ???
        sys.exit(2)


if __name__ == "__main__":
    main()
