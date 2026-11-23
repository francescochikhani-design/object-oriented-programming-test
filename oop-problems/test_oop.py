import unittest

from inheritance import Bicycle, Car, Employee, SavingsAccount, Student, Vehicle
from operators import Circle, ComplexNumber, Matrix, Person, Point, Vector


class OOPExercises(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(ComplexNumber(2, 3) + ComplexNumber(4, -1), ComplexNumber(6, 2))
        self.assertEqual(ComplexNumber(2, 3) - ComplexNumber(4, -1), ComplexNumber(-2, 4))
        self.assertEqual(Vector(1, 2, 3) * Vector(4, 5, 6), 32)
        product = Matrix([[1, 2, 3], [4, 5, 6]]) * Matrix([[1], [2], [3]])
        self.assertEqual(product.rows, ((14,), (32,)))
        with self.assertRaises(ValueError):
            Matrix([[1, 2]]) * Matrix([[3]])

    def test_comparisons(self):
        self.assertGreater(Person("Alice", 22, "woman"), Person("Ben", 19, "man"))
        for small, large, equal in [(Circle(1), Circle(5), Circle(5)),
                                    (Point(0, 1), Point(3, 4), Point(0, 5))]:
            self.assertLess(small, large)
            self.assertLessEqual(small, large)
            self.assertGreater(large, small)
            self.assertGreaterEqual(large, equal)
            self.assertEqual(large, equal)
            self.assertNotEqual(small, large)

    def test_overrides(self):
        self.assertEqual(Vehicle().drive(), "Driving a vehicle")
        self.assertEqual(Car().drive(), "Driving a car")
        self.assertEqual(Bicycle().drive(), "Riding a bicycle")
        self.assertIn("computer science", Student("Alex", 20, "Paris", "computer science").introduce())
        self.assertIn("Studio", Employee("Alex", 27, "Paris", "Studio").introduce())

    def test_inherited_transfer_and_interest(self):
        source = SavingsAccount("A", 100, 0.05)
        destination = SavingsAccount("B")
        self.assertTrue(source.transfer(destination, 20))
        source.add_interest()
        self.assertEqual(source.check_balance(), 84)
        self.assertEqual(destination.check_balance(), 20)
        self.assertFalse(source.transfer(destination, 90))
        self.assertEqual(source.balance, 84)
        self.assertEqual(destination.check_balance(), 20)
