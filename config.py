import datetime
import json
import numpy as np
import scipy as sp
import os
import pandas as pd
import requests
import time
import uuid


version = 'v0.2.2'
root = os.path.dirname(os.path.abspath(__file__))
database_file = 'E:\USPSA\Analytics\USPSAnalytics\Python\classifier_data.db'

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
PROXY = {'https': 'https://brd-customer-hl_6d912e82-zone-unblocker:aa0ou9yl15z7@zproxy.lum-superproxy.io:22225'}
