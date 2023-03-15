from config import *
from Application import classifiers, uspsa, scsa
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


## Practiscore Match ID dates/events
# 01/01/2022: 156251
# 09/07/2022: 180171 2022 SIG Sauer Carry Optics Nationals presented by Federal

# practiscore.download_all(start_id=181398, end_id=182434)
# practiscore.download_all(start_id=183968, end_id=184733)


## Steel Challenge Classifier Match Results
# scsa.download_score(start_id=58609, end_id=60000)


## USPSA Classifier Match Results
# uspsa.download_score(23794, 24434)
# uspsa.download_score(51259, 51260)
# uspsa.download_score(51260, 60000)


## USPSA Analytics Classifier Analytics
# start_date = '01/01/18'
# end_date = '12/31/22'
# code = '09-07'
# classifier = classifiers.USPSA(code=code)
# classifier.print_statistics(start_date=start_date, end_date=end_date)
# classifier.plot_cdf(start_date=start_date, end_date=end_date)


## SCSA Analytics Classifier Analytics
start_date = '01/01/18'
end_date = '12/31/22'
code = 'SC-102'
classifier = classifiers.SCSA(code=code)
classifier.print_statistics(start_date=start_date, end_date=end_date)
classifier.plot_cdf(start_date=start_date, end_date=end_date)


## USPSA Analytics Classifier Count
# start_date = '01/01/22'
# end_date = '12/31/22'
#
# file = root + '/Data/classifiers_hhf.csv'
#
# df = pd.read_csv(file)
# data = uspsa.read_classifier_count(start_date, end_date)
#
# classifier_list = df['code'].unique()
# match_count = uspsa.read_match_count(start_date, end_date)
# total = len(data) + 4
#
# print('Number of Classifiers:', len(classifier_list))
# print('Number of Classifiers Shot:', total)
# print('Number of Matches:', match_count + 2)
#
# classifier_count = np.zeros(len(classifier_list))
#
# for i in range(0, len(classifier_list)):
#     for match in data:
#         if match[1] == classifier_list[i]:
#             classifier_count[i] += 1
#
# classifiers = list()
# for i in range(0, len(classifier_list)):
#     classifiers.append([classifier_list[i], classifier_count[i]])
#
# classifiers = sorted(classifiers, key=lambda x: x[1])[::-1]
# classifier_count = np.sort(classifier_count)[::-1]
# print(classifiers)
# print(classifiers[0:10])
#
# colors = ['#3d4978', '#af3f38']
# nodes = [0.0, 1.0]
# cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
#
# N = 10
# plt.style.use('fivethirtyeight')
# plt.rc('axes', axisbelow=True)
# fig, ax1 = plt.subplots(figsize=(8, 8), dpi=80, layout='constrained')
# ax1.barh(np.arange(N), classifier_count[:N] / total * 100, align='center', color='#af3f38')
# ax1.set_yticks(np.arange(N), labels='')
# ax1.set_xlabel('Number of Matches')
# ax1.set_ylabel('Classifier')
# ax1.invert_yaxis()
# ax1.text(1, 0.1, '99-53 Triple Play', c='k', fontweight='bold')
# ax1.text(1, 1.1, "99-51 Single Tap Standards", c='w', fontweight='bold')
# ax1.text(1, 2.1, '99-56 On the Upper Pad II', c='w', fontweight='bold')
# ax1.text(1, 3.1, '99-40 Close Quarter Standards', c='w', fontweight='bold')
# ax1.text(1, 4.1, '99-61 Sit Or Get Off The Shot', c='w', fontweight='bold')
# ax1.text(1, 5.1, '03-12 Ironsides', c='w', fontweight='bold')
# ax1.text(1, 6.1, "99-02 Night Moves", c='w', fontweight='bold')
# ax1.text(1, 7.1, '99-59 Lazy Man Standards', c='w', fontweight='bold')
# ax1.text(1, 8.1, "99-63 Merle's Standards", c='w', fontweight='bold')
# ax1.text(1, 9.1, "99-16 Both Sides Now #2", c='w', fontweight='bold')
# plt.title('2022 Least Used Classifiers')
#
#
# start_date = '01/01/18'
# end_date = '12/31/23'
#
# file = root + '/Data/classifiers_hhf.csv'
# df = pd.read_csv(file)
# data = uspsa.read_classifier_count(start_date, end_date)
#
# classifier_list = df['code'].unique()
# match_count = uspsa.read_match_count(start_date, end_date)
# total = len(data) + 4
#
# print('Number of Classifiers:', len(classifier_list))
# print('Number of Classifiers Shot:', total)
# print('Number of Matches:', match_count + 2)
#
# classifier_count = np.zeros(len(classifier_list))
#
# for i in range(0, len(classifier_list)):
#     for match in data:
#         if match[1] == classifier_list[i]:
#             classifier_count[i] += 1
#
# classifiers = list()
# for i in range(0, len(classifier_list)):
#     classifiers.append([classifier_list[i], classifier_count[i]])
#
# classifiers = sorted(classifiers, key=lambda x: x[1])[::-1]
# classifier_count = np.sort(classifier_count)[::-1]
# print(classifiers[0:10])
#
# colors = ['#3d4978', '#af3f38']
# nodes = [0.0, 1.0]
# cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
#
# N = 10
# plt.style.use('fivethirtyeight')
# plt.rc('axes', axisbelow=True)
# fig, ax1 = plt.subplots(figsize=(8, 8), dpi=80, layout='constrained')
# ax1.barh(np.arange(N), classifier_count[:N] / total * 100, align='center', color='#af3f38')
# ax1.set_yticks(np.arange(N), labels='')
# ax1.set_xlabel('Number of Matches')
# ax1.set_ylabel('Classifier')
# ax1.invert_yaxis()
# ax1.text(1, 0.1, '99-53 Triple Play', c='w', fontweight='bold')
# ax1.text(1, 1.1, '99-59 Lazy Man Standards', c='w', fontweight='bold')
# ax1.text(1, 2.1, "99-51 Single Tap Standards", c='w', fontweight='bold')
# ax1.text(1, 3.1, '99-40 Close Quarter Standards', c='w', fontweight='bold')
# ax1.text(1, 4.1, '99-02 Night Moves', c='w', fontweight='bold')
# ax1.text(1, 5.1, '99-56 On the Upper Pad II', c='w', fontweight='bold')
# ax1.text(1, 6.1, '99-61 Sit Or Get Off The Shot', c='w', fontweight='bold')
# ax1.text(1, 7.1, "09-10 Life's Little Problems", c='w', fontweight='bold')
# ax1.text(1, 8.1, '03-12 Ironsides', c='w', fontweight='bold')
# ax1.text(1, 9.1, "99-63 Merle's Standards", c='w', fontweight='bold')
# plt.title('2018 - 2022 Least Used Classifiers')
# plt.show()


## All Stats
# file = root + r'/Data/classifier_stats_20230118.csv'
# stages = uspsa.classifier_list()
#
# start_date = '01/01/18'
# end_date = '12/31/23'
#
# df = pd.DataFrame(columns=['code', 'title', 'div', 'total', 'avg', 'max', '100%', 'GM', 'M', 'A', 'B', 'C', 'D'])
# for i in range(0, len(stages['code'])):
#     classifier = classifiers.USPSA(stages['code'].iloc[i])
#     classifier.calculate_statistics(start_date, end_date)
#     df = df.append(classifier.statistics)
#
# df.to_csv(file)
# print(df)


## SCSA Analytics Classifier Count
# start_date = '01/01/22'
# end_date = '12/31/22'
#
# classifier_list = ['SC-101', 'SC-102', 'SC-103', 'SC-104', 'SC-105', 'SC-106', 'SC-107', 'SC-108']
# match_count = scsa.read_match_count(start_date, end_date)
# data = scsa.read_classifier_count(start_date, end_date)
# total = len(data)
#
# print('Number of Classifiers Shot:', total)
# print('Number of Matches:', match_count)
#
# classifier_count = np.zeros(len(classifier_list))
#
# for i in range(0, len(classifier_list)):
#     for match in data:
#         if match[1] == classifier_list[i]:
#             classifier_count[i] += 1
#
# classifiers = list()
# for i in range(0, len(classifier_list)):
#     classifiers.append([classifier_list[i], classifier_count[i]])
#
# print(classifiers)
# print(classifier_count)
#
# colors = ['#3d4978', '#af3f38']
# nodes = [0.0, 1.0]
# cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
#
# N = 8
# plt.style.use('fivethirtyeight')
# plt.rc('axes', axisbelow=True)
# fig, ax1 = plt.subplots(figsize=(8, 8), dpi=80, layout='constrained')
# ax1.barh(np.arange(N), classifier_count[:N], align='center', color='#3d4978')
# ax1.set_yticks(np.arange(N), labels='')
# ax1.set_xlabel('Number of Matches')
# ax1.set_ylabel('Classifier')
# ax1.invert_yaxis()
# ax1.text(10, 0.1, 'SC-101 5 to Go', c='w', fontweight='bold')
# ax1.text(10, 1.1, 'SC-102 Showdown', c='w', fontweight='bold')
# ax1.text(10, 2.1, 'SC-103 Smoke & Hope', c='w', fontweight='bold')
# ax1.text(10, 3.1, 'SC-104 Outer Limits', c='w', fontweight='bold')
# ax1.text(10, 4.1, 'SC-105 Accelerator', c='w', fontweight='bold')
# ax1.text(10, 5.1, 'SC-106 The Pendulum', c='w', fontweight='bold')
# ax1.text(10, 6.1, 'SC-107 Speed Option', c='w', fontweight='bold')
# ax1.text(10, 7.1, 'SC-108 Roundabout', c='w', fontweight='bold')
# plt.title('Steel Challenge Classifiers Shot in 2022')

plt.show()

print('Target Destroyed!')
