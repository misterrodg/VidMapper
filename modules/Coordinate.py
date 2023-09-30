import math

DEG_TO_MIN = 60
EARTH_RADIUS_NM = 3443.92


class Coordinate:
    def __init__(self, lat: float = 0.0, lon: float = 0.0):
        self.lat = lat
        self.lon = lon

    def fromDMS(
        self,
        northSouth: str,
        latD: int,
        latM: int,
        latS: float,
        eastWest: str,
        lonD: int,
        lonM: int,
        lonS: float,
    ):
        lat = latD + (latM / 60) + (latS / (60 * 60))
        if northSouth == "S":
            lat = -lat
        lon = lonD + (lonM / 60) + (lonS / (60 * 60))
        if eastWest == "W":
            lon = -lon
        self.lat = lat
        self.lon = lon

    def fromPBD(self, lat: float, lon: float, bearing: float, distance: float):
        endLat = math.asin(
            math.sin(math.radians(lat)) * math.cos(distance / EARTH_RADIUS_NM)
            + math.cos(math.radians(lat))
            * math.sin(distance / EARTH_RADIUS_NM)
            * math.cos(math.radians(bearing))
        )
        endLon = math.radians(lon) + math.atan2(
            math.sin(math.radians(bearing))
            * math.sin(distance / EARTH_RADIUS_NM)
            * math.cos(math.radians(lat)),
            math.cos(distance / EARTH_RADIUS_NM)
            - math.sin(math.radians(lat)) * math.sin(endLat),
        )
        self.lat = math.degrees(endLat)
        self.lon = math.degrees(endLon)

    def haversineGreatCicleDistance(self, endLat: float, endLon: float):
        theta = self.lon - endLon
        arc = math.degrees(
            math.acos(
                (math.sin(math.radians(self.lat)) * math.sin(math.radians(endLat)))
                + (
                    math.cos(math.radians(self.lat))
                    * math.cos(math.radians(endLat))
                    * math.cos(math.radians(theta))
                )
            )
        )
        distance = arc * DEG_TO_MIN
        return distance

    def haversineGreatCircleBearing(self, endLat: float, endLon: float):
        x = math.cos(math.radians(self.lat)) * math.sin(
            math.radians(endLat)
        ) - math.sin(math.radians(self.lat)) * math.cos(
            math.radians(endLat)
        ) * math.cos(
            math.radians(endLon - self.lon)
        )
        y = math.sin(math.radians(endLon - self.lon)) * math.cos(math.radians(endLat))
        bearing = math.degrees(math.atan2(y, x))
        bearing = math.fmod(bearing + 360, 360)
        return bearing
