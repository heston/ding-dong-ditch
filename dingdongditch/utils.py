import os


class Env(object):
    @classmethod
    def raw(cls, name, default=None):
        return os.getenv(name, default)

    @classmethod
    def string(cls, name, default=''):
        return str(cls.raw(name, default))

    @classmethod
    def number(cls, name, default=0):
        val = cls.raw(name, default)
        try:
            try:
                if '.' in val:
                    return float(val)
                raise TypeError('Not a float')
            except TypeError:
                return int(val)
        except ValueError:
            return default

    @classmethod
    def boolean(cls, name, default=False):
        value = cls.raw(name)

        if value is None:
            return default

        if value in ('', '0', 'false', 'False', 'off', 'no'):
            return False
        return True
