from config import *
from Utilities import filehandler
from Application import uspsa, scsa, classifiers
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib
import re
from textwrap import wrap
import sys

colors = ['#3d4978', 'lightgrey', '#af3f38']
nodes = [0.0, 0.6, 1.0]
cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

# year = 22
# start_date = '1/01/' + str(year)
# end_date = '1/01/' + str(year + 1)
#
# memlist = uspsa.read_member_list(start_date, end_date)
# # blacklist = []
# #
# # for item in blacklist:
# #     try:
# #         memlist.remove(item)
# #     except ValueError:
# #         pass
#
# div_list = ['Open', 'Carry Optics', 'Limited', 'PCC', 'Production', 'Single Stack', 'Revolver', 'Limited 10']
# # div_list = ['PCC']
# gm_count = {'Total': 0, 'Open': 0, 'Carry Optics': 0, 'Limited': 0, 'PCC': 0, 'Production': 0,
#             'Single Stack': 0, 'Revolver': 0, 'Limited 10': 0}
#
# N = len(memlist)
# t = time.time()
# GM_total = 0
#
# for i in range(0, N):
#     memnum = memlist[i]
#     # time.sleep(1)
#     print(np.round(i / N * 100, 3), '%:', memnum)
#     isGM = False
#     for div in div_list:
#         memclass = uspsa.read_member_classification_list(start_date=start_date, end_date=end_date,
#                                                          member_number=memnum, division=div)
#         # print(div, memclass)
#         classification = 'GM'
#         gm = 0
#
#         if len(memclass) > 1:
#             if memclass[-1][0] == 'GM' and memclass[0][0] != 'GM':
#                 # print(memclass)
#                 # if input('Is GM?'):
#                 gm_count[div] += 1
#                 gm_count['Total'] += 1
#                 isGM = True
#             if memclass[-1][0] == 'GM' and memclass[0][0] == 'GM':
#                 isGM = True
#     if isGM is True:
#         GM_total += 1
#         # for i in range(0, len(memclass)):
#         #     if memclass[i][0] == 'GM':
#         #         if i != 0 and memclass[i - 1][0] == 'GM':
#         #             gm += 1
#         # if gm >= 2:
#         #     gm_count[div] += 1
#     # print(gm)
#     # print(gm_count)
#
# elapsed = time.time() - t
# print(np.round(elapsed, 2), 'seconds')
# print(gm_count)
# print('Total GMs:', GM_total)

# file = r'E:\USPSA\Analytics\CompetitionShootingAnalytics\Data\newgm.csv'
#
# years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
# df = pd.read_csv(file)
# print(df)
# # activity = df['total'].values.tolist()
# # OPN = df["opn_norm"].values.tolist()
# # CO = df["co_norm"].values.tolist()
# # LTD = df["ltd_norm"].values.tolist()
# # PCC = df["pcc_norm"].values.tolist()
# # PROD = df["prod_norm"].values.tolist()
# # SS = df["ss_norm"].values.tolist()
# # REV = df["rev_norm"].values.tolist()
# # L10 = df["l10_norm"].values.tolist()
# activity = df['total'].values.tolist()
# OPN = df["opn"].values.tolist()
# CO = df["co"].values.tolist()
# LTD = df["ltd"].values.tolist()
# PCC = df["pcc"].values.tolist()
# PROD = df["prod"].values.tolist()
# SS = df["ss"].values.tolist()
# REV = df["rev"].values.tolist()
# L10 = df["l10"].values.tolist()
#
# colors = cmap(np.linspace(1, 0, 8))
#
# # title = 'New GMs per Year'
# title = 'New GMs Normalized to USPSA Membership'
# plt.style.use('fivethirtyeight')
# fig, ax = plt.subplots(figsize=(8, 8), dpi=80, layout='constrained')
# ax.bar(years, OPN, label='Open', color=colors[0],
#        bottom=np.array(L10) + np.array(REV) + np.array(SS) + np.array(PROD) + np.array(LTD))
#        # bottom=np.array(L10) + np.array(REV) + np.array(SS) + np.array(PROD) + np.array(PCC) + np.array(LTD) + np.array(CO))
# # ax.bar(years, CO, label='Carry Optics', color=colors[1],
# #        bottom=np.array(L10) + np.array(REV) + np.array(SS) + np.array(PROD) + np.array(PCC) + np.array(LTD))
# ax.bar(years, LTD, label='Limited', color=colors[2],
#        bottom=np.array(L10) + np.array(REV) + np.array(SS) + np.array(PROD))
#        # bottom=np.array(L10) + np.array(REV) + np.array(SS) + np.array(PROD) + np.array(PCC))
# # ax.bar(years, PCC, label='PCC', color=colors[3],
# #        bottom=np.array(L10) + np.array(REV) + np.array(SS) + np.array(PROD))
# ax.bar(years, PROD, label='Production', color=colors[4],
#        bottom=np.array(L10) + np.array(REV) + np.array(SS))
# ax.bar(years, SS, label='Single Stack', color=colors[5],
#        bottom=np.array(L10) + np.array(REV))
# ax.bar(years, REV, label='Revolver', color=colors[6],
#        bottom=np.array(L10))
# ax.bar(years, L10, label='L10', color=colors[7])
# # ax2 = ax.twinx()
# # x = np.linspace(0, 9, 10)
# # ax2.plot(x, np.array(activity), color='k')
# # ax2.grid(False)
# # ax2.set_ylim([0, 70900])
# # ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
# # ax2.set_ylabel('Active USPSA Members')
# ax.set_ylabel('Number of New GMs')
# ax.set_xlabel('Year')
# # ax.set_ylabel('Number of New GMs Normalized')
# # ax.set_ylim([0, 15000])
# if title is not None:
#     ax.set_title(title)
# ax.legend()

plt.show()
print('Target Destroyed!')
