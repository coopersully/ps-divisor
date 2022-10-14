import os
import sys

from psd_tools import PSDImage

output_dir = "scanned"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

total_found = 0
for (path, dirs, files) in os.walk("raw"):

    if files.__len__() == 0:
        print('No files were found in the input directory.')
        sys.exit()

    for file in files:

        # If the file isn't a Photoshop file, ignore it
        if not file.__contains__('.psd'):
            continue

        # Add file to the list
        file_abs: str = os.path.join(path, file)

        # Grab file name
        file_name = file[:-4]

        # Save whole image in super-directory as png
        psd: PSDImage = PSDImage.open(file_abs)
        psd.composite().save(f'{output_dir}/{ file_name }.png')

        # Create the subdirectory for image breakdown
        output_subdir = f'{ output_dir }/{ file_name }'
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)

        # Save each layer inside the subdirectory
        for layer in psd:
            print(layer)
            layer_image = layer.composite()
            layer_image.save(f'{ output_subdir }/{ layer.name }.png')

        # Increment total PSD files found
        total_found += 1

print()
print(f'Success! Divided { total_found } photoshop documents.')