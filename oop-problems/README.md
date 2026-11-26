# Python OOP exercises

Implement six operator overloads and three inheritance exercises from slide 67. The problem numbering skips operator exercise 3.

- [Operators](operators.py) implements complex addition and subtraction, age comparison, a vector dot product, all six circle and point comparisons, and rectangular matrix multiplication. Circles compare by radius and points by distance from the origin.
- [Inheritance](inheritance.py) demonstrates overriding `drive()` and `introduce()`, and extends a bank account with interest and balance reporting.

Run `python -m unittest discover -s oop-problems -v` from the repository root.
