import sys
import numpy as np
from matplotlib import pylab as pl
from matplotlib.ticker import MultipleLocator
from wsdeval.formats.sup_corpus import iter_instances
from os.path import join as pjoin


def get_ctx_sizes(fobj):
    for _inst_id, (_word, _pos), (be, inst, af) in iter_instances(fobj):
        yield len(be) + len(inst) + len(af)


def ctx_sizes_arr(path):
    return np.fromiter(get_ctx_sizes(open(path, "rb")), dtype=np.int)


def corpus_path(base, sec):
    return pjoin(base, sec, "corpus.sup.xml")


def plot(ax, stiff_data, eurosense_data, minor_ticks=1):
    hN = ax.hist(stiff_data, bins=max(stiff_data), orientation='horizontal', rwidth=0.8, label='STIFF')
    hS = ax.hist(eurosense_data, bins=max(eurosense_data), orientation='horizontal', rwidth=0.8, label='EuroSense')

    for p in hS[2]:
        p.set_width(-p.get_width())

    xmin = min([min(w.get_width() for w in hS[2]),
                min([w.get_width() for w in hN[2]])])
    xmin = np.floor(xmin)
    xmax = max([max(w.get_width() for w in hS[2]),
                max([w.get_width() for w in hN[2]])])
    xmax = np.ceil(xmax)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim(0)
    xt = ax.get_xticks()
    s = ['%.0f' % abs(i) for i in xt]
    ax.set_xticklabels(s)
    ax.axvline(0.0)

    ax.xaxis.set_minor_locator(MultipleLocator(minor_ticks))
    ax.yaxis.set_minor_locator(MultipleLocator(minor_ticks))

    def mean_line(data, left=False):
        min_xlim, max_xlim = ax.get_xlim()
        half = - min_xlim / (max_xlim - min_xlim)
        limit_args = dict(xmax=half) if left else dict(xmin=half)
        ax.axhline(data.mean(),  color='k', linestyle='dashed', linewidth=1, **limit_args)
        text_x = min_xlim if left else max_xlim
        ax.text(text_x + (minor_ticks if left else -max_xlim * 0.2 - minor_ticks * 2), data.mean() + 1 + minor_ticks, '{:.1f}'.format(data.mean()))

    mean_line(stiff_data)
    mean_line(eurosense_data, left=True)


def main():
    stiff_path, eurosense_path = sys.argv[1:3]

    fig, (ax1, ax2) = pl.subplots(1, 2)
    fig.set_size_inches(645.0 / 72, 441.0 / 72)

    ax1.set_title('Dev')
    plot(ax1, ctx_sizes_arr(corpus_path(stiff_path, "dev")), ctx_sizes_arr(corpus_path(eurosense_path, "dev")), 5)
    ax2.set_title('Test')
    plot(ax2, ctx_sizes_arr(corpus_path(stiff_path, "test")), ctx_sizes_arr(corpus_path(eurosense_path, "test")))

    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')

    if len(sys.argv) > 3:
        pl.savefig(sys.argv[3], bbox_inches="tight")
    else:
        pl.show()


if __name__ == "__main__":
    main()
