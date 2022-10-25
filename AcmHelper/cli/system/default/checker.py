"""Compare output and answer line by line."""
import sys

AC = 0
WA = 1
FAIL = 3

if len(sys.argv) != 4:
    exit(FAIL)

print(len(sys.argv))
inp = open(sys.argv[1], "r")
oup = open(sys.argv[2], "r")
ans = open(sys.argv[3], "r")
try:
    for i, j in zip(oup, ans, strict=True):
        if i.strip() == j.strip():
            continue
        exit(WA)
except ValueError as e:
    exit(WA)
except Exception as e:
    exit(FAIL)
exit(AC)
