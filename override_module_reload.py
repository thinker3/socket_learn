import overridee
def test1():
    from overrider import something, aclass
    aclass.show(1, 2, 3)

def test2():
    from overrider import something, aclass
    aclass.show(1, 2, 3)
    reload(overridee)

def main_0():
    from overrider import aclass # aclass is imported by overrider from overridee
    aclass.show(1, 2, 3)

def main_1():
    from overridee import aclass
    aclass.show(1, 2, 3)
    from overrider import something # just import something, but changed aclass.show
    aclass.show(1, 2, 3)
    from overridee import aclass # have no effect
    aclass.show(1, 2, 3)


def main_2(test):
    test()
    from overridee import aclass
    aclass.show(1, 2, 3)


#main_0()
#main_1()
#main_2(test1)
main_2(test2)


