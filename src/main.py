"""
advent-of-code-2021
"""

import sys

def main(argv):
    """
    Application entry point
    """
    print(argv)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == '__main__':
    main(sys.argv)

