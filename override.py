from overrided import aclass

_aclass_show = aclass.show
def aclass_show(a, b=0, c=None):
    if b>0:
        print a, b
    else:
        _aclass_show(a, b)
aclass.show = aclass_show


something = 'something'

if __name__ == '__main__':
    _aclass_show(1)
    _aclass_show(1, 2)
    _aclass_show(1, 2, 3)
    aclass.show(1)
    aclass.show(1, 2)
    aclass.show(1, 2, 3)
