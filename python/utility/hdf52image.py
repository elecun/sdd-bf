
import h5py
import argparse
import sys
import os
import io
import glob
from PIL import Image
import numpy as np
from pathlib import Path

group_name = "cam1_images"

data_path = []
group_path = []
def extract(name, obj):
    if isinstance(obj, h5py.Dataset):
        data_path.append(name)
    elif isinstance(obj, h5py.Group):
        group_path.append(name)

if __name__ == "__main__":
    #arguments
    parser = argparse.ArgumentParser(description="hdf52image --outpath out_path --infile hdf5_file")
    parser.add_argument('--outpath', nargs='?', required=True, help="output path")
    parser.add_argument('--infile', nargs='?', required=True, help="Input HDF5 file")
    args = parser.parse_args()

    _out_path = args.outpath
    _in_hdf5 = args.infile

    _base_dir = os.path.dirname(os.path.abspath(__file__)) 

    with h5py.File(_in_hdf5, "r") as hf:
        hf.visititems(extract)

        for path in data_path:
            abs_path = Path(_base_dir)/Path(path)
            dir= os.path.dirname(path)
            
            os.mkdir(dir)
            img_data = Image.open(io.BytesIO(np.array(hf[path])))
            print("image size : ", img_data.size)
            #image_file = Image.open(path)
            img_data.save("./"+path, "png")

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


    