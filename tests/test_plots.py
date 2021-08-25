from mindee.plots import plot_metrics


def test_plots():
    try:
        plot_metrics(["test", "test2"], [100, 90], [90, 87], './', savefig=False)
    except:
        assert False, "Plot raised Exception"
