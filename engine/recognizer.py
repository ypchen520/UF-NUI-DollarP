import math
from .geometry import Geometry
SAMPLING_RESOLUTION = 32

class Point:
    # /// <summary>
    # /// Implements a 2D Point that exposes X, Y, and StrokeID properties.
    # /// StrokeID is the stroke index the point belongs to (e.g., 0, 1, 2, ...) that is filled by counting pen down/up events.
    # /// </summary>
    def __init__(self, x, y, strokeId):
        self.X = x
        self.Y = y
        self.StrokeID = strokeId

class Gesture:
    # /// <summary>
    # /// Constructs a gesture from an array of points
    # /// </summary>
    # /// <param name="points"></param>
    def __init__(self, points, gestureName):
        self.Name = gestureName
        # region gesture pre-processing steps: scale normalization, translation to origin, and resampling
        # normalizes the array of points with respect to scale, origin, and number of points
        self.Points = self.Scale(points)
        self.Points = self.TranslateTo(self.Points, self.Centroid(self.Points))
        self.Points = self.Resample(self.Points, SAMPLING_RESOLUTION)

    def Scale(self, points):    
        # /// <summary>
        # /// Performs scale normalization with shape preservation into [0..1]x[0..1]
        # /// </summary>
        # /// <param name="points"></param>
        # /// <returns></returns>
        minx, maxx = float("inf"), 0
        miny, maxy = float("inf"), 0
        for point in points:
            minx = min(minx, point.X)
            maxx = max(maxx, point.X)
            miny = min(miny, point.Y)
            maxy = max(maxy, point.Y)
        # print(minx, miny)
        scale = max(maxx - minx, maxy - miny)
        newPoints = []
        for point in points:
            newPoint = Point((point.X - minx) / scale, (point.Y - miny) / scale, point.StrokeID)
            newPoints.append(newPoint)
        return newPoints

    def Centroid(self, points):
        # /// <summary>
        # /// Computes the centroid for an array of points
        # /// </summary>
        # /// <param name="points"></param>
        # /// <returns></returns>
        cx, cy = 0, 0
        for point in points:
            cx = cx + point.X
            cy = cy + point.Y
        return Point(cx / len(points), cy / len(points), 0)
    def TranslateTo(self, points, cp):
        # /// <summary>
        # /// Translates the array of points by p
        # /// </summary>
        # /// <param name="points"></param>
        # /// <param name="p"></param>
        # /// <returns></returns>
        newPoints = []
        for point in points:
            newPoint = Point(point.X - cp.X, point.Y - cp.Y, point.StrokeID)
            newPoints.append(newPoint)
        return newPoints

    def PathLength(self, points):
        # /// <summary>
        # /// Computes the path length for an array of points
        # /// </summary>
        # /// <param name="points"></param>
        # /// <returns></returns>
        length = 0
        for i in range(1, len(points)):
            if points[i].StrokeID == points[i - 1].StrokeID:
                length = length + Geometry.EuclideanDistance(points[i - 1], points[i])
        return length

    def Resample(self, points, n):
        # /// <summary>
        # /// Resamples the array of points into n equally-distanced points
        # /// </summary>
        # /// <param name="points"></param>
        # /// <param name="n"></param>
        # /// <returns></returns>
        newPoints = [None]*n
        newPoints[0] = Point(points[0].X, points[0].Y, points[0].StrokeID)
        numPoints = 1
        I = self.PathLength(points) / (n - 1) # computes interval length
        D = 0
        for i in range(1, len(points)):
            if points[i].StrokeID == points[i - 1].StrokeID:
                d = Geometry.EuclideanDistance(points[i - 1], points[i])
                if D + d >= I:
                    firstPoint = points[i - 1]
                    while D + d >= I:
                        # add interpolated point
                        t = min(max((I - D) / d, 0), 1)
                        if math.isnan(t):
                            t = 0.5
                        newPoints[numPoints] = Point((1 - t) * firstPoint.X + t * points[i].X, (1 - t) * firstPoint.Y + t * points[i].Y, points[i].StrokeID)
                        numPoints = numPoints + 1
                        # update partial length
                        d = D + d - I
                        D = 0
                        firstPoint = newPoints[numPoints - 1]
                    D = d
                else:
                    D = D + d
        if numPoints == n - 1: # sometimes we fall a rounding-error short of adding the last point, so add it if so
            newPoints[numPoints] = Point(points[len(points) - 1].X, points[len(points) - 1].Y, points[len(points) - 1].StrokeID)
            numPoints = numPoints + 1
        return newPoints

class PointCloudRecognizer:
    def __init__(self):
        pass
    def Classify(self, candidate, trainingSet):
        # /// <summary>
        # /// Main function of the $P recognizer.
        # /// Classifies a candidate gesture against a set of training samples.
        # /// Returns the class of the closest neighbor in the training set.
        # /// </summary>
        # /// <param name="candidate"></param>
        # /// <param name="trainingSet"></param>
        # /// <returns></returns>
        minDistance = float("inf")
        gestureClass = ""
        for template in trainingSet:
            dist = self.GreedyCloudMatch(candidate.Points, template.Points)
            if dist < minDistance:
                minDistance = dist
                gestureClass = template.Name
        return gestureClass
        
    def GreedyCloudMatch(self, points1, points2):
        # /// <summary>
        # /// Implements greedy search for a minimum-distance matching between two point clouds
        # /// </summary>
        # /// <param name="points1"></param>
        # /// <param name="points2"></param>
        # /// <returns></returns>
        n = len(points1) # the two clouds should have the same number of points by now
        eps = 0.5        # controls the number of greedy search trials (eps is in [0..1])
        step = int(math.floor(math.pow(n, 1-eps)))
        minDistance = float("inf")
        for i in range(0, n, step):
            dist1 = self.CloudDistance(points1, points2, i) # match points1 --> points2 starting with index point i
            dist2 = self.CloudDistance(points2, points1, i) # match points2 --> points1 starting with index point i
            minDistance = min(minDistance, min(dist1, dist2))
        return minDistance
    #@staticmethod
    def CloudDistance(self, points1, points2, startIndex):
        # /// <summary>
        # /// Computes the distance between two point clouds by performing a minimum-distance greedy matching
        # /// starting with point startIndex
        # /// </summary>
        # /// <param name="points1"></param>
        # /// <param name="points2"></param>
        # /// <param name="startIndex"></param>
        # /// <returns></returns>
        n = len(points1) # the two clouds should have the same number of points by now
        matched = [0]*n  # matched[i] signals whether point i from the 2nd cloud has been already matched
        sum = 0
        i = startIndex
        while True:
            index = -1
            minDistance = float("inf")
            for j in range(n):
                if matched[j] == 0:
                    dist = Geometry.SqrEuclideanDistance(points1[i], points2[j])
                    if dist < minDistance:
                        minDistance = dist
                        index = j
            matched[index] = 1 # point index from the 2nd cloud is matched to point i from the 1st cloud
            weight = 1.0 - ((i - startIndex + n) % n) / (1.0 * n)
            sum = sum + weight * minDistance # weight each distance with a confidence coefficient that decreases from 1 to 0
            i = (i + 1) % n
            if i == startIndex:
                break
        return sum
