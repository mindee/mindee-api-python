import matplotlib.pyplot as plt


def autolabel(ax, rects):
    """
    :param ax: Matplotlib ax
    :param rects: Matplotlib rectangles from chart's bars
    :return:
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height-height/10),
                    xytext=(0, 3), fontSize=5, color="#ffffff",
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=90)


def plot_metrics(metrics, accuracies, precisions, save_path, savefig=True):
    """
    :param savefig: Boolean to specify whether saving the plot as a png file or not
    :param metrics: List of metrics names
    :param accuracies: List of accuracy values
    :param precisions: List of precision values
    :param save_path: Path to save the figure
    :return: the plt object
    """
    x_range = [float(k) for k in range(len(metrics))]  # the label locations
    width = 0.4  # the width of the bars

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.15)
    rects1 = ax.bar([x - width / 2 for x in x_range], accuracies, width, color='#fd3246', label='Accuracy')
    rects2 = ax.bar([x + width / 2 for x in x_range], precisions, width, color='#007af9', label='Precision')

    autolabel(ax, rects1)
    autolabel(ax, rects2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('%')
    ax.set_title('Metrics')
    ax.set_xticks(x_range)
    ax.set_xticklabels(metrics, rotation=45, fontsize=6)
    ax.legend(loc='lower left')
    plt.grid(True, linestyle='--', color='#e1e1e1', alpha=0.4)

    if savefig:
        plt.savefig(save_path, dpi=300)

    return plt