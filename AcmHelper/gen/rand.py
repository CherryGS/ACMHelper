from random import sample, randint


def rand_cut(n: int, cnt: int, min_value: int = 0):
    """将 `n` 切成 `cnt` 份 , 其中每一段的分布相同"""
    n -= min_value * cnt
    lis = sorted([randint(1, n) for _ in range(cnt)])
    for i in range(cnt - 1, 0, -1):
        lis[i] -= lis[i - 1] - min_value
    return lis
