'''
Initiates polling of the REV2

Usage: 
  python manage.py start_polling <frequency> <house-code1> <house-code2> ... <house-coden>


'''

import cPickle
import rev2

with open(rev2.BackgroundPoller.PKL_LOCATION, 'rb') as f:
    bg_poller = cPickle.load(f)

bg_poller.start(bg=False)

# import os
# import api.models
# import time
# import sys

# polling_frequency = int(sys.argv[2])
# house_codes = sys.argv[3:]

# assert len(house_codes), 'input house codes'

# while True:
#     time.sleep(polling_frequency)
#     for house_code in house_codes:
#         house_code = api.models.HouseCode.objects.get(code=house_code)
#         rev2.rev2_interface.update_status(house_code=house_code)
#         house_code.save()
    
