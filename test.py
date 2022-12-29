from config import *
from Utilities import filehandler, practiscore, uspsa
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import analytics


colors = ['#3d4978', '#af3f38']
nodes = [0.0, 1.0]
cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))


def linear_eq(x, a, b):
    return a * x + b


def piece_eq(x, a, b, c, x0):
    y = np.piecewise(x, [x < x0, x >= x0], [lambda x: a * x + b, lambda x: c * (x - x0) + a * x0 + b])
    return y


def quadrative(x, a, b, c):
    return a * x ** 2 + b * x + c


def cubic_eq(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


def poly_eq(x, a, b, c, d, e):
    return a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e


def power_eq(x, a, m):
    return a * x ** m


def hyperbola(x, a, b, d, e, f):
    return (a * x ** 2 + d * x + f) / (b * x + e)


def ass1(x, a, b, d, e):
    return a / b * x + (d * b - a * e) / b ** 2


file = root + '/Data/jsonFiles/184732.json'
stats_file = root + '/Data/nats_stats.json'

data = filehandler.read_json(file)
stats = filehandler.read_json(stats_file)

prcnt_open = list()
class_open = list()

for stat in stats:
    if stat['division'] == 'Open':
        prcnt_open.append(stat['percent'])
        class_open.append(stat['classification'])

prcnt_open = np.array(prcnt_open)
class_open = np.array(class_open)

prcnt_lim = list()
class_lim = list()

for stat in stats:
    if stat['division'] == 'Limited':
        prcnt_lim.append(stat['percent'])
        class_lim.append(stat['classification'])

prcnt_lim = np.array(prcnt_lim)
class_lim = np.array(class_lim)

prcnt_co = list()
class_co = list()

for stat in stats:
    if stat['division'] == 'Carry Optics':
        prcnt_co.append(stat['percent'])
        class_co.append(stat['classification'])

prcnt_co = np.array(prcnt_co)
class_co = np.array(class_co)

prcnt_pcc = list()
class_pcc = list()

for stat in stats:
    if stat['division'] == 'PCC':
        prcnt_pcc.append(stat['percent'])
        class_pcc.append(stat['classification'])

prcnt_pcc = np.array(prcnt_pcc)
class_pcc = np.array(class_pcc)

prcnt_prod = list()
class_prod = list()

for stat in stats:
    if stat['division'] == 'Production':
        prcnt_prod.append(stat['percent'])
        class_prod.append(stat['classification'])

prcnt_prod = np.array(prcnt_prod)
class_prod = np.array(class_prod)

prcnt_lim10 = list()
class_lim10 = list()

for stat in stats:
    if stat['division'] == 'Limited 10':
        prcnt_lim10.append(stat['percent'])
        class_lim10.append(stat['classification'])

prcnt_lim10 = np.array(prcnt_lim10)
class_lim10 = np.array(class_lim10)

prcnt_ss = list()
class_ss = list()

for stat in stats:
    if stat['division'] == 'Single Stack':
        prcnt_ss.append(stat['percent'])
        class_ss.append(stat['classification'])

prcnt_ss = np.array(prcnt_ss)
class_ss = np.array(class_ss)

prcnt_rev = list()
class_rev = list()

for stat in stats:
    if stat['division'] == 'Revolver':
        prcnt_rev.append(stat['percent'])
        class_rev.append(stat['classification'])

prcnt_rev = np.array(prcnt_rev)
class_rev = np.array(class_rev)
x = np.linspace(25, 100, 1000)

# Open
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8), dpi=80, layout='constrained')
plt.scatter(class_open, prcnt_open, c=np.ones(len(class_open)), cmap=cmap, label='Open')
prcnt_open = prcnt_open[class_open != 0]
class_open = class_open[class_open != 0]
class_open = class_open[prcnt_open != 0]
prcnt_open = prcnt_open[prcnt_open != 0]
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_open, prcnt_open)
# [popt, pcov] = sp.optimize.curve_fit(cubic_eq, class_open, prcnt_open)
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_open, prcnt_open, p0=[1, 0, 2, 90])
# class_open = np.insert(class_open, 0, 0, axis=0)
print('Open', popt[0] / popt[1], popt)
# print('Open', popt)
# plt.plot(x, cubic_eq(x, popt[0], popt[1], popt[2], popt[3]))
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='k', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# Limited
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8), dpi=80, layout='constrained')
plt.scatter(class_lim, prcnt_lim, c=np.ones(len(class_lim)), cmap=cmap, label='Limited')
prcnt_lim = prcnt_lim[class_lim != 0]
class_lim = class_lim[class_lim != 0]
class_lim = class_lim[prcnt_lim != 0]
prcnt_lim = prcnt_lim[prcnt_lim != 0]
# [popt, pcov] = sp.optimize.curve_fit(cubic_eq, class_lim, prcnt_lim)
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_lim, prcnt_lim)
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_lim, prcnt_lim, p0=[1, 0, 2, 90])
print('Limited', popt[0] / popt[1], popt)
# print('Limited', popt)
# plt.plot(x, cubic_eq(x, popt[0], popt[1], popt[2], popt[3]))
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='k', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# Limited 10
plt.style.use('fivethirtyeight')
plt.scatter(class_lim10, prcnt_lim10, color='#af3f38', label='Limited 10')
prcnt_lim10 = prcnt_lim10[class_lim10 != 0]
class_lim10 = class_lim10[class_lim10 != 0]
class_lim10 = class_lim10[prcnt_lim10 != 0]
prcnt_lim10 = prcnt_lim10[prcnt_lim10 != 0]
# [popt, pcov] = sp.optimize.curve_fit(hyperbola, class_lim10, prcnt_lim10, p0=[-70.4498346, -94.63971427, 6981.41745455, 9495.40017478, 9167.31831535])
[popt, pcov] = sp.optimize.curve_fit(piece_eq, class_lim10, prcnt_lim10, p0=[1, 0, 2, 90])
# class_lim10 = np.insert(class_lim10, 0, 0, axis=0)
class_lim10 = np.sort(class_lim10)
print('Limited 10', popt)
plt.plot(x, piece_eq(x, popt[0], popt[1], popt[2], popt[3]), c='r', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# Carry Optics
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8), dpi=80, layout='constrained')
plt.scatter(class_co, prcnt_co, color='#3d4978', label='Carry Optics')
prcnt_co = prcnt_co[class_co != 0]
class_co = class_co[class_co != 0]
class_co = class_co[prcnt_co != 0]
prcnt_co = prcnt_co[prcnt_co != 0]
prcnt_co = prcnt_co[class_co != 39.31]
class_co = class_co[class_co != 39.31]
prcnt_co = prcnt_co[class_co != 12.75]
class_co = class_co[class_co != 12.75]
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_co, prcnt_co)
# [popt, pcov] = sp.optimize.curve_fit(cubic_eq, class_co, prcnt_co)
# [popt1, pcov] = sp.optimize.curve_fit(linear_eq, class_co, prcnt_co, p0=[1, 0])
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_co, prcnt_co, p0=[.75, 0, 1, 85])
print('Carry Optics', popt[0] / popt[1], popt)
# print('Carry Optics', popt)
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='k', linewidth=2)
# plt.plot(x, cubic_eq(x, popt[0], popt[1], popt[2], popt[3]))
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# PCC
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8), dpi=80, layout='constrained')
plt.scatter(class_pcc, prcnt_pcc, color='#3d4978', label='PCC')
prcnt_pcc = prcnt_pcc[class_pcc != 0]
class_pcc = class_pcc[class_pcc != 0]
class_pcc = class_pcc[prcnt_pcc != 0]
prcnt_pcc = prcnt_pcc[prcnt_pcc != 0]
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_pcc, prcnt_pcc)
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_pcc, prcnt_pcc, p0=[1, 0, 2, 90])
# class_open = np.insert(class_pcc, 0, 0, axis=0)
class_open = np.sort(class_open)
print('PCC', popt[0] / popt[1], popt)
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='k', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# Production
plt.style.use('fivethirtyeight')
plt.scatter(class_prod, prcnt_prod, color='#af3f38', label='Production')
prcnt_prod = prcnt_prod[class_prod != 0]
class_prod = class_prod[class_prod != 0]
class_prod = class_prod[prcnt_prod != 0]
prcnt_prod = prcnt_prod[prcnt_prod != 0]
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_prod, prcnt_prod)
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_prod, prcnt_prod, p0=[1, 0, 2, 90])
# class_prod = np.insert(class_prod, 0, 0, axis=0)
class_prod = np.sort(class_prod)
print('Production', popt[0] / popt[1], popt)
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='r', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# Single Stack
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(8, 8), dpi=80, layout='constrained')
plt.scatter(class_ss, prcnt_ss, color='#3d4978', label='Single Stack')
prcnt_ss = prcnt_ss[class_ss != 0]
class_ss = class_ss[class_ss != 0]
class_ss = class_ss[prcnt_ss != 0]
prcnt_ss = prcnt_ss[prcnt_ss != 0]
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_ss, prcnt_ss, p0=[-70.4498346, -94.63971427, 6981.41745455, 9495.40017478, 9167.31831535])
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_ss, prcnt_ss, p0=[1, 0, 2, 90])
# class_ss = np.insert(class_ss, 0, 0, axis=0)
class_ss = np.sort(class_ss)
print('Single Stack', popt[0] / popt[1], popt)
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='k', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()


# Revolver
plt.style.use('fivethirtyeight')
plt.scatter(class_rev, prcnt_rev, color='#af3f38', label='Revolver')
prcnt_rev = prcnt_rev[class_rev != 0]
class_rev = class_rev[class_rev != 0]
class_rev = class_rev[prcnt_rev != 0]
prcnt_rev = prcnt_rev[prcnt_rev != 0]
[popt, pcov] = sp.optimize.curve_fit(hyperbola, class_rev, prcnt_rev)
# [popt, pcov] = sp.optimize.curve_fit(piece_eq, class_rev, prcnt_rev, p0=[1, 0, 2, 90])
# class_rev = np.insert(class_rev, 0, 0, axis=0)
class_rev = np.sort(class_rev)
print('Revolver', popt[0] / popt[1], popt)
plt.plot(x, hyperbola(x, popt[0], popt[1], popt[2], popt[3], popt[4]), c='r', linewidth=2)
plt.ylabel('Match Finish Percent')
plt.xlabel('Classification Percent')
plt.xlim([-5, 105])
plt.ylim([-5, 105])
plt.title('2022 USPSA Nationals vs. Classification')
plt.legend()

plt.show()

print('Target Destroyed!')
