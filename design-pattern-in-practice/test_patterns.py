from decimal import Decimal
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock

import behavioral as behavior
import creational as creation
import structural as structure


class DesignPatterns(unittest.TestCase):
    def test_factory_and_extension(self):
        factory = creation.PaymentFactory()
        valid_payments = {
            "credit_card": ({"card_number": "1234567890123456", "cvv": "123"}, 2.90),
            "bank_transfer": ({"iban": "FR1420041010050500013M02606"}, 1.50),
            "paypal": ({"email": "a@example.test"}, 3.70),
            "apple_pay": ({"device_token": "fixture"}, 1.50),
        }
        factory.register("apple_pay", creation.ApplePay)
        for method, (details, fee) in valid_payments.items():
            with self.subTest(method=method):
                self.assertEqual(factory.get_processor(method).process(100, details)["fee"], fee)
                with self.assertRaises(ValueError):
                    factory.get_processor(method).process(100, {})
        with self.assertRaises(ValueError):
            factory.get_processor("unknown")

    def test_builder(self):
        args = ("Ada", "Lovelace", "ada@example.test")
        developer = creation.DeveloperBuilder().identity(*args).job("IT", "Developer", 50000).build()
        intern = creation.InternBuilder().identity(*args).job("IT", "Intern", 10000).build()
        self.assertTrue(developer.has_admin_rights)
        self.assertEqual(intern.contract_type, "internship")
        self.assertFalse(intern.has_admin_rights)
        with self.assertRaises(ValueError):
            creation.EmployeeBuilder().build()

    def test_singleton(self):
        self.addCleanup(creation.ConfigManager.reset)
        with TemporaryDirectory() as folder:
            path = Path(folder, "config.json")
            path.write_text('{"database":{"host":"db"}}', encoding="utf-8")
            first = creation.ConfigManager.get_instance(path)
            path.unlink()
            second = creation.ConfigManager.get_instance(path)
            self.assertIs(first, second)
            first.set("database.port", 5432)
            self.assertEqual(second.get("database.host"), "db")
            self.assertEqual(second.get("database.port"), 5432)
            self.assertEqual(second.get("missing.value", "default"), "default")

    def test_adapter(self):
        legacy = Mock()
        legacy.generate_report.return_value = "<report><sales>150000</sales><label>A &amp; B</label></report>"
        result = structure.LegacyReportAdapter(legacy).generate({"ignored": True})
        legacy.generate_report.assert_called_once_with({"ignored": True})
        self.assertEqual(structure.AnalyticsDashboard().display(result),
                         {"sales": 150000, "label": "A & B"})

    def test_decorator_order(self):
        base = structure.BaseOrder(100)
        insured = structure.Insurance(base)
        shipped = structure.ExpressShipping(insured)
        wrapped = structure.GiftWrap(shipped)
        total = structure.PremiumMember(structure.Discount(wrapped, 15))
        self.assertEqual(total.get_cost(), Decimal("95.625"))
        self.assertIn("Insurance", total.get_description())
        self.assertNotEqual(structure.Insurance(structure.ExpressShipping(base)).get_cost(),
                            shipped.get_cost())

    def test_strategies_and_save(self):
        rows = [{"name": "A,<B>", "value": 2}]
        report = behavior.ReportGenerator(rows)
        self.assertIn('"A,<B>"', report.generate_report())
        report.set_strategy(behavior.JSONFormat())
        self.assertEqual(json.loads(report.generate_report()), rows)
        report.set_strategy(behavior.PDFFormat())
        self.assertIn("PDF REPORT", report.generate_report())
        report.set_strategy(behavior.ExcelFormat())
        self.assertIn("Name\tValue", report.generate_report())
        report.set_strategy(behavior.HTMLFormat())
        with TemporaryDirectory() as folder:
            path = report.save_report(Path(folder, "report"))
            self.assertEqual(path.suffix, ".html")
            self.assertIn("&lt;B&gt;", path.read_text(encoding="utf-8"))

    def test_pipeline_sources(self):
        load = Mock()
        csv_pipeline = behavior.CSVPipeline("id,name,age\n1,Ada,25\n", load)
        self.assertEqual(csv_pipeline.run()[0]["name"], "ADA")
        api_pipeline = behavior.APIPipeline(lambda: [{"user_id": 1, "username": "ADA", "score": 95}], load)
        self.assertEqual(api_pipeline.run()[0]["grade"], "A")
        db_source = lambda: [{"product_id": 1, "product_name": "tea", "price": "10"}]
        hook = Mock()
        db_pipeline = behavior.DatabasePipeline(db_source, load, before_load=hook)
        self.assertEqual(db_pipeline.run()[0]["tax"], 2)
        hook.assert_called_once_with()
        xml_pipeline = behavior.XMLPipeline('<orders><order order_id="3" amount="24"/></orders>', load)
        self.assertEqual(xml_pipeline.run(), [{"order_id": 3, "amount": 24.0}])
        load.assert_called_with([{"order_id": 3, "amount": 24.0}])

    def test_pipeline_cleans_up_after_invalid_data(self):
        load = Mock()
        pipeline = behavior.CSVPipeline("name\nAda\n", load)
        pipeline.cleanup = Mock()
        with self.assertRaises(ValueError):
            pipeline.run()
        pipeline.cleanup.assert_called_once()
        load.assert_not_called()
