from config import *
from Utilities import filehandler, practiscore, uspsa, scsa
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


## Practiscore Match ID dates/events
# 01/01/2022: 156251
# 09/07/2022: 180171 2022 SIG Sauer Carry Optics Nationals presented by Federal


# practiscore.download_all(start_id=181398, end_id=182434)
# practiscore.download_all(start_id=183968, end_id=184733)


## Steel Challenge Classifier Match Results
scsa.download_score(start_id=17312, end_id=57000)

print('Target Destroyed!')
