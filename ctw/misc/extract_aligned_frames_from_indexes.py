import shutil
import sys
import os

import numpy as np

# TODO replicate the frames of the videos in image format


def main():
    input_folder = sys.argv[1]
    alignment_file = sys.argv[2]
    output_folder = sys.argv[3] if len(sys.argv) > 3 else input_folder

    # matlab is 1-indexed
    aligned_idx = np.loadtxt(alignment_file, delimiter=',')

    video_folders = sorted(os.listdir(input_folder))
    assert len(video_folders) == aligned_idx.shape[1], "lenght differs"

    for idx, video_folder in enumerate(video_folders):
        print idx, video_folder

        if not os.path.exists(os.path.join(output_folder, video_folder)):
            os.makedirs(os.path.join(output_folder, video_folder))

        for frame_idx, frame in enumerate(aligned_idx[:, idx]):
            source = os.path.join(input_folder, video_folder,
                                  "image_{:05d}.jpg".format(int(round(frame))))
            dest = os.path.join(output_folder, video_folder,
                                "image_{:05d}.jpg".format(frame_idx + 1))
            shutil.copyfile(source, dest)


if __name__ == '__main__':
    main()
