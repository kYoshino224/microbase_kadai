class Line:
    def __init__(self, x1, y1, x2, y2):
        self.gradient = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')
        self.intercept = y1 - self.gradient * x1 if self.gradient != float('inf') else None

    def y(self, x):
        if self.gradient == float('inf'):
            return None
        return self.gradient * x + self.intercept