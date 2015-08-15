'''
Initiates polling of the REV2

Usage: 
  python manage.py start_polling <frequency> <house-code1> <house-code2> ... <house-coden>


'''

import os
import api.models
import rev2
import time
import sys

print sys.argv

polling_frequency = int(sys.argv[2])
house_codes = sys.argv[3:]

print polling_frequency
print house_codes

assert len(house_codes), 'input house codes'

while True:
    time.sleep(polling_frequency)
    for house_code in house_codes:
        house_code = api.models.HouseCode(code=house_code)
        rev2.rev2_interface.update_status(house_code=house_code)
        house_code.save()
    
