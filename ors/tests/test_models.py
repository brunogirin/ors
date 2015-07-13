from django.test import TestCase
from django.core.exceptions import ValidationError
from ors.models import HouseCode

class HouseCodeTests(TestCase):

    def test_duplicates_throw_validation_error(self):
        HouseCode.objects.create(code="housecode1")
        house_code = HouseCode(code="housecode1")
        with self.assertRaises(ValidationError):
            house_code.full_clean()
            house_code.save()

    def test_empty_input_throws_validation_error(self):
        house_code = HouseCode(code="")
        with self.assertRaises(ValidationError):
            house_code.full_clean()
            house_code.save()

