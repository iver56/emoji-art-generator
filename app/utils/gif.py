import os

import imageio

from app.utils.files import get_file_paths


def make_gif(folder, use_every_n=20, include_last_frame=True):
    frame_paths = get_file_paths(folder)
    frame_paths = [
        path
        for i, path in enumerate(frame_paths)
        if (include_last_frame and i == len(frame_paths) - 1) or i % use_every_n == 0
    ]
    gif_output_path = os.path.join(folder, "evolution.gif")

    durations = [0.166] * len(frame_paths)
    durations[-1] = 1.0
    images = [imageio.imread(frame_path) for frame_path in frame_paths]
    imageio.mimsave(gif_output_path, images, duration=durations)
