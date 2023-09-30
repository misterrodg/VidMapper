from modules.RNAVArc import RNAVArc
from modules.Coordinate import Coordinate
from modules.Circle import Circle


class RNAV:
    def __init__(
        self, lat: float, lon: float, sides: int, radius: float, rotation: float = 0
    ):
        self.lat = lat
        self.lon = lon
        self.sides = sides
        self.radius = radius
        self.rotation = rotation
        self.featureArray = []
        self.draw()

    def draw(self):
        # These ratios are based off of trig principles.
        # For a triangle of side 1, the hypotenuse is 1.414.
        # In order to draw a circle within touching circles
        # the touching circles radius of 1, of distance 1.414
        # from the center point. The resulting inner circle
        # must be of radius 1.414 minus 1.
        ARC_RATIO = 1.414
        inner = Circle(
            self.lat,
            self.lon,
            self.sides,
            self.radius * (ARC_RATIO - 1),
            self.rotation,
        )
        self.featureArray.append(inner.feature)
        degrees = [
            {"bearing": 45, "from": 180, "to": 270},
            {"bearing": 135, "from": 270, "to": 360},
            {"bearing": 225, "from": 0, "to": 90},
            {"bearing": 315, "from": 90, "to": 180},
        ]
        for i in range(4):
            bearing = self.rotation + degrees[i]["bearing"]
            arcPoint = Coordinate()
            arcPoint.fromPBD(self.lat, self.lon, bearing, self.radius * ARC_RATIO)
            arc = RNAVArc(
                arcPoint.lat,
                arcPoint.lon,
                self.sides,
                self.radius,
                degrees[i]["from"],
                degrees[i]["to"],
                self.rotation,
            )
            self.featureArray.append(arc.feature)
