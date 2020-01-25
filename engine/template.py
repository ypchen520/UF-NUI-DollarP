
class Point:
    def __init__(self, x, y, stroke_id=None):
        self.x = x
        self.y = y
        self.stroke_id = stroke_id

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + '), stroke ' + str(self.stroke_id)


class Template(list):
    def __init__(self, name, points):
        self.name = name
        super(Template, self).__init__(points)


class Recognizer:
    def __init__(self, templates):
        self.templates = templates

    def recognize(self, points, n=32):
        """Recognizer main function.
        Match points against a set of templates by employing the Nearest-Neighbor classification rule.
        Parameters
        ----------
        points:
            List of Point objects.
        n:
            Number of resampled points per gesture.
        Returns
        -------
        gesture:
            Name of the recognized gesture.
        score:
            Normalized match score in [0..1] with 1 denoting perfect match.
        """
        result = None
        points = self._normalize(points, n)
        score = float("inf")

        for template in self.templates:
            template = self._normalize(template, n)
            d = self._greedy_cloud_match(points, template, n)
            if score > d:
                score = d
                result = template
        score = max((2 - score) / 2, 0)
        if result is None or score == 0:
            return None, score
        return result.name, score

    def _greedy_cloud_match(self, points, template, n):
        epsilon = 0.5  # [0..1] controls the number of tested alignments
        step = int(math.floor(n ** (1 - epsilon)))
        minimum = float("inf")

        for i in range(0, n, step):
            d_1 = self._cloud_distance(points, template, n, i)
            d_2 = self._cloud_distance(template, points, n, i)
            minimum = min(minimum, d_1, d_2)
        return minimum

    def _cloud_distance(self, points, template, n, start):
        matched = [False] * n
        sum_distance = 0
        i = start

        while True:
            minimum = float("inf")
            index = None
            for j in [x for x, b in enumerate(matched) if not b]:
                d = self._euclidean_distance(points[i], template[j])
                if d < minimum:
                    minimum = d
                    index = j
            matched[index] = True
            weight = 1 - ((i - start + n) % n) / n
            sum_distance += weight * minimum
            i = (i + 1) % n
            if i == start:
                break
        return sum_distance