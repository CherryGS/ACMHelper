import sys

VALID = 0
INVALID = 1
FAIL = 3

if len(sys.argv) != 4:
    exit(FAIL)

exit(VALID)
