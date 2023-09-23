class Converter:
    def tryIntParse(self, value):
        result = None
        intParse = None
        try:
            intParse = int(value)
        except ValueError as verr:
            pass
        if isinstance(intParse, int):
            result = intParse
        return result

    def tryFloatParse(self, value):
        result = None
        floatParse = None
        try:
            floatParse = float(value)
        except ValueError as verr:
            pass
        if isinstance(floatParse, float):
            result = floatParse
        return result
