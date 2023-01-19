from config import *
from Application import uspsa


def cumulative_density(data):
    """
    :param data: 1D array
    :return: 2D array [data, cdf]

    Actual cumulative density function from the data
    """

    cumulative = 0
    cdf = np.zeros(len(data))

    for i in range(len(data)):
        cumulative += 1
        cdf[i] = cumulative / len(data)

    return np.vstack((data, cdf)).T


def weibull_distribution(x, lam, k, cdf=True):
    """
    :param x: x-value
    :param lam: scale parameter (l > 0)
    :param k: shape parameter (k > 0)
    :param cdf: True -> return cdf; False -> return pdf

    Weibull distribution function
    """
    if cdf is True:
        return 1 - np.exp(-1 * (x / lam) ** k)
    else:
        return k / lam * (x / lam) ** (k - 1) * np.exp(-1 * (x / lam) ** k)


def percentile(data, x):
    """
    :param x: value
    :type x: float
    :param data: all hit factors
    :type data: np.array
    :return: percentile
    :rtype: float
    """

    total = len(data)
    cdf_data = cumulative_density(data)
    fraction = np.where(cdf_data[:, 0] >= x)[0]
    return 100 - len(fraction) / total * 100


class USPSA:
    def __init__(
            self,
            code: str = None,
            title: str = None
    ):
        """
        :param code: USPSA classifier code '##-##'
        :param title: USPSA classifier name
        """

        classifier = uspsa.Classifier(code, title, hhfs=True)
        self.code = classifier.code
        self.title = classifier.title
        self.hhfs = classifier.hhfs
        self.statistics = None

    def calculate_statistics(self, start_date='01/01/18', end_date='12/21/22', file=uspsa_database):
        """
        :param start_date: start date (MM/DD/YY, unix, or datetime)
        :param end_date: end date (MM/DD/YY, unix, or datetime)
        :param file: uspsa database file path
        """
        df = pd.DataFrame(columns=['code', 'title',
                                   'div', 'total', 'avg', 'max', '100%', 'GM', 'M', 'A', 'B', 'C', 'D'])

        for i in range(0, len(self.hhfs['division'])):
            data = uspsa.read_classifier_data(self.code, self.hhfs['division'].iloc[i], start_date, end_date, file)
            stats = {'code': self.code,
                     'title': self.title,
                     'div': self.hhfs['division_abv'].iloc[i],
                     'total': len(data),
                     'avg': np.average(data),
                     'max': np.max(data),
                     '100%': 100 - percentile(data, self.hhfs['hhf'].iloc[i]),
                     'GM': 100 - percentile(data, self.hhfs['hhf'].iloc[i] * 0.95),
                     'M': 100 - percentile(data, self.hhfs['hhf'].iloc[i] * 0.85),
                     'A': 100 - percentile(data, self.hhfs['hhf'].iloc[i] * 0.75),
                     'B': 100 - percentile(data, self.hhfs['hhf'].iloc[i] * 0.60),
                     'C': 100 - percentile(data, self.hhfs['hhf'].iloc[i] * 0.40),
                     'D': 100 - percentile(data, self.hhfs['hhf'].iloc[i] * 0.02)}
            df = df.append(stats, ignore_index=True)
        self.statistics = df

    def print_statistics(self, start_date='01/01/18', end_date='12/21/22', file=uspsa_database):
        """
        :param start_date: start date (MM/DD/YY, unix, or datetime)
        :param end_date: end date (MM/DD/YY, unix, or datetime)
        :param file: uspsa database file path
        """
        if self.statistics is None:
            self.calculate_statistics(start_date, end_date, file)

        for i in range(0, len(self.statistics['div'])):
            print(uspsa.check_division(self.hhfs['division'].iloc[i]), 'statistics for stage', self.code, self.title)
            print(self.statistics['total'].iloc[i], 'Total attempts')
            print(np.round(self.statistics['avg'].iloc[i], 4), ': Average HF')
            print(self.statistics['max'].iloc[i], ': Highest HF')
            print(np.round(self.statistics['100%'].iloc[i], 2), '% : 100% Score')
            print(np.round(self.statistics['GM'].iloc[i], 2), '% : GM')
            print(np.round(self.statistics['M'].iloc[i], 2), '% : M or better')
            print(np.round(self.statistics['A'].iloc[i], 2), '% : A or better')
            print(np.round(self.statistics['B'].iloc[i], 2), '% : B or better')
            print(np.round(self.statistics['C'].iloc[i], 2), '% : C or better')
            print(np.round(self.statistics['D'].iloc[i], 2), '% : D or better')
            print('')

    def plot_cdf(self, division=None, start_date='01/01/18', end_date='12/31/22', file=uspsa_database):
        """
        :param division: division name
        :param start_date: start date (MM/DD/YY, unix, or datetime)
        :param end_date: end date (MM/DD/YY, unix, or datetime)
        :param file: uspsa database file path
        """

        def _plot(div):
            hhf = self.hhfs.loc[self.hhfs['division'] == div.upper()]['hhf'].values[0]
            data = uspsa.read_classifier_data(self.code, div, start_date, end_date, file)
            data = sorted(data)
            data = np.reshape(np.array(data), len(data))

            stats = {
                'total': len(data),
                'zeros': len(np.where(data < 0.02 * hhf)[0]),
                'D1': len(np.where((data >= 0.02 * hhf) & (data < 0.1 * hhf))[0]),
                'D2': len(np.where((data >= 0.1 * hhf) & (data < 0.2 * hhf))[0]),
                'D3': len(np.where((data >= 0.2 * hhf) & (data < 0.3 * hhf))[0]),
                'D4': len(np.where((data >= 0.3 * hhf) & (data < 0.4 * hhf))[0]),
                'C1': len(np.where((data >= 0.4 * hhf) & (data < 0.5 * hhf))[0]),
                'C2': len(np.where((data >= 0.5 * hhf) & (data < 0.6 * hhf))[0]),
                'B1': len(np.where((data >= 0.6 * hhf) & (data < 0.675 * hhf))[0]),
                'B2': len(np.where((data >= 0.675 * hhf) & (data < 0.75 * hhf))[0]),
                'A1': len(np.where((data >= 0.75 * hhf) & (data < 0.8 * hhf))[0]),
                'A2': len(np.where((data >= 0.8 * hhf) & (data < 0.85 * hhf))[0]),
                'M': len(np.where((data >= 0.85 * hhf) & (data < 0.95 * hhf))[0]),
                'GM': len(np.where((data >= 0.95 * hhf) & (data < hhf))[0]),
                'hundos': len(np.where((data >= 0.95 * hhf) & (data < hhf))[0])
            }
            hist_list = list([stats['D1'], stats['D2'], stats['D3'], stats['D4'], stats['C1'], stats['C2'],
                              stats['B1'], stats['B2'], stats['A1'], stats['A2'], stats['M'], stats['GM'],
                              stats['hundos']])

            cdf = cumulative_density(data)
            cdf_new = cumulative_density(np.delete(data, np.where(data == 0)[0]))
            cdf_frac = cdf[len(np.delete(data, np.where(data > 0)[0])), 1] * 100
            x = np.linspace(0, 1.05 * max(cdf[:, 0]), 1000)

            try:
                opt = sp.optimize.curve_fit(weibull_distribution, cdf_new[:, 0], cdf_new[:, 1],
                                            p0=[np.mean(data), np.mean(data)/3])
            except:
                converge = False
                opt = None
                print('Bell curve does not converge.')
            else:
                converge = True

            # Plot Parameters
            plt.style.use('fivethirtyeight')
            plt.rc('axes', axisbelow=True)
            fig, ax1 = plt.subplots(figsize=(8, 8), dpi=80, layout='constrained')
            ax2 = ax1.twinx()
            plt.title(self.code + ' ' + self.title + ' - ' + div)
            ax1.set_xlabel('Hit Factor')
            ax1.set_ylabel('Percentage of Shooters')
            ax2.grid(False)
            ax1.set_xlim(0, max(x))
            ax2.set_ylim([-2, 102])
            ax1.set_ylim(-2, 102)
            ax2.axes.get_yaxis().set_visible(False)

            # Plot Data
            ax2.scatter(cdf[:, 0], cdf[:, 1] * 100, color="#4591e3")

            # Plot Statistics
            ax2.text(np.mean(data) - 0.035 * max(x), 60, 'Average', rotation='vertical', color='b')
            ax2.plot([np.mean(data), np.mean(data)], [-10, 110], color='b', linewidth=1, label='Average')
            ax2.plot([hhf, hhf], [-5, 105], color='k', linewidth=3, label='HHF')
            ax2.text(hhf + 0.01 * max(x), 90, 'HHF', rotation='vertical', fontweight='bold')
            ax2.plot([hhf * 0.95, hhf * 0.95], [-5, 105], color='k', linewidth=1)
            ax2.text(hhf * 0.95 - 0.025 * max(x), 93, 'GM')
            ax2.plot([hhf * 0.85, hhf * 0.85], [-5, 105], color='k', linewidth=1)
            ax2.text(hhf * 0.85 - 0.03 * max(x), 98, 'M')
            # ax2.text(hhf * 0.85 - 0.03 * max(x), 93, 'M')
            ax2.plot([hhf * 0.75, hhf * 0.75], [-5, 105], color='k', linewidth=1)
            ax2.text(hhf * 0.75 - 0.03 * max(x), 98, 'A')
            ax2.plot([hhf * 0.60, hhf * 0.60], [-5, 105], color='k', linewidth=1)
            ax2.text(hhf * 0.60 - 0.03 * max(x), 98, 'B')
            ax2.plot([hhf * 0.4, hhf * 0.4], [-5, 105], color='k', linewidth=1)
            ax2.text(hhf * 0.40 - 0.03 * max(x), 98, 'C')

            # Plot Histogram
            ax1.add_patch(Rectangle((0, 0), 0.02 * hhf, stats['zeros'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.02 * hhf, 0), 0.1 * hhf - 0.02 * hhf, stats['D1'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.1 * hhf, 0), 0.2 * hhf - 0.1 * hhf, stats['D2'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.2 * hhf, 0), 0.3 * hhf - 0.2 * hhf, stats['D3'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.3 * hhf, 0), 0.4 * hhf - 0.3 * hhf, stats['D4'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.4 * hhf, 0), 0.5 * hhf - 0.4 * hhf, stats['C1'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.5 * hhf, 0), 0.6 * hhf - 0.5 * hhf, stats['C2'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.6 * hhf, 0), 0.675 * hhf - 0.6 * hhf, stats['B1'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.675 * hhf, 0), 0.75 * hhf - 0.675 * hhf, stats['B2'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.75 * hhf, 0), 0.8 * hhf - 0.75 * hhf, stats['A1'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.8 * hhf, 0), 0.85 * hhf - 0.8 * hhf, stats['A2'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.85 * hhf, 0), 0.95 * hhf - 0.85 * hhf, stats['M'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((0.95 * hhf, 0), hhf - 0.95 * hhf, stats['GM'] / stats['total'] * 100,
                                    facecolor='k', alpha=0.2))
            ax1.add_patch(Rectangle((hhf, 0), hhf, stats['hundos'] / stats['total'] * 100, facecolor='k', alpha=0.2))

            # Plot Distribution Curve Fit
            if converge is True:
                y2 = weibull_distribution(x, opt[0][0], opt[0][1]) * (100 - cdf_frac) + cdf_frac
                pdf2 = weibull_distribution(x, opt[0][0], opt[0][1], False) * 100
                frac = max(hist_list) / stats['total'] / np.max(pdf2) * 100
                ax2.plot(x, y2, color='k', linestyle='-', linewidth=2)
                ax2.plot(x, pdf2 * frac, color='k', linestyle='-', linewidth=2)

        if division is None:
            for i in range(0, len(self.hhfs['division'])):
                division = uspsa.check_division(self.hhfs['division'].iloc[i])
                _plot(division)
