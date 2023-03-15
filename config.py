import certifi
import datetime
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
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
# uspsa_database = r'E:\USPSA\Analytics\USPSAnalytics\Python\classifier_data.db'
uspsa_database = r'E:\USPSA\Analytics\CompetitionShootingAnalytics\Data\uspsa.db'
scsa_database = r'E:\USPSA\Analytics\CompetitionShootingAnalytics\Data\scsa.db'
classifier_list_file = root + r'\Data\classifier_list.csv'
classifier_hhf_file = root + r'\Data\classifiers_hhf.csv'

HEADER = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
PROXY = {'https': 'https://brd-customer-hl_6d912e82-zone-unblocker:aa0ou9yl15z7@zproxy.lum-superproxy.io:22225'}
CERTS = certifi.where()
http = urllib3.PoolManager(certs_res='CERT_REQUIRED', ca_certs=CERTS)
warnings.filterwarnings('ignore')

uspsa_divisions = (
    {'name': 'Open', 'short': 'OPN'},
    {'name': 'Limited', 'short': 'LTD'},
    {'name': 'Limited 10', 'short': 'L10'},
    {'name': 'PCC', 'short': 'PCC'},
    {'name': 'Carry Optics', 'short': 'CO'},
    {'name': 'Production', 'short': 'PROD'},
    {'name': 'Single Stack', 'short': 'SS'},
    {'name': 'Revolver', 'short': 'REV'})

scsa_divisions = (
    {'name': 'Rimfire Rifle Open', 'short': 'RFRO'},
    {'name': 'Rimfire Pistol Open', 'short': 'RFPO'},
    {'name': 'PCC Optics', 'short': 'PCCO'},
    {'name': 'Carry Optics', 'short': 'CO'},
    {'name': 'Rimfire Pistol Iron', 'short': 'RFPI'},
    {'name': 'Rimfire Rifle Iron', 'short': 'RFRI'},
    {'name': 'Open', 'short': 'OPN'},
    {'name': 'Production', 'short': 'PROD'},
    {'name': 'Limited', 'short': 'LTD'},
    {'name': 'Single Stack', 'short': 'SS'},
    {'name': 'Optical Sight Revolver', 'short': 'OSR'},
    {'name': 'PCC Iron', 'short': 'PCCI'},
    {'name': 'Iron Sight Revolver', 'short': 'ISR'})

colors = ['#3d4978', 'silver', '#af3f38']
nodes = [0.0, 0.5, 1.0]
cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
