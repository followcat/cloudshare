import os

import services.customers
import sources.industry_id
from baseapp.datadbs import *


MED_needed = sources.industry_id.needed_medical
AI_needed = sources.industry_id.needed_ai

CUSTOMERS_PATH = 'customers'
SVC_CUSTOMERS = services.customers.Customers(CUSTOMERS_PATH, [SVC_ACCOUNT], [SVC_CO_REPO],
                                             [SVC_CV_REPO, SVC_CV_STO], [SVC_MULT_PEO])
CTM_WILLENDARE = SVC_CUSTOMERS.get('willendare')
