from config import *
from Utilities import filehandler, practiscore, uspsa
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


## Practiscore Match ID dates/events
# 01/01/2022: 156251
# 09/07/2022: 180171 2022 SIG Sauer Carry Optics Nationals presented by Federal


# practiscore.download_all(start_id=181398, end_id=182434)
# practiscore.download_all(start_id=183968, end_id=184733)

# uspsa.update_hhf(start_with='08-05 &nbsp; &nbsp; &nbsp; Long Range Standards 2', offline=False)

# for file in os.listdir(root+'/Data/txtFiles/'):
#     path = root + '/Data/txtFiles/' + file
#     practiscore.txt_to_json(path)
# practiscore.majors_list()

# competitors = practiscore.competitor_list()

# comp_list = pd.DataFrame(columns=['firstname', 'lastname', 'uspsa', 'number', 'division', 'class', 'average_score'])


# competitors = competitors.groupby(['uspsa']).to_frame()

# competitors = competitors.groupby(['uspsa', 'division']).to_frame()

file = root + '/Data/jsonFiles/180171.json'
scores = filehandler.read_json(file)

colors = ['#3d4978', '#af3f38']
nodes = [0.0, 1.0]
cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

pts, time, hf = list(), list(), list()
for score in scores['scores']:
    if score['stage'] == 1:
        if score['stage'] != 9:
            if score['disqualify'] is True or score['dnf'] is True:
                pass
            else:
                pts.append(score['total_points']), time.append(score['time']), hf.append(score['hitfactor'])

pts = np.array(pts)
time = np.array(time)
hf = np.array(hf)

plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8), dpi=80, layout='constrained')
ax = fig.add_subplot(projection='3d')
ax.scatter(time, pts, hf, s=40, c=hf/hf.max(), cmap=cmap)
# plt.scatter(time, pts, s=40, c=hf/hf.max(), cmap=cmap)
plt.xlabel('Time (s)')
plt.ylabel('Points')
ax.text(0.5, 70, 4.5, 'Carry Optics Nationals Stage #1')
ax.set_zlabel('Hit Factor')
# plt.gca().invert_yaxis()

plt.show()


# uspsa.login_to_uspsa(password='horse*fish91L')
# print(uspsa.class_record('FY121741', 'Single Stack'))
# driver.quit()

print('Target Destroyed!')
