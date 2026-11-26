# Hospital management

The organizer assigns patient problems to doctors, delivers prescriptions, collects fees, and manages member accounts.

## Task 1 · Roles

```mermaid
classDiagram
    Organizer "1" --> "0..*" Patient : registers
    Organizer "1" --> "0..*" Doctor : assigns cases
    class Patient {
        -id
        -name
        -contactAddress
        +submitProblem()
        +payFee()
    }
    class Doctor {
        -id
        -name
        -specialty
        +reviewProblem()
        +issuePrescription()
    }
    class Organizer {
        -id
        -name
        -email
        +createAccount()
        +deliverPrescription()
        +forwardFee()
    }
```

A patient has one organizer. An organizer can support any number of patients and doctors.

## Task 2 · Consultation records

```mermaid
classDiagram
    Patient "1" --> "0..*" HealthProblem : submits
    HealthProblem "1" --> "0..1" Prescription : results in
    Doctor "1" --> "0..*" Prescription : writes
    Prescription "1" --> "0..1" Payment : settled by
    Organizer ..> HealthProblem : assigns
    Organizer ..> Payment : forwards
    Payment <|-- Check
    Payment <|-- Cash
    Payment <|-- CreditCard
    class Payment {
        +amount
        +receivedAt
    }
```

A problem can await a prescription, and a prescription can await payment. Each payment has one prescription.

## Task 2 · End-to-end consultation

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    P->>O: Submit health problem
    O->>D: Request review
    D-->>O: Issue prescription
    O-->>P: Deliver prescription
    P->>O: Pay fee
    O->>D: Forward confirmed payment
    O-->>P: Send receipt
```

The organizer mediates the conversation and payment.

## Task 3 · Accounts, review history and payment strategies

```mermaid
classDiagram
    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Organizer ..> User : provisions accounts
    Patient "1" --> "0..*" HealthProblem : reports
    HealthProblem "0..*" -- "0..*" Doctor : reviewed by
    HealthProblem "1" --> "0..*" Prescription : yields
    Doctor "1" --> "0..*" Prescription : signs
    Patient "1" --> "0..*" Prescription : views history
    Prescription "0..*" --> "0..1" Prescription : renews
    Prescription "1" --> "0..*" PaymentAttempt : records
    PaymentAttempt "0..*" --> "1" PaymentMethod : uses
    PaymentMethod <|.. Cash
    PaymentMethod <|.. Check
    PaymentMethod <|.. CreditCard
    class User {
        +id
        +name
        -passwordHash
        +login()
        +logout()
    }
    class HealthProblem {
        +status
        +createdAt
        +updatedAt
    }
    class PaymentMethod {
        <<interface>>
        +collect(amount)
    }
```

Cases awaiting review can have zero reviewers. A case can later have several reviewers and several prescriptions, each signed by its own doctor. Renewals point to earlier prescriptions. Each prescription can have several payment attempts.

## Registration

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant A as Account store
    P->>O: Request membership
    O->>A: Create pending account
    A-->>O: Return ID and activation token
    O-->>P: Send activation link
    P->>A: Activate and set password
    A-->>P: Confirm account
```

The database assigns an account ID. The patient sets a password through an activation link.

## Review and prescription

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    P->>O: Submit case
    O->>O: Record Pending
    O->>D: Assign case
    O->>O: Record In review
    D->>D: Read case and prior prescriptions
    D-->>O: Return signed prescription
    O->>O: Record Resolved
    O-->>P: Deliver prescription
```

A case progresses from Pending to In review to Resolved.

## Payment outcomes

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant M as Payment strategy
    participant D as Doctor
    P->>O: Choose method and submit fee
    O->>M: Collect fee using attempt ID
    alt Accepted
        M-->>O: Confirm payment
        O->>O: Record acceptance and queue forwarding
        O->>D: Forward fee
        O-->>P: Send receipt
    else Refused
        M-->>O: Return reason
        O-->>P: Offer a new attempt
    end
```

Validate the amount first and assign a unique attempt ID. Record acceptance and queue forwarding together in the database. Retry forwarding with the same reference to avoid duplicate transfers.
