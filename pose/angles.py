import math
class AngleCalculator:

    def calculate(self, p1, p2, p3):
        """
        Returns angle (in degrees) formed at p2.
        """

        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y

        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2)
            - math.atan2(y1 - y2, x1 - x2)
        )

        angle = abs(angle)

        if angle > 180:
            angle = 360 - angle

        return round(angle, 2)