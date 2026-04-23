# nnUNetDemo

This project uses nnUNet and publicly available data to train segmentation models

WORK IN PROGRESS: README.md and project as a whole is still under contruction

## Choose Data to train on

### Dataset: AMOS22
https://zenodo.org/records/7155725

Citation:
JI YUANFENG. (2022). Amos: A large-scale abdominal multi-organ benchmark for versatile medical image segmentation \[Data set]. Zenodo. https://doi.org/10.5281/zenodo.7155725

To download the data from a command line utility run the following command:

	curl https://zenodo.org/records/7155725/files/amos22.zip -o <path/to/output/file>

where <path/to/output/file> is where you want to save the file

### Dataset: FLARE2022
https://flare22.grand-challenge.org/

Citation:
Home—MICCAI FLARE 2022—Grand Challenge. (n.d.). Retrieved April 21, 2026, from https://flare22.grand-challenge.org/Home/
MA. et al. Unleashing the strengths of unlabelled data in deep learning-assisted pan-cancer abdominal organ quantification: the FLARE22 challenge. https://doi.org/10.1016/S2589-7500(24)00154-7


### Other
Alternatively choose your own data to train on

## Prepare Data

