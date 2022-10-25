# AcmHelper

本地环境下的 Polygon , 但不止于 Polygon.

你可以

- 快速创建具有合理结构的题目文件夹
- 指定 `std` , `checker` , `validator` , `interactor` 
- 使用不同语言完成不同部分 (cpp/py)
- 使用额外的程序来测试数据的质量
- 使用预制的数据生成器快速生成具有某些特征的数据 (py)
- 同时使用多种数据生成器 , 并可以指定每个程序所接受的生成器
- 享受由 `rich` , `typer`, `loguru` 带来的美丽

TODO

- [ ] 使 `helper sys run` 可以执行 `save` 下的数据
- [ ] 添加对 `Validator` 和 `Interactor` 的支持
- [ ] 根据 `hash` 动态选择是否编译

## 简易使用说明

得益于 `typer` , 关于题目生成的功能都可以通过输入 `helper --help` 大致了解

### 安装

`pip install acmhelper`

**你需要具有全局的`g++` , 默认使用 `-std=c++17` 编译** , 可在设置修改

### 数据生成

```py
from AcmHelper import gen
from rich import inspect

tree = gen.Tree(10, weighed=True)
tree.gen_edge()
tree.gen_weight(1, 10)
inspect(tree)

dag = gen.DAG(10, 20, weighed=False)
dag.gen_edge()
inspect(dag)

graph = gen.Graph(10, 20, weighed=True)
graph.gen_edge()
graph.gen_weight(-10, -1)
inspect(graph)

gen_str = gen.String(_type="lun", sigma="!@#$%^&*()")
inspect(gen_str(50))

try:
    tree.render(name='tree')
    dag.render(name='dag')
    graph.render(name='graph')
except:
    pass
```

### 快速从数据文件得到渲染的图

**如果想要使用图的渲染功能 , 你需要下载 Graphviz 的二进制文件并且将其加入 Path**

对于形式为 

```txt
n m (optional)
u1 v1 w1 (w1 is optional)
...
un vn wn
```

的数据 , 可以使用 `helper render` 来快速渲染

首先创建文件 `test.in` , 写入一个不连通的 `DAG`

```txt
5 2
1 2 3
1 3 5
1 5 -7
```

在该文件目录下输入 `helper render -dic test.in`

查看 `test.png` , 应该如下所示

![test](Assert/test.png)

具体的设置请使用 `helper render --help` 查看

### 创建一道题目(以 "输出一个绝对值小于输入数字绝对值的整数"为例(`int`范围内))

首先新建文件夹 `Problem` , 然后在此文件夹下打开命令行 , 输入 `helper sys init` , 回答问题 , 完成初始化

如果初始化正确的话你的目录结构应该向下面的一样(部分文件可能没有 , 这需要我们后续手动创建)

```txt
题目目录结构
- Problem
    - config.json
    - std.cpp/py
    - testlib.h (optional)
    - checker.cpp/py (optional with "testlib.h")
    - interactor.cpp (optional with "testlib.h") (Not implemented)
    - validator.cpp (optional with "testlib.h") (Not implemented)
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
        - 20220303.log
    - temp
        - someting temporary...
    - output
        - something...
```

然后打开 `std.cpp` , 写入以下代码

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int a; 
    cin >> a; 
    cout << abs(a)/2 << '\n'; 
    return 0;
}
```

保存后 , 我们来写第一个数据生成器 `make1.py` , 它只用来生成大于 `0` 的数.

在 `generator` 下创建文件 `make1.py` , 写入以下代码

```py
from random import randint
print(randint(1, 1000))
```

接下来只需要修改一些配置 , 就可以通过 `CLI` 来生成数据了

打开文件 `config.json` , 将如下代码复制

```json
{
    "gen_list": [
        "make1"
    ],
    "accept_list": [],
    "wrong_list": [],
    "gen_link_code": {
        "make1": [
            "std"
        ]
    },
    "gen_data_num": {
        "make1": 10
    },
    "time_limit": 2,
    "max_time_limit": 10,
    "std": "std",
    "checker": "checker",
    "interactor": "",
    "validator": "",
    "gcc_version" 17
}
```

这个文件描述的含义是 , 有一个生成器 `make1` , 其生成 10 组数据 , 生成的数据被用来运行 `std` , 没有额外的理论错误和理论正确的代码 , `Time_Limit_Exceed` 的上界是 `2s` , 程序被 kill 掉的上界是 `10s` , std 的辨识名称为 `std` , checker 的辨识名称为 `checker` , 没有使用 `interactor` 和 `validator` , 使用 `-std=c++17` 编译

保存后 , 输入 `helper sys run` , 你应该能看到我们暂时性的成功

接下来 , 我们来添加额外的生成器,测试代码和 `checker` 来完善这道题

在 `wrong` 下创建 `wa1.cpp` 和 `wa2.py` , 然后写入下述代码

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int a; 
    cin >> a; 
    cout << a-1 << '\n'; 
    return 0;
}
```



```py
n = int(input())
print(n + 1)
```



在 `accept` 下创建 `ac1.cpp` 写入如下代码

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int a; 
    cin >> a; 
    if(a >= 0) { cout << a-1 << '\n'; }
    else { cout << a+1 << '\n'; }
    return 0;
}
```

可以发现 , `wrong` 下的两个代码分别会在 `a<0` 和 `a>0` 时出错 , 所以我们再新建一个生成器

在 `generator` 下创建 `make2.py` 写入如下代码 , 注意负号

```py
from random import randint
print(-randint(1, 1000))
```

可以发现这道题需要 `checker` , 打开 `checker.cpp` , 写入如下代码

```cpp
#include <bits/stdc++.h>
#include "testlib.h"
using namespace std;

int main(int argc,char** argv) {
    registerTestlibCmd(argc,argv); // Required
    int n = inf.readInt();
    int m = ouf.readInt();
    if(abs(m) < abs(n)) { quitf(_ok,"Correct!"); }
    else { quitf(_wa,"Wrong Answer!"); }
}
```

最后我们再修改一下 `config.json`

```json
{
    "gen_list": [
        "make1",
        "make2"
    ],
    "accept_list": [
        "ac1"
    ],
    "wrong_list": [
        "wa1",
        "wa2"
    ],
    "gen_link_code": {
        "make1": [
            "std",
            "ac1",
            "wa1",
            "wa2"
        ],
        "make2": [
            "std",
            "ac1",
            "wa1",
            "wa2"
        ]
    },
    "gen_data_num": {
        "make1": 10,
        "make2": 10
    },
    "time_limit": 2,
    "max_time_limit": 10,
    "std": "std",
    "checker": "checker",
    "interactor": "",
    "validator": "",
    "gcc_version": 17
}
```

最后输入 `helper sys run` , 完成了.

如果字体和终端合适 , 你应该会看到像这样的东西

![result](Assert/table.png)

不出意料地 , 两个不对的程序在合适的地方不对了.

作为结尾 , 我们来使用 `CLI` 打包数据以及 `checker`

输入 `helper sys add 1 2 3 4 5 6 7 8 9 10` , 这样我们就将前10组输入数据和 `std` 的输出数据从 `auto` 移动到了 `save` 下 , 值得注意的是 , 数据的编号会自动地递增 , 所以不用担心数据覆盖问题

然后输入 `helper sys output checker.cc` , 查看 `output` 文件夹下 , 你应该可以看到名为 `data.zip` 的文件 , 其中的所有文件都被合适的重命名了 , 特殊的 , `checker` 被重命名为了 `checker.cc`

更细节的使用请参考 `helper sys --help` , `helper sys add --help` 等