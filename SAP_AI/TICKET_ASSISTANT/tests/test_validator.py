import tempfile
import unittest
from pathlib import Path
from modules.validator import Validator, ValidationError


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = Validator(r"^[A-Za-z]{2,10}[0-9]{3,12}$")
        self.steps = [
            {"step_number": 1, "status": "PENDING"},
            {"step_number": 2, "status": "PENDING"},
        ]

    def test_ticket_normalization(self):
        self.assertEqual(self.validator.ticket_id("inc123456"), "INC123456")

    def test_prevents_skipping(self):
        with tempfile.NamedTemporaryFile(suffix='.png') as image:
            image.write(b'x')
            image.flush()
            with self.assertRaises(ValidationError):
                self.validator.can_complete(self.steps, 2, image.name)

    def test_closure_rejects_pending(self):
        with self.assertRaises(ValidationError):
            self.validator.can_close(self.steps)


if __name__ == '__main__':
    unittest.main()
