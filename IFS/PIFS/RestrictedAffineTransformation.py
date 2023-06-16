# preamble to set up directory
import os, sys
dir2 = os.path.abspath('')
dir1 = os.path.dirname(dir2)
if not dir1 in sys.path: sys.path.append(dir1)

from AffineTransformation import AffineTransformation
    
class RestrictedAffineTransformation(AffineTransformation):
    def __init__(self, ratio, matrix_type, e, f):
        a, b, c, d = self.get_matrix(matrix_type)
        
        a *= ratio
        b *= ratio
        c *= ratio
        d *= ratio
        
        super().__init__(a, b, c, d, e, f)
    
        
    def get_matrix(self, matrix_type):
        a = b = c = d = 0 
        
        if matrix_type == 0:
            a = d = 1
        elif matrix_type == 1: 
            a = 1
            d = -1
        elif matrix_type == 2:
            a = -1
            d = 1
        elif matrix_type == 3:
            b = c = 1
        elif matrix_type == 4:
            b = c = -1
        elif matrix_type == 5:
            b = 1
            c = -1
        elif matrix_type == 6:
            a = d = -1
        elif matrix_type == 7:
            b = -1
            c = 1
        else:
            raise Exception("Matrix type invalid")
        
        return a, b, c, d
        
        
        