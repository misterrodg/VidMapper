from modules.Coordinate import Coordinate


class CircleBarbs:
    def __init__(self, lat, lon, barbs, length, radius, rotation=0):
        self.lat = lat
        self.lon = lon
        self.barbs = barbs
        self.length = length
        self.radius = radius
        self.rotation = rotation
        self.featureArray = []
        self.draw()

    def draw(self):
        DEGREES_IN_CIRCLE = 360
        barbsCenter = Coordinate(self.lat, self.lon)
        angle = DEGREES_IN_CIRCLE / self.barbs
        for i in range(self.barbs):
            bearing = self.rotation + (i * angle)
            barbLine = []
            coord = Coordinate()
            coord.fromPBD(barbsCenter.lat, barbsCenter.lon, bearing, self.radius)
            # GeoJSON uses LON, LAT format
            barbLine.append([coord.lon, coord.lat])
            coord.fromPBD(coord.lat, coord.lon, bearing, self.length)
            # GeoJSON uses LON, LAT format
            barbLine.append([coord.lon, coord.lat])
            featureObject = {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": barbLine},
                "properties": {
                    "thickness": 1,
                },
            }
            self.featureArray.append(featureObject)
