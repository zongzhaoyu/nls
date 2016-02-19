#   nls/pumping.py
#   The module defines abstract type and operation with pumping objects. Also it provides several predefined pumping
#   classes.
#   (c) Daniel Bershatsky, 2016
#   See LICENSE for details

from numpy import exp


class AbstractPumping(object):
    """Base class of pumping tree that define commont interface of pumping objects behavior.
    """

    def __add__(self, other):
        return OpSumPumping(self, other)

    def __sub__(self, other):
        return OpSubPumping(self, other)

    def __str__(self):
        return str(repr(self))

    def __repr__(self):
        return u'AbstractPumping'

    def __unicode__ (self):
        return repr(self);


class OpSumPumping(AbstractPumping):
    """Functor object that incapsulates two pumping functional objects and represents their sum.
    """

    def __init__(self, lhs, rhs):
        super(AbstractPumping, self).__init__()

        self.lhs = lhs
        self.rhs = rhs

    def __call__(self, *args, **kwargs):
        return self.lhs(*args, **kwargs) + self.rhs(*args, **kwargs)

    def __repr__(self):
        return repr(self.lhs) + u' + ' + repr(self.rhs)


class OpSubPumping(AbstractPumping):
    """Functor object that incapsulates two pumping functional objects and represents their substract.
    """

    def __init__(self, lhs, rhs):
        super(AbstractPumping, self).__init__()

        self.lhs = lhs
        self.rhs = rhs

    def __call__(self, *args, **kwargs):
        return self.lhs(*args, **kwargs) - self.rhs(*args, **kwargs)

    def __repr__(self):
        return repr(self.lhs) + u' - ' + repr(self.rhs)


class GaussianPumping(AbstractPumping):
    """Steady state gaussian pumping with given origin, maximum power, and decay.
    """

    def __init__(self, power=1.0, x0=0.0, y0=0.0, variation=5.0):
        super(AbstractPumping, self).__init__()

        self.power = power
        self.x0 = x0
        self.y0 = y0
        self.variation = variation

    def __call__(self, x, y, t=None):
        return self.power * exp( - ((x - self.x0) ** 2 + (y - self.y0) ** 2) / (2.0 * self.variation))

    def __repr__(self):
        pattern = u'{0} exp(-{1} ((x - {2})^2 - (x - {3})^2))'
        return pattern.format(self.power, 1.0 / (2.0 * self.variation), self.x0, self.y0)


class GaussianPumping1D(GaussianPumping):
    """Facade object for `GaussianPumping` class in one dimension case. This overrides only parent call-method.
    """

    def __init__(self, power=1.0, x0=0.0, y0=0.0, variation=5.0):
        super(GaussianPumping1D, self).__init__(power, x0, y0, variation)

    def __call__(self, x, t=None):
        return GaussianPumping.__call__(self, x, 0.0, t)


class GaussianPumping2D(GaussianPumping):
    """Facade(actually proxy) for `GaussianPumping` class in two dimension case.
    """

    def __init__(self, power=1.0, x0=0.0, y0=0.0, variation=5.0):
        super(GaussianPumping2D, self).__init__(power, x0, y0, variation)