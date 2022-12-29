import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def cdf_fun(data):
    """
    Calculates the cumulative density function from raw data.

    :param data: 1-D array
    :type data: np.array
    :return: 2-D array [data, cdf]
    :rtype: np.array
    """

    cumulative = 0
    cdf = np.zeros(len(data))

    for i in range(len(data)):
        cumulative += 1
        cdf[i] = cumulative / len(data)

    return np.vstack((data, cdf)).T


def precentile(hf, data):
    """
    Calculates percentiles given the read data.

    :param hf: hit factor
    :type hf: float
    :param data: all hit factors
    :type data: np.array
    :return: percentile
    :rtype: float
    """

    total = len(data)
    cdf_data = cdf_fun(data)
    fraction = np.where(cdf_data[:, 0] >= hf)[0]
    return len(fraction) / total * 100


def print_statistics(data, stage, div, hhf):
    gm = np.round(hhf * 0.95, 4)
    m = np.round(hhf * 0.85, 4)
    a = np.round(hhf * 0.75, 4)
    b = np.round(hhf * 0.60, 4)
    c = np.round(hhf * 0.40, 4)
    print(div, 'statistics for stage', stage)
    print(len(data), 'attempts')
    print(np.round(np.max(data), 4), ': Highest HF')
    print(np.round(np.mean(data), 4), ': Average HF')
    print(str(np.round(precentile(hhf, data), 2)) + '%', ': Score of 100%')
    print(str(np.round(100 - stats.percentileofscore(data, gm), 2)) + '%', ': GM')
    print(str(np.round(100 - stats.percentileofscore(data, m), 2)) + '%', ': M or better')
    print(str(np.round(100 - stats.percentileofscore(data, a), 2)) + '%', ': A or better')
    print(str(np.round(100 - stats.percentileofscore(data, b), 2)) + '%', ': B or better')
    print(str(np.round(100 - stats.percentileofscore(data, c), 2)) + '%', ': C or better')
    print('')


def hhf_what_if(stage, division, data, hhf, gm_pct=1, stats=True):
    if stats is True:
        print_statistics(data, stage, division, hhf)

    print('Actual HHF:', hhf)
    print('Recommended HHF:',
          str(np.round(np.percentile(data, 100 - gm_pct) / 0.95, 4)),
          'if GM is the top', str(np.round(gm_pct, 2)) + '%', )
    print('')


def generate_cdf(stage, division, data, hhf):
    colors = ['#3d4978', 'silver', '#af3f38']
    nodes = [0.0, 0.5, 1.0]

    def distribution_weibull(x, l, k, cdf=True):
        if cdf is True:
            return 1 - np.exp(-1 * (x / l) ** k)
        else:
            return k / l * (x / l) ** (k - 1) * np.exp(-1 * (x / l) ** k)

    cdf = cdf_fun(data)
    cdf_new = cdf_fun(np.delete(data, np.where(data == 0)[0]))

    converge = False
    try:
        poptw, pcow = optimize.curve_fit(distribution_weibull, cdf_new[:, 0], cdf_new[:, 1], p0=[np.mean(data), np.mean(data)/3])
    except:
        print('Bell curve does not converge.')
    else:
        converge = True

    total = len(data)
    zeros = len(np.where(data < 0.02 * hhf)[0])
    D1s = len(np.where((data >= 0.02 * hhf) & (data < 0.1 * hhf))[0])
    D2s = len(np.where((data >= 0.1 * hhf) & (data < 0.2 * hhf))[0])
    D3s = len(np.where((data >= 0.2 * hhf) & (data < 0.3 * hhf))[0])
    D4s = len(np.where((data >= 0.3 * hhf) & (data < 0.4 * hhf))[0])
    C1s = len(np.where((data >= 0.4 * hhf) & (data < 0.5 * hhf))[0])
    C2s = len(np.where((data >= 0.5 * hhf) & (data < 0.6 * hhf))[0])
    B1s = len(np.where((data >= 0.6 * hhf) & (data < 0.675 * hhf))[0])
    B2s = len(np.where((data >= 0.675 * hhf) & (data < 0.75 * hhf))[0])
    A1s = len(np.where((data >= 0.75 * hhf) & (data < 0.8 * hhf))[0])
    A2s = len(np.where((data >= 0.8 * hhf) & (data < 0.85 * hhf))[0])
    Ms = len(np.where((data >= 0.85 * hhf) & (data < 0.95 * hhf))[0])
    GMs = len(np.where((data >= 0.95 * hhf) & (data < hhf))[0])
    hundos = len(np.where((data >= 0.95 * hhf) & (data < hhf))[0])
    hist_list = [D1s, D2s, C1s, C2s, B1s, B2s, A1s, A2s, Ms, GMs, hundos]

    x = np.linspace(0, 1.05 * max(cdf[:, 0]), 1000)
    cdf_frac = cdf[len(np.delete(data, np.where(data > 0)[0])), 1] * 100

    if converge is True:
        y2 = distribution_weibull(x, poptw[0], poptw[1]) * (100 - cdf_frac) + cdf_frac
        pdf2 = distribution_weibull(x, poptw[0], poptw[1], False) * 100
        frac = max(hist_list) / total / np.max(pdf2) * 100

    plt.style.use('fivethirtyeight')
    plt.rc('axes', axisbelow=True)
    fig, ax1 = plt.subplots(figsize=(8, 8), dpi=80, layout='constrained')
    ax2 = ax1.twinx()
    plt.title(stage + ' - ' + division)
    ax1.set_xlabel('Hit Factor')
    ax1.set_ylabel('Percentage of Shooters')
    ax2.grid(False)
    ax2.text(np.mean(data) - 0.035 * max(x), 60, 'Average', rotation='vertical', color='b')
    ax2.plot([np.mean(data), np.mean(data)], [-10, 110], color='b', linewidth=1, label='Average')
    ax2.scatter(cdf[:, 0], cdf[:, 1] * 100, color="#4591e3")
    ax1.add_patch(Rectangle((0, 0), 0.02 * hhf, zeros / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.02 * hhf, 0), 0.1 * hhf - 0.02 * hhf, D1s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.1 * hhf, 0), 0.2 * hhf - 0.1 * hhf, D2s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.2 * hhf, 0), 0.3 * hhf - 0.2 * hhf, D3s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.3 * hhf, 0), 0.4 * hhf - 0.3 * hhf, D4s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.4 * hhf, 0), 0.5 * hhf - 0.4 * hhf, C1s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.5 * hhf, 0), 0.6 * hhf - 0.5 * hhf, C2s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.6 * hhf, 0), 0.675 * hhf - 0.6 * hhf, B1s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.675 * hhf, 0), 0.75 * hhf - 0.675 * hhf, B2s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.75 * hhf, 0), 0.8 * hhf - 0.75 * hhf, A1s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.8 * hhf, 0), 0.85 * hhf - 0.8 * hhf, A2s / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.85 * hhf, 0), 0.95 * hhf - 0.85 * hhf, Ms / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((0.95 * hhf, 0), hhf - 0.95 * hhf, GMs / total * 100, facecolor='k', alpha=0.2))
    ax1.add_patch(Rectangle((hhf, 0), hhf, GMs / total * 100, facecolor='k', alpha=0.2))
    # ax2.plot(x, y * (100 - cdf_frac) + cdf_frac, color='k', linestyle='-', linewidth=2)
    if converge is True:
        ax2.plot(x, y2, color='k', linestyle='-', linewidth=2)
        ax2.plot(x, pdf2 * frac, color='k', linestyle='-', linewidth=2)
    # plt.xticks(np.arange(0, max(x), 10))
    ax1.set_xlim(0, max(x))
    ax2.set_ylim([-2, 102])
    ax1.set_ylim(-2, 102)
    ax2.axes.get_yaxis().set_visible(False)

    ax2.plot([hhf, hhf], [-5, 105], color='k', linewidth=3, label='HHF')
    ax2.text(hhf + 0.01 * max(x), 90, 'HHF', rotation='vertical', fontweight='bold')
    ax2.plot([hhf * 0.95, hhf * 0.95], [-5, 105], color='k', linewidth=1)
    # ax2.text(hhf * 0.95 - 0.025 * max(x), 98, 'GM')
    ax2.text(hhf * 0.95 - 0.025 * max(x), 90, 'GM')
    ax2.plot([hhf * 0.85, hhf * 0.85], [-5, 105], color='k', linewidth=1)
    ax2.text(hhf * 0.85 - 0.03 * max(x), 98, 'M')
    # ax2.text(hhf * 0.85 - 0.03 * max(x), 90, 'M')
    ax2.plot([hhf * 0.75, hhf * 0.75], [-5, 105], color='k', linewidth=1)
    ax2.text(hhf * 0.75 - 0.03 * max(x), 98, 'A')
    ax2.plot([hhf * 0.60, hhf * 0.60], [-5, 105], color='k', linewidth=1)
    ax2.text(hhf * 0.60 - 0.03 * max(x), 98, 'B')
    ax2.plot([hhf * 0.4, hhf * 0.4], [-5, 105], color='k', linewidth=1)
    ax2.text(hhf * 0.40 - 0.03 * max(x), 98, 'C')

