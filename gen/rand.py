from random import sample, randint


def rand_cut(n: int, cnt: int, min_value: int = 0):
    """将 `n` 切成 `cnt` 份 , 其中每一段的分布相同"""
    n -= min_value * cnt
    lis = sorted([randint(1, n) for _ in range(cnt)])
    for i in range(cnt - 1, 0, -1):
        lis[i] -= lis[i - 1] - min_value
    return lis


str_sigma = [
    "abcdefghijklmnopqrstuvwxyz",
    "abcdefghijklmnopqrstuvwxyz".upper(),
    "0123456789",
]


def rand_str(n: int, _type: str | None = "l", sigma: str | None = None):
    """
    生成随机字符串
        n : 长度
        _type : 字符集
            l -> lower
            u -> upper
            n -> number
            及其组合
        sigma : 自定义字符集 , 与 _type 求并
    """
    s: set[str] = set()
    if _type is not None:
        for i in _type:
            r = 0
            if i == "l":
                r = 0
            elif i == "u":
                r = 1
            else:
                r = 2

            s = s | {_ for _ in str_sigma[r]}
    if sigma is not None:
        s = s | {_ for _ in sigma}
    return ''.join(sample(s, n))
