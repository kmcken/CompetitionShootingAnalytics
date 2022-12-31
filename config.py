import certifi
import datetime
import json
import numpy as np
import scipy as sp
import os
import pandas as pd
import requests
import ssl
import sqlite3
import time
import uuid
import urllib3
import warnings


version = 'v0.2.2'
root = os.path.dirname(os.path.abspath(__file__))
uspsa_database = r'E:\USPSA\Analytics\USPSAnalytics\Python\classifier_data.db'
scsa_database = r'E:\USPSA\Analytics\CompetitionShootingAnalytics\Data\scsa.db'

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
PROXY = {'https': 'https://brd-customer-hl_6d912e82-zone-unblocker:aa0ou9yl15z7@zproxy.lum-superproxy.io:22225'}
CERTS = certifi.where()
http = urllib3.PoolManager(certs_res='CERT_REQUIRED', ca_certs=CERTS)
warnings.filterwarnings('ignore')
