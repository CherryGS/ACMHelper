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
        - make1.cpp
        - make2.py
    - accept
        - ac1.cpp
        - ac2.py
    - wrong
        - wa1.cpp
        - wa2.py
    - exec
        - something executable...
    - data
        - auto
            - in
                - 1.make1.in
                - 2.make2.in
            - out
                - 1.ac1.out
                - 1.wa1.out
        - save
            - in
                - 1.make1.in
                - 2.make2.in
            - out
                - 1.ac1.out
                - 1.wa1.out
    - log
        - 20220303-13:03:03.log
    - temp
        - someting temporary...
```