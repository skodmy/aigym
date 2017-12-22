from numpy import zeros, argmax, sum, arange, all
from matplotlib import pyplot

from aigym.backends import EmrecBackend


def plot_emrecbackend_model_prediction_matrix():
    """
    Plots EmrecBackend model's prediction matrix for used by it training data.
    """
    # Initializing EmrecBackend instance.
    emrec_backend = EmrecBackend()
    emrec_backend.build_algorithm()
    emrec_backend.create_model()
    emrec_backend.load_model()
    emrec_backend.prepared_dataset.load()

    emotion_number = len(emrec_backend.prepared_dataset.emotion_choices)

    # Calculating effectiveness
    data = zeros((emotion_number, emotion_number))
    for i in range(emrec_backend.prepared_dataset.images.shape[0]):
        result = emrec_backend.respond_on(emrec_backend.prepared_dataset.images[i])
        data[argmax(emrec_backend.prepared_dataset.images_labels[i]), result[0].tolist().index(max(result[0]))] += 1
    #
    for i in range(len(data)):
        total = sum(data[i])
        for x in range(len(data[0])):
            data[i][x] = data[i][x] / total

    # Configuring plotting
    plt_color = pyplot.pcolor(data, edgecolors='k', linewidths=4, cmap='Greens', vmin=0.0, vmax=1.0)
    plt_color.update_scalarmappable()
    ax = plt_color.axes
    ax.set_yticks(arange(emotion_number) + 0.5, minor=False)
    ax.set_xticks(arange(emotion_number) + 0.5, minor=False)
    ax.set_xticklabels(emrec_backend.prepared_dataset.emotion_choices, minor=False)
    ax.set_yticklabels(emrec_backend.prepared_dataset.emotion_choices, minor=False)
    # Populating plotting with data
    for p, color, value in zip(plt_color.get_paths(), plt_color.get_facecolors(), plt_color.get_array()):
        x, y = p.vertices[:-2, :].mean(0)
        if all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        ax.text(x, y, "%.3f" % value, ha="center", va="center", color=color)
    pyplot.xlabel("Predicted emotion")
    pyplot.ylabel("Real emotion")

    # Displaying plotted matrix
    pyplot.show()
