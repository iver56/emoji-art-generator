# Emoji Art Generator

| Description | Image |
| ----------- | ----- |
| Target image | ![Target image](data/target_images/sunglasses2.png) |
| RGB MSE fitness | ![Evolved emoji image](demo/rgb_mse.gif) |
| LAB MSE fitness | ![Evolved emoji image](demo/lab_mse.gif) |
| LAB Delta E CIE 2000 fitness | ![Evolved emoji image](demo/lab_delta_e.gif) |
| LAB Delta E CIE 2000 combined with SSIM fitness | ![Evolved emoji image](demo/lab_delta_e_ssim.gif) |
| SSIM fitness | ![Evolved emoji image](demo/ssim.gif) |

# Setup

* `conda env create`

# Usage

Prepare a target image (store it in `data/target_images/`) and a set of emojies/tiles (store them in `data/emoji/`). Then run the following command:

`python -m app.generator.generate`

```
usage: generate.py [-h] [--starting-canvas STARTING_CANVAS] [--target TARGET]
                   [--fitness {RGBMSE,LABDeltaESSIM,LABMSE,LABDeltaE,SSIM}]
                   [-g NUM_GENERATIONS] [-p POPULATION_SIZE] [--width WIDTH]
                   [--height HEIGHT] [--emoji-size EMOJI_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  --starting-canvas STARTING_CANVAS
                        Path to an image to start with. If not specified, a
                        white image will be used.
  --target TARGET       Filename of target image. Should reside in
                        data/target_images/
  --fitness {RGBMSE,LABDeltaESSIM,LABMSE,LABDeltaE,SSIM}
                        Choose fitness evaluator. See fitness.py for more
                        information.
  -g NUM_GENERATIONS, --num-generations NUM_GENERATIONS
  -p POPULATION_SIZE, --population-size POPULATION_SIZE
  --width WIDTH         If specified, resize the target image (and the
                        starting canvas) to this width. Otherwise, keep the
                        original width.
  --height HEIGHT       If specified, resize the target image (and the
                        starting canvas) to this height. Otherwise, keep the
                        original height.
  --emoji-size EMOJI_SIZE
```
