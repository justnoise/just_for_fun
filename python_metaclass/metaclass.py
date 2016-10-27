from pprint import pformat
from copy import deepcopy


class AttributeMetaclass(type):

    def __new__(mcs, class_name, bases, dct):
        new_attrs = {}
        value_attrs = {}
        for k, v in dct.iteritems():
            # ignore nested classes and functions
            # not comprehensive but good enough for now
            if k.startswith('_') or type(v) == type or hasattr(v, '__call__'):
                new_attrs[k] = v
            else:
                value_attrs[k] = v
        new_attrs['_initial_values'] = value_attrs
        return super(AttributeMetaclass, mcs).__new__(mcs, class_name, bases, new_attrs)


class EasyObject(object):

    __metaclass__ = AttributeMetaclass

    def __init__(self, **kwargs):
        for k, v in deepcopy(self._initial_values).iteritems():
            setattr(self, k, v)
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        d = {}
        for k, v in self.__dict__.iteritems():
            if k.startswith('_') or type(k) == type or hasattr(k, '__call__'):
                continue
            else:
                d[k] = v
        return pformat(d)


class Apple(EasyObject):
    color = 'red'
    taste = 'tart'


class Pear(EasyObject):
    color = 'greenish'
    taste = 'sweet'

    def rot(self):
        self.color = 'brown'
        self.taste = 'mushy'


def main():
    good_apple = Apple()
    rotton_apple = Apple(taste='gross')
    print 'good_apple', good_apple
    print 'rotton_apple', rotton_apple

    changing_pear = Pear()
    print 'changing_pear', changing_pear
    unripe_pear = Pear(taste='chalky')
    changing_pear.rot()
    print 'unripe_pear', unripe_pear
    print 'changing_pear', changing_pear

if __name__ == '__main__':
    main()
