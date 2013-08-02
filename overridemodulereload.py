import overrided
def test1():
    from override import something, aclass
    aclass.show(1, 2, 3)

def test2():
    from override import something, aclass
    aclass.show(1, 2, 3)
    reload(overrided)

def main_0():
    from override import aclass # aclass is imported by override from overrided
    aclass.show(1, 2, 3)

def main_1():
    from overrided import aclass
    aclass.show(1, 2, 3)
    from override import something # just import something, but changed aclass.show
    aclass.show(1, 2, 3)
    from overrided import aclass # have no effect
    aclass.show(1, 2, 3)


def main_2(test):
    test()
    from overrided import aclass
    aclass.show(1, 2, 3)


#main_0()
#main_1()
main_2(test1)
#main_2(test2)


