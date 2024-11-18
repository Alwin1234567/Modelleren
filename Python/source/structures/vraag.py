import warnings

class Vraag(list):
    def __init__(self, values):
        if not all(isinstance(v, int) for v in values):
            raise ValueError("All values must be integers.")
        
        if len(values) > 7:
            raise ValueError("There can be at most 7 values.")
        
        if len(values) < 7:
            warnings.warn("Fewer than 7 values provided, filling with 0.")
            values.extend([0] * (7 - len(values)))
        
        super().__init__(values)

    @property
    def monday(self):
        return self[0]

    @property
    def tuesday(self):
        return self[1]

    @property
    def wednesday(self):
        return self[2]

    @property
    def thursday(self):
        return self[3]

    @property
    def friday(self):
        return self[4]

    @property
    def saturday(self):
        return self[5]

    @property
    def sunday(self):
        return self[6]
