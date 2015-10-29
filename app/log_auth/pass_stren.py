"""
Reworked from code originally taken from here:
http://bredsaal.dk/calculating-password-entropy-in-python
reference to wiki link in there also.

Essentially works out bit requirements to replicate variety -
Say I can choose from only [abc] and my password is 4 digits long (eg acba);
I have 3^4 = 81 choices;
In binary, 2 ^ 6 = 64, 2 ^ 7 = 128
log(81, 2) = 6.3
ie 6.3 bits required to represent that level of diversity.

#NOTE: we do not here test for randomness (and positively assume it);
ie we don't factor in dictionary attacks.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from math import log, pow, ceil


class PasswordCalc(object):
    """
    convert our ascii characters;
    create our upper, lower, digit and symbol sets;
    score entropy for intersections.
    """
    # our ordinals
    upp = set(range(65, 91))
    low = set(range(97, 123))
    dig = set(range(48, 58))
    sym = set(range(33, 128)) - upp - low - dig

    def __init__(self, password=None):
        if password:
            self.get_entropy(password)

    def get_entropy(self, password):
        self.get_entropy_val(password)
        return self.table_conversion(self.h)

    def get_entropy_val(self, password):
        self.password = password
        self.variety, o_password = 0, set(map(ord, password))
        for group in self.upp, self.low, self.dig, self.sym:
            if set.intersection(o_password, group): self.variety += len(group)
        # convert choices into bits to determine variety
        self.h = log(pow(self.variety, len(password)), 2)
        return self.h

    def table_conversion(self, h):
        """fairly arbitrary breakpoints"""
        if h < 50: self.strength = 'weak'
        elif h < 90: self.strength = 'medium'
        else: self.strength = 'strong'
        return self.strength

    def remedials(self):
        """
        Not used: just figuring out the remedial fixes needed to make medium strength
        """
        targ = pow(2, 50)
        print 'same characters required:', ceil(log(targ, self.variety)) - len(self.password)
        print 'char points required:', pow(targ, 1.0 / len(self.password)) - self.variety


if __name__ == '__main__':
    pc = PasswordCalc()
    str = pc.get_entropy('dasher')
    pc.remedials()
