import os

import imageio
import numpy as np

from app.utils.files import get_file_paths


def make_gif(folder, max_num_frames=16):
    frame_paths = get_file_paths(folder)
    frame_paths = [p for p in frame_paths if p.name != "target.png"]

    if len(frame_paths) > max_num_frames:
        frame_indexes = np.linspace(
            start=0, stop=len(frame_paths) - 1, endpoint=True, num=max_num_frames, dtype=np.int
        ).tolist()
        frame_indexes = set(frame_indexes)
        frame_paths = [path for i, path in enumerate(frame_paths) if i in frame_indexes]

    gif_output_path = os.path.join(folder, "evolution.gif")

    durations = [0.2] * len(frame_paths)
    durations[-1] = 1.5
    images = [imageio.imread(frame_path) for frame_path in frame_paths]
    imageio.mimsave(gif_output_path, images, duration=durations)
