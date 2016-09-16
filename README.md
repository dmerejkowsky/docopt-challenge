# My solution to the docopt challenge

OK, it's ~50 lines of Python, but here are a few reason I think `argparse` is
still a better choice

## Better return value


Using `argparse`:

```python
args = parse("ship move bounty 10.5 -5 --speed 42")
if args.cmd == "move_ship":
    move_ship(args.name, args.pos, args.speed)
```


Using `docopt`:

```python
def to_float(opt_str):
    try:
        return float(opt_str.replace("\\", ""))
    except ValueError:
        return 0

# Need to escape the minus to get a negative value
opts = parse("ship bounty move 10.5 \\-5 --speed 42")

x = to_float(opts["<x>"])
y = to_float(opts["<y>"])
speed = to_float(opts["--speed"])
position = Position(x, y)
(name, ) = opts["<name>"] # opts["<name>"] is still a list

if opts["ship"]:
    if opts["move"]:
        move_ship(name, position, speed)
```

So in the end you have ~20 lines of code before you can use the
return value of `docopt` ...

## Consistency and coupling

I've cheated a bit. In the `argparse` version, it's `ship move <name> <x> <y>`,
and not `move ship <name> <x> <y>` as in the `docopt` version.
Still, I find it more consistent.

Also, note how `argparse` return value is a class with sensible attributes
names, whereas with `docopt` you end up using `opt["foo"]`, `opt["--foo"]` or
`opt["<foo>"]` depending on whether it's a command, an option or an argument.

Also note how we have to add a custom conversion function to get real values
from the `<x>` and `<y>` arguments.

## Error messages

`docopt` will *always* print the usage if it can't parse the command line, with
no explanation.

`argparse` will generate much more information:

```console
$ naval_fate move
invalid choice: 'move' (choose from 'ship', 'mine')
$ naval_fate ship new
the following arguments are required: names
$ naval_fate ship move bounty 5 fortytwo
argument y: invalid float value: 'fortytwo'
```

## Help message

Of course, you can pass the whole docstring from the `docopt` version to the
`ArgumentParser` constructor, but look what happens if you don't:

```console
$ naval_fate -h
usage: naval_fate_argparse.py [-h] {ship,mine} ...

optional arguments:
  -h, --help   show this help message and exit

commands:
  {ship,mine}
```

```console
$ naval_fate ship new -h
Usage: naval_fate_argparse.py ship new [-h] names [names ...]

positional arguments:
  names

optional arguments:
  -h, --help  show this help message and exit
```

See? You get just the information you need!


## Maintainability

Here are a few changes that are much easier to do in the `argparse` version:

* Adding a new mine type (say `--deep`)

* Use a 3D position

* Add even adding new actions! Just make sure to use
  `parser.set_defaults(cmd=...)` and you're all set. In the `docopt` version,
  you'll have to carefully patch some code in the middle of several `if`
  statement ...
