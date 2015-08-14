import rev2
import datetime
import mock
from collections import OrderedDict
from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import HouseCode

class HouseCodeTests(TestCase):

    def test_instantiating_a_blank_house_code_raises_a_validation_error(self):

        with self.assertRaises(ValidationError):
            hc1 = HouseCode(code='')

    def test_save_can_overwrite(self):

        hc1 = HouseCode.objects.create(code='FA-32')
        hc2 = HouseCode(code='FA-32')
        hc2.save(overwrite=True)
        # does not raise error

    def test_overwrite_doesn_not_error_when_no_existing_house_code(self):

        hc1 = HouseCode(code='FA-32')
        hc1.save(overwrite=True)
        # does not raise error

    def test_full_clean_can_ignore_duplicates(self):

        hc1 = HouseCode.objects.create(code='FA-32')
        hc2 = HouseCode(code='FA-32')
        hc2.full_clean(ignore_duplication=True)
        # does not raise and error
    
    def test_duplicates_overwrite_eachother(self):
        HouseCode.objects.create(code="FA-32")
        house_code = HouseCode(code="FA-32")
        house_code.save()
        self.assertEqual(len(HouseCode.objects.all()), 1)

    def test_dictionary_conversion(self):
        hc = HouseCode(code='FA-32')
        hc.relative_humidity = None
        hc.temperature_opentrv = None
        hc.temperature_ds18b20 = None
        hc.window = None
        hc.switch = None
        hc.last_updated_all = None
        hc.last_updated_temperature = None
        hc.synchronising = None
        hc.ambient_light = None
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

