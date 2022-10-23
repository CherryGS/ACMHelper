# AcmHelper

尝试成为 CLI 版的 codeforces polygon

文件结构

```txt
- Problem
    - config.yaml
    - std.cpp
    - checker.cpp (optional with "testlib.h")
    - interactor.cpp (optional with "testlib.h")
    - validator.cpp (optional with "testlib.h")
    - generator
        - test1.cpp
        - test2.py
    - accept
        - code1.cpp
        - code2.py
    - wrong
        - code3.cpp
        - code4.py
    - data
        - auto
            - in
                - 1.in
            - out
                - 1.out
            - wa
                - 1_test.wa
        - hand
            - in
                - 1.in
            - out
                - 1.out
            - wa
                - 1_test.wa
    - log
        - 20220303-13:03:03.log
```