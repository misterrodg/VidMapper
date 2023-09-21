from modules.Coordinate import Coordinate


class Circle:
    def __init__(self, lat, lon, sides, radius, rotation=0):
        self.lat = lat
        self.lon = lon
        self.sides = sides
        self.radius = radius
        self.rotation = rotation
        self.feature = None
        self.draw()

    def draw(self):
        DEGREES_IN_CIRCLE = 360
        circleCenter = Coordinate(self.lat, self.lon)
        circlePoints = []
        angle = DEGREES_IN_CIRCLE / self.sides
        segments = self.sides + 1
        # Closes circle by drawingfrom final segment back to initial
        for i in range(segments):
            bearing = self.rotation + (i * angle)
            newPoint = Coordinate()
            newPoint.fromPBD(circleCenter.lat, circleCenter.lon, bearing, self.radius)
            # GeoJSON uses LON, LAT format
            circlePoints.append([newPoint.lon, newPoint.lat])
        featureObject = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": circlePoints},
            "properties": {
                "thickness": 1,
            },
        }
        self.feature = featureObject
