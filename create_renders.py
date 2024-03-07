# import pdb
import bpy 
import sys
import os
import csv
import imageio.v2 as imageio
import h5py
import uuid


def read_exr(file_path):
    """Read an EXR file and return its data as a NumPy array."""
    exr_data = imageio.imread(file_path)
    return exr_data  # This is already a NumPy array with the image data


def save_to_hdf5(data, hdf5_path, dataset_name):
    """Save the data to an HDF5 file with a unique dataset name."""
    unique_name = dataset_name[:-4] # Append a timestamp to make the name unique
    # print("unique: ", unique_name)
    with h5py.File(hdf5_path, 'a') as hdf5_file:
        hdf5_file.create_dataset(unique_name, data=data, compression="gzip")

sys.path.append(os.path.basename(bpy.data.filepath))

csv_filepath = "./output/codification.csv"

mount_point = "/home/abha/abha/umn/mono_depth/resources_data/selected_obj_files/"

with open("./data/object_loc_output_loc.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip header 
    next(csv_reader)
    for index, row in enumerate(csv_reader):
        #object_filepath,output_blend_paths
        object_filepath = mount_point  + str(row[1])
        output_folder = "./output/"  #+ str(row[0])
        temp_folder = "./temp/"
        # scene.direct_renders(object_filepath,output_folder)
        arguments = str(object_filepath)+" "+str(output_folder) +" "+str(temp_folder) +" "+str(csv_filepath)
        # print(f'blender -P tutorial.py -- '+ arguments)

        # breakpoint()
        os.system(f'blender -b -P tutorial.py -- '+ arguments)
        filename_hdf5 = str(uuid.uuid4())+'.hdf5'
        hdf5_path = output_folder + filename_hdf5  # Ensure this is a full path including the file name
        print(hdf5_path)

        for filename in os.listdir(temp_folder):
            # print("0",os.listdir(directory_path))
            if filename.endswith(".exr"):
                file_path = os.path.join(temp_folder, filename)
                data = read_exr(file_path)
                dataset_name = os.path.splitext(filename)[0]  # Use the filename without the extension as the dataset name
                save_to_hdf5(data, hdf5_path, dataset_name)

        with open(csv_filepath, mode='r', newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)

        # Assuming there is at least one line to edit
        if lines:
            # Step 2: Modify the last line
            # Example modification: changing the second column of the last row
            lines[-1][0] = filename_hdf5

        # Step 3: Rewrite the CSV file with the modified lines
        with open(csv_filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

print("-----------------------------------------------------------------------")

