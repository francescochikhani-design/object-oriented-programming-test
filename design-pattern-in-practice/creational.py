from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from pathlib import Path
import re
from threading import Lock


class PaymentProcessor(ABC):
    @abstractmethod
    def fee(self, amount):
        pass

    @abstractmethod
    def valid(self, details):
        pass

    def process(self, amount, details):
        if amount <= 0 or not self.valid(details):
            raise ValueError("Invalid payment amount or details")
        fee = round(self.fee(amount), 2)
        return {"amount": amount, "fee": fee, "total": round(amount + fee, 2)}


class CreditCard(PaymentProcessor):
    def valid(self, details):
        return bool(re.fullmatch(r"[0-9]{16}", details.get("card_number", "")) and
                    re.fullmatch(r"[0-9]{3,4}", details.get("cvv", "")))

    def fee(self, amount):
        return amount * 0.029


class BankTransfer(PaymentProcessor):
    def valid(self, details):
        return bool(re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}",
                                 details.get("iban", "").replace(" ", "").upper()))

    def fee(self, amount):
        return 1.50


class PayPal(PaymentProcessor):
    def valid(self, details):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", details.get("email", "")))

    def fee(self, amount):
        return amount * 0.034 + 0.30


class ApplePay(PaymentProcessor):
    def valid(self, details):
        return bool(details.get("device_token"))

    def fee(self, amount):
        return amount * 0.015


class PaymentFactory:
    def __init__(self):
        self._processors = {"credit_card": CreditCard, "bank_transfer": BankTransfer,
                            "paypal": PayPal}

    def register(self, name, processor):
        self._processors[name] = processor

    def get_processor(self, name):
        try:
            processor = self._processors[name]
        except KeyError:
            raise ValueError(f"Unsupported payment method: {name}") from None
        return processor()


@dataclass(frozen=True)
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str = "TBD"
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self):
        self._fields = {}

    def identity(self, first_name, last_name, email):
        self._fields.update(first_name=first_name, last_name=last_name, email=email)
        return self

    def job(self, department, position, salary):
        self._fields.update(department=department, position=position, salary=salary)
        return self

    def options(self, **fields):
        optional = Employee.__dataclass_fields__.keys() - {
            "first_name", "last_name", "email", "department", "position", "salary"
        }
        if fields.keys() - optional:
            raise ValueError("Unknown employee option")
        self._fields.update(fields)
        return self

    def build(self):
        for field in ("first_name", "last_name", "email", "department", "position"):
            if not self._fields.get(field, "").strip():
                raise ValueError(f"Missing {field}")
        if "@" not in self._fields["email"] or not self._fields.get("salary", -1) >= 0:
            raise ValueError("Invalid email or salary")
        return Employee(**self._fields)


class DeveloperBuilder(EmployeeBuilder):
    def __init__(self):
        super().__init__()
        self.options(has_laptop=True, has_vpn_access=True, has_admin_rights=True)


class InternBuilder(EmployeeBuilder):
    def __init__(self):
        super().__init__()
        self.options(has_laptop=True, contract_type="internship")


class ConfigManager:
    _instance = None
    _lock = Lock()
    _default_path = Path(__file__).with_name("config.json")

    def __new__(cls, path=None):
        with cls._lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                with Path(path or cls._default_path).open(encoding="utf-8") as source:
                    instance._settings = json.load(source)
                cls._instance = instance
            return cls._instance

    @classmethod
    def get_instance(cls, path=None):
        return cls(path)

    @classmethod
    def reset(cls):
        with cls._lock:
            cls._instance = None

    def get(self, key, default=None):
        value = self._settings
        for segment in key.split("."):
            if not isinstance(value, dict) or segment not in value:
                return default
            value = value[segment]
        return value

    def set(self, key, value):
        node = self._settings
        *parents, name = key.split(".")
        for segment in parents:
            node = node.setdefault(segment, {})
        node[name] = value
