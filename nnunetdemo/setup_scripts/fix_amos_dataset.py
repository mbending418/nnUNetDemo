import nibabel as nib
import numpy as np
import click
import json
import os

from nnunetdemo.prepare_data.prepareNIFTI import NIFTI_FILE_ENDING


@click.command()
@click.argument("data_folder", type=click.Path(exists=True))
@click.argument("dataset", type=str)
def fix_amos(data_folder, dataset):
    dataset_folder = os.path.join(data_folder, "nnUNet_raw", dataset)
    labels_folder = os.path.join(dataset_folder, "labelsTr")
    with open(os.path.join(dataset_folder, "dataset.json"), "r") as fj:
        dataset_dict = json.load(fj)
    labels =  dataset_dict["labels"]
    code = None
    label = None
    for key, value in labels.items():
        if key != "background":
            label = key
            code = value
    if code is None or label is None:
        raise Exception("no non background labels")
    dataset_dict["labels"][label] = 1

    for label in os.listdir(labels_folder):
        if not label.endswith(NIFTI_FILE_ENDING):
            continue
        label_file = os.path.join(labels_folder, label)
        label_obj = nib.load(label_file)
        label_data = label_obj.get_fdata()

        new_data = nib.Nifti1Image(label_data==code, affine=label_obj.affine, header=label_obj.header)
        nib.save(new_data, label_file)

    with open(os.path.join(dataset_folder, "dataset.json"), "w") as fj:
        json.dump(dataset_dict, fj, indent=4)

