# nnUNetDemo

This project uses nnUNet and publicly available data to train segmentation models

You can read more about nnUNet at their official GitHub here: https://github.com/MIC-DKFZ/nnUNet/

citation:

	Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2021). nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nature Methods, 18(2), 203-211.

## Choose Data to train on

### Dataset: AMOS22
https://zenodo.org/records/7155725

Citation:

	JI YUANFENG. (2022). Amos: A large-scale abdominal multi-organ benchmark for versatile medical image segmentation \[Data set]. Zenodo. https://doi.org/10.5281/zenodo.7155725

To download the data from a command line utility run the following command:

	curl https://zenodo.org/records/7155725/files/amos22.zip -o amos22.zip

This will download a zip file called "amos22.zip"

### Dataset: FLARE2022
https://flare22.grand-challenge.org/

Citation:

	Home—MICCAI FLARE 2022—Grand Challenge. (n.d.). Retrieved April 21, 2026, from https://flare22.grand-challenge.org/Home/ MA. et al. Unleashing the strengths of unlabelled data in deep learning-assisted pan-cancer abdominal organ quantification: the FLARE22 challenge. https://doi.org/10.1016/S2589-7500(24)00154-7


### Other
Alternatively choose your own data to train on

## Install Package
You can install this package by checking out this repository locally and installing it using the following commands:
	
	git clone https://github.com/mbending418/nnUNetDemo.git
	cd nnUNetDemo
	pip install -e .

## Setup and Prepare Data

You can read more about the requirements for setup here (for instance if you ant to setup your own dataset): 

	https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how-to/prepare-a-dataset.md

### Dataset: AMOS2022
If you are using the AMOS22 dataset run the following commands:
	
	unzip amos22.zip -d amos22
	sort_AMOS22 amos22/amos22
	setup_AMOS22 amos22/amos22 DatasetName DataSetID OutputFolder Modality LabelName_1 LabelName_2 ...

DatasetName is what you want to call your dataset

DatasetID is a unique dataset identifier from 000 to 999

OutputFolder is where you want to save the prepared data

Modality is either "CT" or "T2" depending on if you want the CT or MR data

LabelName_i is the ith label you wish to train your model on. eg liver, spleen, aorta, etc. Leave this off to train on all labels

If sort_AMOS22 or setup_AMOS22 don't work, make sure that the python `bin` directory is in your path. If it's still giving you trouble you should be able to open up a python console and manually import the functions to run like so:

	python
	from nnunetdemo.setup_scripts.setup_AMOS22 import sort_amos22 prepare_amos22
	sort_amos22("amos22/amos22")
	setup_amos22("amos22/amos22", "myDataset", "000","output", "CT")

or similar depending on your exact setup 

## Set the Path Variables

See section 5 on the nnUNet installation and setup: 

	https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/getting-started/installation-and-setup.md

Don't skip this step. This is how nnUNet knows where you data is.

### Dataset: AMOS22
If you are using AMOS22, you'll want to set the following values:

	nnUNet_raw="amos22/amos22/nnUNet_raw"
	nnUNet_preprocessing="amos22/amos22/nnUNet_preprocessing"
	nnUNet_results="amos22/amos22/nnUNet_results"
	
## Preprocess Data

You can read more about the preprocessing here (for instance if you want to setup your own dataset):
 
	https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how-to/plan-and-preprocess.md

### Dataset: AMOS22
If you are using the AMOS22 dataset run the following command:
	
	nnUNetv2_plan_and_preprocess -d DatasetID --verify_dataset_integrity

If you are having trouble, make sure that the python `bin` directory is in your path.

## Train

You can read more about the training process here (for instance if you want to use your own dataset):
	
	https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how-to/train-models.md

### Dataset: AMOS22
If you are using the AMOS22 dataset run the following command:

	nnUNetv2_train DatasetID CONFIGURATION FOLD

where

CONFIGURATION is one of "2d", "3d_fullres", "3d_lowres", "3d_cascade_fullres". Depending on the side of the dataset, "3d_lowres" and/or "3d_cascade_fullres" may not be available.

FOLD is a number 0 through 4 which represents which of the "folds" in a 5 fold cross validation you which to train on.