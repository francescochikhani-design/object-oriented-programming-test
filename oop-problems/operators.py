from dataclasses import dataclass
from functools import total_ordering
from math import hypot


@dataclass(frozen=True)
class ComplexNumber:
    real: float
    imaginary: float

    def __add__(self, other):
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)

    def __sub__(self, other):
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)


@dataclass
class Person:
    name: str
    age: int
    gender: str

    def __gt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age


@dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def __mul__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z


@total_ordering
@dataclass(frozen=True)
class Circle:
    radius: float

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Radius must be nonnegative")

    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius


@total_ordering
@dataclass(frozen=True, eq=False)
class Point:
    x: float
    y: float

    @property
    def distance(self):
        return hypot(self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance == other.distance

    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance < other.distance


class Matrix:
    def __init__(self, rows):
        self.rows = tuple(tuple(row) for row in rows)
        if not self.rows or not self.rows[0]:
            raise ValueError("A matrix must have at least one row and column")
        if any(len(row) != len(self.rows[0]) for row in self.rows):
            raise ValueError("Matrix rows must have the same length")

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("Incompatible matrix dimensions")
        columns = tuple(zip(*other.rows))
        return Matrix([
            [sum(a * b for a, b in zip(row, column)) for column in columns]
            for row in self.rows
        ])
