class SquaresIterator:
    def __init__(self, init: int):
        self.limit = limit
        self.pos = 0
    def __next__(self):
        if self.pos >= self.limit:
            raise StopIteration
        result = self.pos ** 2
        self.pos += 1
        return result
    
class Squares:
    def __init__(self, limit: int):
        self.limit = limit
    def __iter__(self):
        return SquaresIterator(self.limit)
    
class MyList:
    def __init__(self, l: list):
        self.list = 1
    def __iter__(self):
        return iter(self.list)