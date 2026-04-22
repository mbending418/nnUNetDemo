import nibabel as nib
import numpy as np
import shutil
import json
import os

NIFTI_FILE_ENDING = ".nii.gz"

def validate_nifti_label(label_file: str, label_codes: list[int]) -> bool:
    """
    check to make sure the label file has all the appropriate labels

    :param label_file: the file to check
    :param label_codes: the labels to check
    :return:
    """

    lab = nib.load(label_file)
    for label_code in label_codes:
        if np.sum(lab.get_fdata()==label_code) == 0:
            return False
    return True

def prepare_nifti(image_label_folder_pairs: list[tuple[str,str]],
                  output_folder: str,
                  dataset_name: str,
                  label_map: dict[str, int],
                  modality: str):
    """
    given a bunch of folders with image and label data
    produce a dataset compliant with nnUNet complete with dataset.json file

    The output folder will include:
        nnUNet_raw
        nnUNet_preprocessed
        dataset.json

    :param image_label_folder_pairs: list of tuples where the first entry of each tuple is the image and the second entry is the label
    :param output_folder: where to save the data
    :param dataset_name: the name of the dataset "eg. Liver"
    :param label_map: map from structure name to labelID
        for instance if the data is labeled where "liver" is 1 and "stomach" is 11
        then this label_map is {"liver" : 1, "stomach" : 11}
    :param modality: the 'modality' or 'channel name' eg "CT", "MR", "T2", "ADC", etc
    :return:
    """

    case_map : dict[str, tuple[str, str]] = {}
    for image_label_folder_pair in image_label_folder_pairs:
        for image_folder, label_folder in image_label_folder_pair:
            for case in os.listdir(image_folder):
                if not case.endswith(NIFTI_FILE_ENDING):
                    continue
                case, _ = case.split(NIFTI_FILE_ENDING)

                case_image = os.path.join(image_folder, case)
                case_label = os.path.join(label_folder, case)

                if not os.path.isfile(case_label):
                    print(f"WARNING: cannot file label file for {case}. Skipping.")
                    continue

                if not validate_nifti_label(case_label, list(label_map.values())):
                    print(f"WARNING: label file has missing labels for {case}. Skipping.")
                    continue

                if case in case_map:
                    print(f"WARNING: duplicate case: {case}. Skipping.")
                    continue

                case_map[case] = (case_image, case_label)

    for case, (src_image, src_label) in case_map.items():
        dest_folder = os.path.join(output_folder, "nnUNet_raw", f"Dataset001_{dataset_name}")
        dest_image = os.path.join(dest_folder, "imagesTr", f"{case}_0000{NIFTI_FILE_ENDING}")
        dest_label = os.path.join(dest_folder, "labelsTr", f"{case}{NIFTI_FILE_ENDING}")

        shutil.copyfile(src_image, dest_image)

        label = nib.load(src_label)
        label_data = label.getfdata()
        mask = label_data==label_data
        for label_code in label_map.values():
            mask *= label_data!=label_code
        label_data[mask]=0
        new_label = nib.Nifti1Image(label_data, affine=label.affine, header=label.header)
        nib.save(new_label, dest_label)

        label_map["background"] = 0

        output_json = {
            "channel_names": {"0": modality},
            "labels" : label_map,
            "numTraining" : len(case_map),
            "file_ending" : NIFTI_FILE_ENDING,
        }

        with open(os.path.join(dest_folder, "dataset.json"), 'w') as jf:
            json.dump(output_json, jf, indent=4)


