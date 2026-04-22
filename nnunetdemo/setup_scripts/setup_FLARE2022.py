import os
import click
from nnunetv2.experiment_planning.plan_and_preprocess_api import extract_fingerprints, plan_experiments, preprocess
from nnunetdemo.prepare_data.prepareNIFTI import prepare_nifti


ALL_LABELS = {
    "liver" : 1,
    "right_kidney" : 2,
    "spleen" : 3,
    "pancreas": 4,
    "aorta": 5,
    "inferior_vena_cava" : 6,
    "right_adrenal_gland" : 7,
    "gallbladder" : 8,
    "esophagus" : 9,
    "stomach" : 10,
    "duodenum" : 11,
    "left_kidney" : 12
}
MODALITY="CT"

def prepare_flare2022(input_folder: str,
                      dataset_name: str,
                      label_names: tuple[str,...],
                      output_folder="output",
                      image_folder="images",
                      label_folder="labels"):
    image_folder = os.path.join(input_folder, image_folder)
    label_folder = os.path.join(input_folder, label_folder)

    for label in label_names:
        if label not in ALL_LABELS:
            raise Exception(f"Label '{label}' is not available for FLARE 2022 Dataset.")

    prepare_nifti(image_label_folder_pairs=[(image_folder, label_folder)],
                  output_folder=output_folder,
                  dataset_name=dataset_name,
                  label_map= {label: ALL_LABELS[label] for label in label_names},
                  modality=MODALITY)

@click.command()
@click.argument('input_folder', type=click.Path(exists=True))
@click.argument('dataset_name', type=str)
@click.argument("output_folder", type=str, default="output")
@click.argument("image_folder", type=str, default="images")
@click.argument("label_folder", type=str, default="labels")
@click.argument('label_names', type=str, nargs=-1)
def run_setup_flare2022(input_folder: str,
                        dataset_name: str,
                        output_folder: str,
                        image_folder: str,
                        label_folder: str,
                        label_names: tuple[str, ...]):
    prepare_flare2022(input_folder=input_folder,
                      dataset_name=dataset_name,
                      label_names=label_names,
                      output_folder=output_folder,
                      image_folder=image_folder,
                      label_folder=label_folder)

    extract_fingerprints(dataset_ids = [0],
                         check_dataset_integrity=True)
    plans_identifier = plan_experiments(dataset_ids = [0])
    preprocess(dataset_ids = [0],plans_identifier=plans_identifier)