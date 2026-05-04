import math

class SmoothCursor:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.x = 0
        self.y = 0
        self.initialized = False

    def update(self, x, y):
        if not self.initialized:
            self.x, self.y = x, y
            self.initialized = True
            return x, y

        self.x = self.alpha * x + (1 - self.alpha) * self.x
        self.y = self.alpha * y + (1 - self.alpha) * self.y

        return int(self.x), int(self.y)


def distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5