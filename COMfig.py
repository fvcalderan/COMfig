import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage
from PIL import Image
import webcolors

__author__ = 'Felipe V. Calderan'
__copyright__ = 'Copyright (C) 2024 Felipe V. Calderan'
__license__ = 'BSD 3-Clause "New" or "Revised" License'
__version__ = '1.0'

# Thanks to Fraxel and Prakash Dahal for closest_color algorithm
# https://stackoverflow.com/questions/9694165
# /convert-rgb-color-to-english-color-name-like-green-with-python
def closest_color(requested_color):
    """ Find closest name for requested color """

    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colours[(rd + gd + bd)] = name

    return min_colours[min(min_colours.keys())]


def normalize_cmap(arr):
    """ Normalize colormap for better representation """

    # Flatten the 2D array to a 1D list and get unique items
    unique = set([item for sublist in arr for item in sublist])

    # Create a dictionary to map unique items to their index
    index_mapping = {item: i for i, item in enumerate(unique)}

    # Create a new array to store indices, instead of values
    new_arr = [[index_mapping[item] for item in row] for row in arr]

    return new_arr


def gen_center_of_mass(arr, scale):
    """ Generate center of mass based on array """

    # Get center of mass
    center = ndimage.center_of_mass(arr.T)

    # Print center of mass
    print(f"Center of mass is: ({center[0]/scale:.2f}, {center[1]/scale:.2f})")

    # Generate chart
    plt.imshow(normalize_cmap(arr), cmap="bone_r")
    plt.scatter(*center, c="r", marker="x", s=100)
    plt.text(
        center[0], center[1] - center[1]/16,
        f"({center[0]/scale:.2f}, {center[1]/scale:.2f})",
        horizontalalignment='center',
        fontweight="bold",
        c="r"
    )
    plt.xticks(())
    plt.yticks(())
    plt.tight_layout()
    plt.show()


def get_scale(message):
    """ Get scale in the format x:y """

    repeat = True
    while repeat:
        print(message, end="")
        try:
            numerator, denominator = (float(x) for x in input().split(":"))
            repeat = False
        except Exception:
            print("\nInvalid scale format...")
            repeat = True

    return numerator / denominator


def process_csv(file):
    """ Process CSV file """

    # Load CSV
    try:
        arr = pd.read_csv(file, header=None).fillna(0)
    except Exception:
        print("\nInvalid CSV File")
        print("Press [Enter] to exit...")
        input()
        exit()

    # Get scale
    scale = get_scale(
            f"Your spreadsheet is of size {arr.to_numpy().shape}. "
            "Type the scale of the spreadsheet (e.g. 2:1):\n>>> "
    )

    # Process CSV
    gen_center_of_mass(arr.to_numpy(), scale)


def process_img(file):
    """ Process image file """

    # Load image
    try:
        image = Image.open(file)
    except Exception:
        print("\nInvalid PNG File")
        print("Press [Enter] to exit...")
        input()
        exit()

    # Get scale
    scale = get_scale(
        f"Your image is of size {np.array(image).shape[:-1]}. "
        "Type the scale of image (e.g. 2:1):\n>>> "
    )

    # Transform image into an array
    arr = np.array(image)

    # Get color names
    new_arr = [tuple(b)[:-1] for a in arr for b in a]

    # Attribute mass to colors
    color_to_mass = dict()
    for u in set(new_arr):

        color = closest_color(u)

        # White is always 0
        if color == "white":
            color_to_mass[u] = 0
            continue

        # Treat possible errors while reading colors
        repeat = True
        while repeat:
            try:
                mass = float(input(f"Type mass for color [{color}]:\n>>> "))
                repeat = False
            except:
                print("\nInvalid mass.")
                repeat = True

        color_to_mass[u] = mass

    # Create array of masses
    mass_arr = [color_to_mass[c] for c in new_arr]
    mass_arr = np.array(mass_arr).reshape(arr.shape[:-1])

    np.savetxt("foo.csv", mass_arr, delimiter=",")

    # Call result function
    gen_center_of_mass(mass_arr, scale)


def main():
    """ Main function """

    # Get mode
    mode = ""
    repeat = True
    while repeat:
        mode = input("Select type of file:\n1 - CSV\n2 - PNG\n>>> ")
        if mode in ["1", "2"]:
            repeat = False
        else:
            print("\nInvalid type.")

    # Get file
    file = ""
    repeat = True
    while not os.path.isfile(file):
        file = input("Type path to file:\n>>> ")
        if os.path.isfile(file):
            repeat = False
        else:
            print("\nFile does not exist or is unreadable.")

    # Catch all errors
    try:
        if mode == "1":
            process_csv(file)
        elif mode == "2":
            process_img(file)
    except Exception:
        print("\nAn error has occurred trying to run the program...")
        print("Press [Enter] to exit...")
        input()
        exit()

    print("\nDone!")
    print("Press [Enter] to exit...")
    input()


if __name__ == "__main__":
    main()
