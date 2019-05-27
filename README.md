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

* `python -m app.generator.generate`
