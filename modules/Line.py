class Line:
    def __init__(self, startLat, startLon, endLat, endLon):
        self.startLat = startLat
        self.startLon = startLon
        self.endLat = endLat
        self.endLon = endLon
        self.feature = None
        self.draw()

    def draw(self):
        # GeoJSON uses LON, LAT format
        featureObject = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [self.startLon, self.startLat],
                    [self.endLon, self.endLat],
                ],
            },
            "properties": {
                "thickness": 1,
            },
        }
        self.feature = featureObject
