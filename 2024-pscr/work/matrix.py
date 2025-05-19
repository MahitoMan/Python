class Vector:
    def __init__(self, elements):
        self.elements = list(elements)
    
    @property
    def length(self):
        return len(self.elements)
    
    def __add__(self, other):
        if isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Vectors must be of the same length")
            return Vector([a + b for a, b in zip(self.elements, other.elements)])
        elif isinstance(other, (int, float)):
            return Vector([a + other for a in self.elements])
        else:
            return NotImplemented
    
    __radd__ = __add__
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Vectors must be of the same length")
            return Vector([a - b for a, b in zip(self.elements, other.elements)])
        elif isinstance(other, (int, float)):
            return Vector([a - other for a in self.elements])
        else:
            return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Vector([other - a for a in self.elements])
        else:
            return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Vectors must be of the same length")
            return Vector([a * b for a, b in zip(self.elements, other.elements)])
        elif isinstance(other, (int, float)):
            return Vector([a * other for a in self.elements])
        else:
            return NotImplemented
    
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        if isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Vectors must be of the same length")
            return Vector([a / b for a, b in zip(self.elements, other.elements)])
        elif isinstance(other, (int, float)):
            return Vector([a / other for a in self.elements])
        else:
            return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector([other / a for a in self.elements])
        else:
            return NotImplemented
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return Vector(self.elements[index])
        return self.elements[index]
    
    def __setitem__(self, index, value):
        self.elements[index] = value
    
    def __str__(self):
        return '[' + ', '.join(map(str, self.elements)) + ']'
    
    def __repr__(self):
        return f'Vector({self.elements})'


class Matrix:
    def __init__(self, rows):
        if not rows:
            self.elements = []
            self.rows = 0
            self.cols = 0
            return
        
        row_lens = {len(row) for row in rows}
        if len(row_lens) > 1:
            raise ValueError("All rows must have the same length")
        
        self.elements = [list(row) for row in rows]
        self.rows = len(rows)
        self.cols = len(rows[0]) if self.rows else 0
    
    @property
    def length(self):
        return self.rows * self.cols
    
    def _flatten(self):
        return [elem for row in self.elements for elem in row]
    
    def _unflatten(self, flat_list):
        return [flat_list[i*self.cols : (i+1)*self.cols] for i in range(self.rows)]
    
    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions")
            return Matrix([[a+b for a, b in zip(ra, rb)] for ra, rb in zip(self.elements, other.elements)])
        elif isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Matrix and Vector lengths must match")
            flat = [a + b for a, b in zip(self._flatten(), other.elements)]
            return Matrix(self._unflatten(flat))
        elif isinstance(other, (int, float)):
            return Matrix([[a + other for a in row] for row in self.elements])
        return NotImplemented
    
    __radd__ = __add__
    
    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions")
            return Matrix([[a-b for a, b in zip(ra, rb)] for ra, rb in zip(self.elements, other.elements)])
        elif isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Matrix and Vector lengths must match")
            flat = [a - b for a, b in zip(self._flatten(), other.elements)]
            return Matrix(self._unflatten(flat))
        elif isinstance(other, (int, float)):
            return Matrix([[a - other for a in row] for row in self.elements])
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Matrix([[other - a for a in row] for row in self.elements])
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise ValueError("Matrices must have the same dimensions")
            return Matrix([[a*b for a, b in zip(ra, rb)] for ra, rb in zip(self.elements, other.elements)])
        elif isinstance(other, Vector):
            if self.length != other.length:
                raise ValueError("Matrix and Vector lengths must match")
            flat = [a * b for a, b in zip(self._flatten(), other.elements)]
            return Matrix(self._unflatten(flat))
        elif isinstance(other, (int, float)):
            return Matrix([[a * other for a in row] for row in self.elements])
        return NotImplemented
    
    __rmul__ = __mul__
    
    def __getitem__(self, indices):
        if isinstance(indices, tuple):
            if len(indices) != 2:
                raise IndexError("Matrix indices must be 2D")
            row_idx, col_idx = indices
            
            rows = self.elements[row_idx] if isinstance(row_idx, slice) else [self.elements[row_idx]]
            rows = rows if isinstance(rows[0], list) else [rows]
            
            new_rows = []
            for row in rows:
                cols = row[col_idx] if isinstance(col_idx, slice) else [row[col_idx]]
                new_rows.append(cols if isinstance(cols, list) else [cols])
            return Matrix(new_rows)
        else:
            sliced = self.elements[indices]
            return Matrix([sliced] if isinstance(indices, int) else sliced)
    
    def __setitem__(self, indices, value):
        if isinstance(indices, tuple) and len(indices) == 2:
            row, col = indices
            self.elements[row][col] = value
        else:
            self.elements[indices] = value
    
    def __str__(self):
        return '[\n' + ',\n'.join('  [' + ', '.join(map(str, row)) + ']' for row in self.elements) + '\n]'
    
    def __repr__(self):
        return f'Matrix({self.elements})'