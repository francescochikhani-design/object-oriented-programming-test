from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
import json
import xml.etree.ElementTree as ET


class LegacyReportGenerator:
    def generate_report(self, data):
        report = ET.Element("report")
        for name, value in data.items():
            ET.SubElement(report, name).text = str(value)
        return ET.tostring(report, encoding="unicode")


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, data):
        pass


class LegacyReportAdapter(ReportGenerator):
    def __init__(self, legacy):
        self.legacy = legacy

    def generate(self, data):
        report = ET.fromstring(self.legacy.generate_report(data))
        fields = {}
        for child in report:
            value = child.text or ""
            try:
                candidate = json.loads(value)
            except json.JSONDecodeError:
                candidate = value
            fields[child.tag] = candidate if type(candidate) in (int, float) else value
        return json.dumps(fields)


class AnalyticsDashboard:
    def display(self, json_report):
        return json.loads(json_report)


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_description(self):
        pass


class BaseOrder(OrderComponent):
    def __init__(self, price):
        self.price = Decimal(str(price))

    def get_cost(self):
        return self.price

    def get_description(self):
        return f"Base order: {self.price}"


@dataclass
class OrderDecorator(OrderComponent):
    order: OrderComponent

    @abstractmethod
    def adjustment(self, subtotal):
        pass

    def get_cost(self):
        subtotal = self.order.get_cost()
        return subtotal + self.adjustment(subtotal)

    def get_description(self):
        adjustment = self.adjustment(self.order.get_cost())
        return f"{self.order.get_description()}\n{self.label}: {adjustment:+}"


class ExpressShipping(OrderDecorator):
    label = "Express shipping"

    def adjustment(self, subtotal):
        return Decimal("15")


class GiftWrap(OrderDecorator):
    label = "Gift wrap"

    def adjustment(self, subtotal):
        return Decimal("5")


class Insurance(OrderDecorator):
    label = "Insurance"

    def adjustment(self, subtotal):
        return subtotal * Decimal("0.05")


class Discount(OrderDecorator):
    label = "Discount"

    def __init__(self, order, percent):
        super().__init__(order)
        self.percent = Decimal(str(percent))
        if not 0 <= self.percent <= 100:
            raise ValueError("Discount must be between 0 and 100")

    def adjustment(self, subtotal):
        return -subtotal * self.percent / 100


class PremiumMember(Discount):
    label = "Premium member"

    def __init__(self, order):
        super().__init__(order, 10)
