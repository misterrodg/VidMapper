from modules.Coordinate import Coordinate


class RNAVArc:
    def __init__(
        self,
        lat: float,
        lon: float,
        sides: int,
        radius: float,
        fromDegree: float,
        toDegree: float,
        rotation: float = 0,
    ):
        self.lat = lat
        self.lon = lon
        self.sides = sides
        self.radius = radius
        self.fromDegree = fromDegree
        self.toDegree = toDegree
        self.rotation = rotation
        self.feature = None
        self.draw()

    def draw(self):
        DEGREES_IN_CIRCLE = 360
        arcCenter = Coordinate(self.lat, self.lon)
        arcPoints = []
        angle = DEGREES_IN_CIRCLE / self.sides
        segments = self.sides + 1
        # Closes circle by drawingfrom final segment back to initial
        for i in range(segments):
            bearing = self.rotation + (i * angle)
            if bearing >= (self.fromDegree + self.rotation) and bearing <= (
                self.toDegree + self.rotation
            ):
                newPoint = Coordinate()
                newPoint.fromPBD(arcCenter.lat, arcCenter.lon, bearing, self.radius)
                # GeoJSON uses LON, LAT format
                arcPoints.append([newPoint.lon, newPoint.lat])
        featureObject = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": arcPoints},
            "properties": {
                "thickness": 1,
            },
        }
        self.feature = featureObject
