
import h5py
import argparse
import sys
import os
import io
import glob
from PIL import Image
import numpy as np

group_name = "cam1_images"

data = []
group = []
def extract(name, obj):
    if isinstance(obj, h5py.Dataset):
        data.append(name)
    elif isinstance(obj, h5py.Group):
        group.append(name)

if __name__ == "__main__":
    #arguments
    parser = argparse.ArgumentParser(description="hdf52image --outpath out_path --infile hdf5_file")
    parser.add_argument('--outpath', nargs='?', required=True, help="output path")
    parser.add_argument('--infile', nargs='?', required=True, help="Input HDF5 file")
    args = parser.parse_args()

    _out_path = args.outpath
    _in_hdf5 = args.infile

    with h5py.File(_in_hdf5, "r") as hf:
        hf.visititems(extract)

        for image_data in data:
            arr = np.array(hf[image_data])
            img = Image.open(io.BytesIO(arr))
            print("image size : ", img.size)

        # group_key = list(hf.keys())[0]
        # print("Root group : ", group_key)

        # sub_group_key = list(hf[group_key])[0]
        # print("Sub Group : ", sub_group_key)

        # datalist = hf[group_key][sub_group_key].keys() # n members

        # for datakey in datalist:
        #     print("data key : ", datakey)
        #     data = hf[group_key][sub_group_key][datakey]
        #     print(data[0:,])

        hf.close()


    