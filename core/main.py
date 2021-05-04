# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import mmh3

import math_st
from config import Config
from math_st import Test2


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(mmh3.hash("foo"))
    print(math_st.add(1, 2))
    t = Test2()
    print(t.add2(2, 3))
    c = Config("dev")
    # c = Config()
    # print(c)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
