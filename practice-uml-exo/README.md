# UML practice

Model the consultation service and the mail-order record club from slide 68. Open either Markdown file on GitHub to view the diagrams. Read a sequence diagram from top to bottom and follow each message between lifelines. Branches labeled `alt` represent different outcomes.

- [Hospital management](hospital.md) covers the initial roles, consultation and payments, and the expanded model.
- [ABCD Records](abcd_records.md) covers use cases, classes, an example order, and the order and payment scenarios.

On a class diagram, `1` means exactly one, `0..1` means optional, `0..*` means any number and `1..*` means one or more. Read the number at one end as the number of instances at that end per single instance at the other end. A line is an association, the hollow triangle points to a parent class, and a dashed line with a hollow triangle points to an interface. A filled diamond marks composition at the owner end. A dashed dependency shows that a class uses another in an operation. In the use-case diagrams, `include` points to a required substep and `extend` points to a base use case augmented under a condition.
