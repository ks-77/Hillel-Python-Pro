from decimal import Decimal
from colorama import Fore, Style


class frange:
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        self.start = Decimal(start)
        self.stop = Decimal(stop)
        self.step = Decimal(step)

    def __next__(self):
        if self.step > 0 and self.start >= self.stop:
            raise StopIteration
        elif self.step < 0 and self.start <= self.stop:
            raise StopIteration
        else:
            value = self.start
            self.start += self.step
            return value

    def __iter__(self):
        return self


class colorizer:
    def __init__(self, color):
        self.color = color  # color write in capital

    def __enter__(self):
        print(Fore.__dict__[self.color], end='')

    def __exit__(self, exc_type, exc_value, trace):
        print(Style.RESET_ALL, end='')
