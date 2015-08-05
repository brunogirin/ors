import rev2
import datetime
import mock
from collections import OrderedDict
from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import HouseCode

class HouseCodeTests(TestCase):

    # TODO: move test to test_rev2.py
    # @mock.patch('rev2.connect_to_rev2')
    # def test_poll_updates_house_code(self, mock_connect):
    #     mock_ser = mock.Mock()
    #     mock_connect.return_value = mock_ser
    #     mock_ser.readline = mock.Mock()
    #     mock_ser.readline.side_effect = [
    #         '>',
    #         "'*' FA-32 FA-32 false|false|1+37 1+100 1+100 false|50|0 nzcrc",
    #     ]
        
    #     hc = HouseCode.objects.create(code='FA-32')
    #     rev2.poll(hc)

    #     now = datetime.datetime.now()
    #     self.assertEqual(hc.relative_humidity, 74)
    #     self.assertEqual(hc.temperature_opentrv, '50.000')
    #     self.assertEqual(hc.temperature_ds18b20, '25.000')
    #     self.assertEqual(hc.window, 'closed')
    #     self.assertEqual(hc.switch, 'off')
    #     self.assertTrue(now - hc.last_updated_all < datetime.timedelta(seconds=1))
    #     self.assertTrue(now - hc.last_updated_temperature < datetime.timedelta(seconds=1))
    #     self.assertEqual(hc.synchronising, 'off')
    #     self.assertEqual(hc.ambient_light, 205)
    
    def test_invalid_input_for_temperature_ds18b20(self):
        hc = HouseCode.objects.create(code='FA-32')
        hc.temperature_ds18b20 = 'asdf'
        with self.assertRaises(ValidationError) as e:
            hc.full_clean()
            hc.save()
        hc.temperature_ds18b20 = '23.3333'
        with self.assertRaises(ValidationError) as e:
            hc.full_clean()
            hc.save()
        hc.temperature_ds18b20 = '100.0'
        with self.assertRaises(ValidationError) as e:
            hc.full_clean()
            hc.save()

    def test_invalid_input_for_temperature_opentrv(self):
        hc = HouseCode.objects.create(code='FA-32')
        hc.temperature_opentrv = 'asdf'
        with self.assertRaises(ValidationError) as e:
            hc.full_clean()
            hc.save()
        hc.temperature_opentrv = '23.3333'
        with self.assertRaises(ValidationError) as e:
            hc.full_clean()
            hc.save()
        hc.temperature_opentrv = '100.0'
        with self.assertRaises(ValidationError) as e:
            hc.full_clean()
            hc.save()

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
