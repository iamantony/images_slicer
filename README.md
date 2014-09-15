[![Build Status](https://travis-ci.org/iamantony/images_slicer.svg?branch=master)](https://travis-ci.org/iamantony/images_slicer)   [![Coverage Status](https://coveralls.io/repos/iamantony/images_slicer/badge.png)](https://coveralls.io/r/iamantony/images_slicer)

images_slicer
=============

Multi-thread Python app for slicing images.

Start point - [0, 0] - upper left corner of the image.

Tags
=======================
python, image, processing, slice, slicing, multithread

Usage
=======================

    $ images_slicer PATH_TO_FOLDER WIDTH HEIGHT -ADD -RESULTS_FOLDER

* PATH_TO_FOLDER - absolute path to the folder with images that you want to slice
* WIDTH - width of the slice
* HEIGHT - height of the slice
* -ADD - add extra space at the last slice (optional)
* -RESULTS_FOLDER - absolute path where slices should be saved (optional)

Examples
=======================

Create slices with size 100x90 for all images in images_folder:

    $ python images_slicer.py /home/my_user_name/images_folder 100 90
    
Create slices with size 300x20 for all images in images_folder. If the size of
the last slice is less than required, than it will be appended to previous slice.
So for image of size 400x50 will be created 2 slices - 400x20 and 400x30:

    $ python images_slicer.py /home/my_user_name/images_folder 300 20 -add
    
Create slices with size 100x90 for all images in images and save them to /some/other-folder:

    $ python images_slicer.py C:\\images 100 90 -s /some/other-folder
    
Show help:

    $ python images_slicer.py -h
    
Requirements
=======================

Python >= 2.6

Pillow (PIL) library

    $pip install Pillow
