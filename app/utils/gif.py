import os

import imageio

from app.utils.files import get_file_paths


def make_gif(folder, use_every_n=9):
    frame_paths = get_file_paths(folder)
    frame_paths = [path for i, path in enumerate(frame_paths) if i % use_every_n == 0]
    gif_output_path = os.path.join(folder, "evolution.gif")
    with imageio.get_writer(gif_output_path, mode="I") as writer:
        for frame_path in frame_paths:
            image = imageio.imread(frame_path)
            writer.append_data(image)
