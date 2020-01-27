import math
#from .recognizer import Point

class Geometry:
    def __init__(self):
        pass
    @staticmethod
    def EuclideanDistance(a, b):
        # /// <summary>
        # /// Computes the Euclidean Distance between two points in 2D
        # /// </summary>
        return math.sqrt(Geometry.SqrEuclideanDistance(a, b))
    @staticmethod    
    def SqrEuclideanDistance(a, b):
        # /// <summary>
        # /// Computes the Squared Euclidean Distance between two points in 2D
        # /// </summary>
        return (a.X - b.X) * (a.X - b.X) + (a.Y - b.Y) * (a.Y - b.Y)