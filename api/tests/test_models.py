from collections import OrderedDict
from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import HouseCode

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

    def test_dictionary_conversion(self):
        hc = HouseCode(code='FA-32')
        dict_ = OrderedDict()
        dict_['house-code'] = 'FA-32'
        dict_['relative-humidity'] = None
        dict_['temperature-opentrv'] = None
        dict_['temperature-ds18b20'] = None
        dict_['window'] = None
        dict_['switch'] = None
        dict_['last-updated-all'] = None
        dict_['last-updated-temperature'] = None
        dict_['synchronising'] = None
        dict_['ambient-light'] = None
        self.assertEqual(dict_, hc.to_dict())
