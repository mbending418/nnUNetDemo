import os
import click
import shutil
from typing import Literal
from nnunetv2.experiment_planning.plan_and_preprocess_api import extract_fingerprints, plan_experiments, preprocess
from nnunetdemo.prepare_data.prepareNIFTI import prepare_nifti, NIFTI_FILE_ENDING

ALL_LABELS = {
    "spleen" : 1,
    "right_kidney" : 2,
    "left_kidney" : 3,
    "gallbladder" : 4,
    "esophagus" : 5,
    "liver" : 6,
    "stomach" : 7,
    "aorta" : 8,
    "postcava" : 9,
    "pancreas" : 10,
    "right_adrenal_gland" : 11,
    "left_adrenal_gland" : 12,
    "duodenum" : 13,
    "bladder" : 14,
    "prostate/uterus" : 15
}

MODALITY_FOLDERS = {
    "CT" : "ct_data",
    "T2" : "mr_data"
}

#if the number in the file name is less than 500 it's a CT
def is_ct(amos_file: str) -> bool:
    code = int(amos_file[5:9])
    return code < 500

subfolders= ("Tr", "Va", "Ts")
def sort_amos22(input_folder: str,
                subfolders_to_sort: tuple[str, ...] = subfolders):
    """
    AMOS22 data is combined CT and MR.
    Any case # less than 500 is CT the rest are MR
    This function sorts the data into two new folders: "ct_data" and "mr_data"

    AMOS22 data folder has a Training, Validation, and Test Split organized by subfolders
    use subfolders_to_sort to specify which of these you want to include

    :param input_folder: input folder where all the data lives
        should have subfolders "imagesTr", "labelsTr", "imagesVa", "labelsVa", etc
    :param subfolders_to_sort: which of the subfolders you want to include
        "Tr" refers to the training set
        "Va" refers to the validation set
        "Ts" refers to the test set
    :return:
    """
    if os.path.isdir(os.path.join(input_folder, MODALITY_FOLDERS["CT"])):
        raise Exception(f"CT Data directory already present: {os.path.join(input_folder, MODALITY_FOLDERS["CT"])}")
    if os.path.isdir(os.path.join(input_folder, MODALITY_FOLDERS["T2"])):
        raise Exception(f"MR Data directory already present: {os.path.join(input_folder, MODALITY_FOLDERS["T2"])}")
    os.makedirs(os.path.join(input_folder, MODALITY_FOLDERS["CT"]))
    os.makedirs(os.path.join(input_folder, MODALITY_FOLDERS["CT"], "imagesTr"))
    os.makedirs(os.path.join(input_folder, MODALITY_FOLDERS["CT"], "labelsTr"))
    os.makedirs(os.path.join(input_folder, MODALITY_FOLDERS["T2"]))
    os.makedirs(os.path.join(input_folder, MODALITY_FOLDERS["T2"], "imagesTr"))
    os.makedirs(os.path.join(input_folder, MODALITY_FOLDERS["T2"], "labelsTr"))

    for subfolder in subfolders_to_sort:
        image_input_folder = os.path.join(input_folder, f"images{subfolder}")
        label_input_folder = os.path.join(input_folder, f"labels{subfolder}")
        for case in os.listdir(image_input_folder):
            if not case.endswith(NIFTI_FILE_ENDING):
                continue
            if case not in os.listdir(label_input_folder):
                print(f"WARNING: cannot find label file for {case}. Skipping.")
                continue
            if is_ct(case):
                output_image_folder = os.path.join(input_folder, MODALITY_FOLDERS["CT"], "imagesTr")
                output_label_folder = os.path.join(input_folder, MODALITY_FOLDERS["CT"], "labelsTr")
            else:
                output_image_folder = os.path.join(input_folder, MODALITY_FOLDERS["T2"], "imagesTr")
                output_label_folder = os.path.join(input_folder, MODALITY_FOLDERS["T2"], "labelsTr")

            shutil.copyfile(os.path.join(image_input_folder, case), os.path.join(output_image_folder, case))
            shutil.copyfile(os.path.join(label_input_folder, case), os.path.join(output_label_folder, case))

def prepare_amos22(input_folder: str,
                   dataset_name: str,
                   dataset_id: int,
                   modality: Literal["CT", "T2"],
                   label_names: tuple[str,...],
                   output_folder="output"):
    for label in label_names:
        if label not in ALL_LABELS:
            raise Exception(f"Label '{label}' is not available for AMOS 2022 Dataset.")

    if modality not in ["CT", "T2"]:
        raise Exception(f"Unknown modality '{modality}' for AMOS 2022 Dataset.")
    image_folder = os.path.join(input_folder, MODALITY_FOLDERS[modality], "imagesTr")
    label_folder = os.path.join(input_folder, MODALITY_FOLDERS[modality], "labelsTr")

    prepare_nifti(image_label_folder_pairs=[(image_folder, label_folder)],
                  dataset_name=dataset_name,
                  label_map={label: ALL_LABELS[label] for label in label_names},
                  modality=modality,
                  output_folder=output_folder,
                  dataset_id=dataset_id)

@click.command()
@click.argument("input_folder", type=click.Path(exists=True))
@click.argument("subfolders_to_sort", type=str, nargs=-1)
def run_sort_amos22(input_folder: str, subfolders_to_sort: tuple[str, ...]):
    sort_amos22(input_folder=input_folder,subfolders_to_sort=subfolders_to_sort)

@click.command()
@click.argument('input_folder', type=click.Path(exists=True))
@click.argument('dataset_name', type=str)
@click.argument("dataset_id", type=int)
@click.argument("output_folder", type=str, default="output")
@click.argument('modality', type=str)
@click.argument('label_names', type=str, nargs=-1)
def run_setup_amos22(input_folder: str,
                     dataset_name: str,
                     dataset_id: int,
                     output_folder: str,
                     modality: Literal["CT", "T2"],
                     label_names: tuple[str, ...]):

    prepare_amos22(input_folder=input_folder,
                   dataset_name=dataset_name,
                   dataset_id=dataset_id,
                   modality=modality,
                   label_names=label_names,
                   output_folder=output_folder)

    #add paths to environment variables
    os.environ["nnUNet_raw"] = os.path.join(output_folder, MODALITY_FOLDERS[modality], "nnUNet_raw")
    os.environ["nnUNet_preprocessed"] = os.path.join(output_folder, MODALITY_FOLDERS[modality], "nnUNet_preprocessed")
    os.environ["nnUNet_results"] = os.path.join(output_folder, MODALITY_FOLDERS[modality], "nnUNet_results")

    extract_fingerprints(dataset_ids = [0],
                         check_dataset_integrity=True)
    plans_identifier = plan_experiments(dataset_ids = [0])
    preprocess(dataset_ids = [0],plans_identifier=plans_identifier)