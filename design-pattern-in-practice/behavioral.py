from abc import ABC, abstractmethod
import csv
from html import escape
from io import StringIO
import json
from pathlib import Path
import xml.etree.ElementTree as ET


class ReportFormat(ABC):
    @abstractmethod
    def format(self, rows):
        pass


class CSVFormat(ReportFormat):
    extension = "csv"

    def format(self, rows):
        output = StringIO(newline="")
        writer = csv.DictWriter(output, ("name", "value"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()


class JSONFormat(ReportFormat):
    extension = "json"

    def format(self, rows):
        return json.dumps(rows, indent=2)


class HTMLFormat(ReportFormat):
    extension = "html"

    def format(self, rows):
        body = "".join(
            f"<tr><td>{escape(str(row['name']))}</td><td>{escape(str(row['value']))}</td></tr>"
            for row in rows
        )
        return f"<table><thead><tr><th>Name</th><th>Value</th></tr></thead><tbody>{body}</tbody></table>"


class PDFFormat(ReportFormat):
    # The course's legacy formatter produces a text preview.
    extension = "txt"

    def format(self, rows):
        return "PDF REPORT\n" + "\n".join(f"{row['name']}: {row['value']}" for row in rows)


class ExcelFormat(ReportFormat):
    # A tab-delimited report can be opened directly in Excel.
    extension = "tsv"

    def format(self, rows):
        output = StringIO(newline="")
        writer = csv.writer(output, delimiter="\t", lineterminator="\n")
        writer.writerow(("Name", "Value"))
        writer.writerows((row["name"], row["value"]) for row in rows)
        return output.getvalue()


class ReportGenerator:
    def __init__(self, rows, strategy=None):
        self.rows = list(rows)
        self.strategy = strategy if strategy is not None else CSVFormat()

    def set_strategy(self, strategy):
        self.strategy = strategy

    def generate_report(self):
        return self.strategy.format(self.rows)

    def save_report(self, filename):
        path = Path(f"{filename}.{self.strategy.extension}")
        path.write_text(self.generate_report(), encoding="utf-8", newline="")
        return path


class DataPipeline(ABC):
    def __init__(self, source, load):
        self.source = source
        self.load = load

    def run(self):
        try:
            self.connect()
            rows = self.extract()
            self.validate(rows)
            transformed = [self.transform(row) for row in rows]
            self.before_load()
            self.load(transformed)
            self.after_run()
            return transformed
        finally:
            self.cleanup()

    def connect(self):
        pass

    def validate(self, rows):
        if not rows or any(not self.required_fields <= row.keys() for row in rows):
            raise ValueError("Missing records or required fields")

    def before_load(self):
        pass

    def after_run(self):
        pass

    def cleanup(self):
        pass

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, row):
        pass


class CSVPipeline(DataPipeline):
    required_fields = {"id", "name", "age"}

    def extract(self):
        return list(csv.DictReader(StringIO(self.source)))

    def transform(self, row):
        return {**row, "id": int(row["id"]), "name": row["name"].upper(),
                "age": int(row["age"])}


class APIPipeline(DataPipeline):
    required_fields = {"user_id", "username", "score"}

    def extract(self):
        return self.source()

    def transform(self, row):
        score = int(row["score"])
        return {**row, "username": row["username"].lower(), "score": score,
                "grade": "A" if score >= 90 else "B"}


class DatabasePipeline(DataPipeline):
    required_fields = {"product_id", "product_name", "price"}

    def __init__(self, source, load, before_load=lambda: None):
        super().__init__(source, load)
        self._begin_transaction = before_load

    def extract(self):
        return list(self.source())

    def before_load(self):
        self._begin_transaction()

    def transform(self, row):
        price = float(row["price"])
        return {**row, "product_name": row["product_name"].title(), "price": price,
                "tax": round(price * 0.20, 2)}


class XMLPipeline(DataPipeline):
    required_fields = {"order_id", "amount"}

    def extract(self):
        return [child.attrib for child in ET.fromstring(self.source).findall("order")]

    def transform(self, row):
        return {**row, "order_id": int(row["order_id"]), "amount": float(row["amount"])}
