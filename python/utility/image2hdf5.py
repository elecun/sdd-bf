
import h5py
import argparse
import sys
import os
import glob
from PIL import Image
import numpy as np

group_name = "dataset"

if __name__ == "__main__":
    #arguments
    parser = argparse.ArgumentParser(description="image2hdf5 --out output_hdf5 --in image_path")
    parser.add_argument('--outfile', nargs='?', required=True, help="Output HDF5 file")
    parser.add_argument('--inpath', nargs='?', required=True, help="Input images (path)")
    args = parser.parse_args()

    _out_hdf5 = args.outfile
    _in_path = args.inpath + "*.png"

    try :
        if _out_hdf5 is None or _in_path is None:
            print("It must be required the output file name.")

        with h5py.File(_out_hdf5, 'a') as hf:
            group = hf.create_group(group_name)

            image_list = glob.glob(_in_path)
            for file in image_list:
                if os.path.isfile(file):
                    print("read image : ", file)
                    # read image as binary
                    with open(file, 'rb') as img:
                        bin_image = img.read() # read as binary
                        bin_image_np = np.asarray(bin_image)
                        dset = group.create_dataset(file, data=bin_image_np)
                        print(dset.name, dset.shape, dset.dtype)

        hf.close()

        
    except ValueError as e:
        print("Error :", e)

    