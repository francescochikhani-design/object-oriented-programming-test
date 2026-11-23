# ABCD Records

Regular and Royal members order CDs and tapes by mail. Royal membership adds a discount, priority, and permission to back-order unavailable items.

## Level 1 · Core use cases

```mermaid
flowchart LR
    M[Member]
    C[Order processing clerk]
    subgraph Club[ABCD Records]
        O([Place order])
        V([Verify membership])
        P([Process order])
        T([Pay invoice])
    end
    M --- O
    M --- T
    C --- V
    C --- P
    O -. include .-> V
```

Members place and pay for orders. The processing clerk verifies membership and processes orders.

## Level 1 · Core classes

```mermaid
classDiagram
    Member "1" --> "0..*" Order : places
    ProcessingClerk "0..1" --> "0..*" Order : handles
    class Order {
        +orderNumber
        +date
        +status
        +addItem()
        +total()
    }
    class Member {
        +memberId
        +name
        +address
        +placeOrder()
        +payInvoice()
    }
    class ProcessingClerk {
        +clerkId
        +name
        +email
        +verifyMembership()
        +processOrder()
    }
```

Each order belongs to one member. A newly submitted order can await clerk assignment.

## Level 2 · Expanded use cases

```mermaid
flowchart LR
    M[Member]
    N[Non-member]
    C[Order processing clerk]
    K[Collection clerk]
    subgraph Club[ABCD Records]
        O([Place order])
        V([Verify membership])
        A([Check availability])
        D([Apply Royal discount])
        B([Back-order item])
        F([Send application form])
        P([Process order])
        I([Print invoice])
        S([Print shipping list])
        R([Record daily order])
        T([Collect payment])
    end
    M --- O
    M --- T
    N --- F
    C --- V
    C --- P
    K --- T
    O -. include .-> V
    O -. include .-> A
    F -. extend .-> V
    D -. extend .-> O
    B -. extend .-> A
    P -. include .-> I
    P -. include .-> S
    P -. include .-> R
```

Membership and availability are required checks. An application is sent when membership fails. Discount and back-order extensions apply to eligible Royal orders.

## Level 2 · Expanded classes

```mermaid
classDiagram
    Member <|-- RoyalMember
    Member <|-- RegularMember
    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" CatalogItem : specifies
    CatalogItem <|-- CD
    CatalogItem <|-- Tape
    Order "1" --> "0..1" Invoice : generates
    Order "1" --> "0..1" ShippingList : generates
    Order "1" --> "0..*" Payment : has attempts
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft
    ProcessingClerk "0..1" --> "0..*" Order : handles
    CollectionClerk "1" --> "0..*" Payment : collects
    DailyRecord "0..1" --> "0..*" Order : logs
    ProcessingClerk ..> MembershipApplication : sends
    class OrderLine {
        +quantity
        +unitPrice
        +backOrdered
    }
```

An order owns one or more lines and each line references one catalog item. Orders can await their invoice or shipping list. A daily record groups all orders processed that day.

## Level 2 · Order example

```mermaid
flowchart LR
    M["member7: RoyalMember"] --> O["order42: Order"]
    O --> L1["line1: quantity 1"]
    O --> L2["line2: quantity 1, back-ordered"]
    L1 --> A["CD A: stock 5"]
    L2 --> B["CD B: stock 0"]
    O --> P["payment1: Check"]
```

Order 42 has one available CD, one back-ordered CD and a check payment.

## Level 3 · Order processing and membership verification

```mermaid
sequenceDiagram
    actor M as Customer
    participant S as Order system
    participant C as Processing clerk
    participant R as Daily record
    M->>S: Submit order request
    S->>C: Verify membership
    C-->>S: Return active membership tier
    S->>S: Check item eligibility and price by tier
    alt Items are eligible for this tier
        S->>C: Process order
        C->>S: Print invoice and shipping list
        S->>R: Append processed order
        S-->>M: Send invoice
    else An unavailable line is ineligible
        S-->>M: Request an updated order
    end
```

Accepted orders generate dispatch paperwork and appear in the daily record.

## Level 3 · Membership verification

```mermaid
sequenceDiagram
    actor M as Customer
    participant S as Order system
    participant C as Processing clerk
    M->>S: Provide membership ID
    S->>C: Look up active membership
    alt Active membership
        C-->>S: Confirm Regular or Royal tier
        S-->>M: Continue to availability check
    else Membership missing or inactive
        C-->>S: Reject membership check
        S-->>M: Send application form and decline order
    end
```

Invalid membership ends the ordering flow with an application form.

## Level 3 · Payment collection

```mermaid
sequenceDiagram
    actor M as Member
    participant C as Collection clerk
    participant S as Payment record
    M->>C: Pay invoice
    alt Cash
        C->>S: Record cash amount
    else Check
        C->>S: Record check reference
    else Bank draft
        C->>S: Record draft reference
    end
    alt Payment accepted
        S-->>C: Confirm collection
        C-->>M: Send receipt
    else Payment refused
        S-->>C: Return failure
        C-->>M: Request another payment
    end
```

The collection clerk records the outcome and sends a receipt for accepted payments.

## Level 3 · Unavailable items

```mermaid
sequenceDiagram
    actor M as Member
    participant S as Order system
    participant I as Catalog
    M->>S: Request item
    S->>I: Check stock
    I-->>S: Item unavailable
    alt Royal membership
        S->>S: Back-order line and prioritize order
        S-->>M: Confirm deferred shipment
    else Regular membership
        S-->>M: Ask customer to substitute or remove line
    end
```

Only Royal members can keep unavailable items on an order.
