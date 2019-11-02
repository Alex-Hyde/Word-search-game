import math


class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        return Vec3(self.x // other, self.y // other, self.z // other)

    def __sub__(self, point):
        return Vec3(self.x - point.x, self.y - point.y, self.z - point.z)

    def __add__(self, point):
        return Vec3(self.x + point.x, self.y + point.y, self.z + point.z)

    def __mul__(self, cons):
        return Vec3(self.x * cons, self.y * cons, self.z * cons)

    def dot(self, point):
        return self.x * point.x + self.y * point.y + self.z * point.z

    def cross(self, other):
        return Vec3(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

    def distance(self, point):
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def unit(self):
        length = len(self)
        return Vec3(self.x/length, self.y/length, self.x/length)

    def __str__(self):
        return str(self.x) + " ," + str(self.y) + " ," + str(self.z)


class Vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vec2(self.x // other, self.y // other)

    def __sub__(self, point):
        return Vec2(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return Vec2(self.x + point.x, self.y + point.y)

    def __mul__(self, cons):
        return Vec2(self.x * cons, self.y * cons)

    def dot(self, point):
        return self.x * point.x + self.y * point.y

    def distance(self, point):
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        length = len(self)
        return Vec2(self.x/length, self.y/length)

    def __str__(self):
        return str(self.x) + " ," + str(self.y)

    def slope(self, other):
        if other.x - self.x == 0:
            return 1000000000
        return (other.y - self.y) / (other.x - self.x)

    def angle(self, other):
        angle = math.degrees(math.atan((other.y - self.y)/(other.x - self.x+0.000000001)))
        if other.x < self.x:
            return angle + 180
        if other.y < self.y:
            return angle + 360
        return angle

    def y_int(self, slope):
        return self.y - slope * self.x

    @staticmethod
    def closest_point(a, b, p):
        slope = a.slope(b)
        p2 = Vec2(p.x + 1, p.y - slope)
        return Vec2.poi(a, b, p, p2)

    @staticmethod
    def poi(a1, a2, b1, b2):
        m1 = a2.slope(a1)
        m2 = b2.slope(b1)
        d1 = a1.y_int(m1)
        d2 = b1.y_int(m2)

        x = (d2 - d1) / (m1 - m2)
        y = m1 * x + d1

        return Vec2(x, y)
