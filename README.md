# COMfig
Calculate [**C**]enter [**O**]f [**M**]ass of a [**fig**]ure represented by CSV sheet or PNG image

```
  __                _     _                      
 / _|_   _____ __ _| | __| | ___ _ __ __ _ _ __  
| |_\ \ / / __/ _` | |/ _` |/ _ \ '__/ _` | '_ \ 
|  _|\ V / (_| (_| | | (_| |  __/ | | (_| | | | |
|_|   \_/ \___\__,_|_|\__,_|\___|_|  \__,_|_| |_|

BSD 3-Clause License
Copyright (c) 2024, Felipe V. Calderan
All rights reserved.
See the full license inside LICENSE file
```

## Install dependencies

Install required libraries using provided `requirements.txt` file:
```sh
pip3 install -r requirements.txt
```

## Modes

There are two modes: CSV and PNG.

### CSV
A valid CSV contains numerical values representing the weight of each pixel, with blank spaces or 0s indicating vacuum.

Refer to [Example 1](examples/ex01.csv) for reference.

### PNG
A valid PNG image is saved with distinct colors representing varying weights, with white indicating vacuum.

Refer to [Example 2](examples/ex02.png) for reference.

## Execution

The program is interactive and receives no arguments:
```sh
python3 COMfig.py
```

You'll then be asked for the mode of execution:
```
Select type of file:
1 - CSV
2 - PNG
>>>
```
Type `1` for CSV or `2` for PNG. Then, you must inform the path to the file.

After that, COMfig prompts you to specify the scale of the spreadsheet or image. For instance, if you input `2:1`, you are indicating to the program that the spreadsheet or image is twice the actual size. This is helpful for increasing the number of pixels to depict more detailed objects, but it's later downscaled for calculation purposes.

When using PNG mode, you'll also need to specify the mass that each color represents.

Once completed, the program will showcase the center of mass and provide an image indicating its position.

