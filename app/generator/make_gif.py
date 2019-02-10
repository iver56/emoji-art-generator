from app.settings import OUTPUT_DIR
from app.utils.files import get_subfolders
from app.utils.gif import make_gif


if __name__ == "__main__":
    """Make gif from frames in the most recent experiment folder. This can be useful if you
    stopped the experiment before it reached the gif-making phase at the end."""
    experiment_folders = get_subfolders(OUTPUT_DIR)
    experiment_folders.sort(key=lambda f: f.name)
    most_recent_experiment_folder = experiment_folders[-1]
    print(most_recent_experiment_folder)
    make_gif(most_recent_experiment_folder)
