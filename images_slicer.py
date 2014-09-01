__author__ = 'Antony Cherepanov'

import argparse
import os
import multiprocessing
from PIL import Image


def parse_arguments():
    """ Parse arguments and start slice process
    :return list of arguments
    """

    parser = argparse.ArgumentParser(description="Multi-thread python app for slicing images")
    parser.add_argument("folder", help="absolute path to the folder with images to slice")
    parser.add_argument("-width", help="width of slice", type=int)
    parser.add_argument("-height", help="height of slice", type=int)
    parser.add_argument("-add", action="store_true",
                        help="if size of the last slice is less than desired, add it to the previous slice")
    parser.add_argument("-s", "--save_to", help="path to the folder where slices should be saved")

    args = parser.parse_args()
    return args.folder, args.width, args.height, args.add, args.save_to


def check_arguments(t_folder, t_width, t_height, t_save_folder):
    """ Check arguments
    :param t_folder: string with absolute path to the folder with images to slice
    :param t_width: int width of the slice
    :param t_height: int height of the slice
    :param t_save_folder: string absolute path to folder for slices
    :return boolean value. True if arguments are OK.
    """

    if check_existing_folder(t_folder) is False:
        print("Error: Invalid path to folder with images - " + t_folder)
        return False

    if t_width <= 0 or t_height <= 0:
        print("Error: Invalid slice size")
        return False

    if check_folder_path(t_save_folder) is False:
        print("Error: Invalid path to folder for slices - " + t_save_folder)
        return False

    return True


def check_existing_folder(t_path):
    """ Check if folder really exist
    :param t_path: string with absolute path to presumably existing folder
    :return: boolean value. True if folder exist, False if it's not
    """

    if not os.path.isabs(t_path) or\
            not os.path.exists(t_path) or\
            not os.path.isdir(t_path):
        return False
    return True


def check_folder_path(t_path):
    """ Check if path to folder is valid
    :param t_path: string with absolute path to some folder
    :return: boolean value. True if path could be path for folder.
    """

    if os.path.isabs(t_path) is True:
        return True
    return False


def start_slicing(t_folder, t_width, t_height, t_add_small_slice, t_save_folder):
    """ Slice images
    :param t_folder: string with absolute path to the folder with images to slice
    :param t_width: int width of the slice
    :param t_height: int height of the slice
    :param t_add_small_slice: boolean value If True and last slice is too small, add it to the previous
    :param t_save_folder: string absolute path to folder for slices
    """

    images = get_images_paths(t_folder)
    cores_num = multiprocessing.cpu_count()
    img_chunks = list_split(images, cores_num)

    jobs = list()
    for i in range(cores_num):
        thread = multiprocessing.Process(target=slice_images,
                                         args=(next(img_chunks), t_width, t_height, t_add_small_slice, t_save_folder))
        jobs.append(thread)
        thread.start()

    for thread in jobs:
        thread.join()


def get_images_paths(t_folder):
    """ Check if folder contains images (on the first level) and return their paths
    :param t_folder: string with the absolute path to the folder
    :return: list with the absolute paths of the images in folder
    """

    if not os.path.isdir(t_folder):
        return list()

    image_extensions = ("jpg", "jpeg", "bmp", "png", "gif", "tiff")
    images = list()
    entries = os.listdir(t_folder)
    for entry in entries:
        file_path = os.path.join(t_folder, entry)
        extension = get_extension(file_path)
        if os.path.isfile(file_path) and extension in image_extensions:
            images.append(file_path)

    return images


def get_extension(t_path):
    """ Get extension of the file
    :param t_path: path or name of the file
    :return: string with extension of the file or empty string if we failed to get it
    """

    path_parts = str.split(t_path, '.')
    extension = path_parts[-1:][0]
    extension = extension.lower()
    return extension


def list_split(t_list, t_size):
    """ Generator that split list of elements in n chunks
    :param t_list - list of elements
    :param t_size - size of chunk
    :return generator of lists of chunks
    """

    new_length = int(len(t_list) / t_size)
    for i in range(0, t_size - 1):
        yield t_list[i * new_length:i * new_length + new_length]
    yield t_list[t_size * new_length - new_length:]


def slice_images(t_images, t_width, t_height, t_add_small_slice, t_save_folder):
    """
    :param t_images: list of path to the images
    :param t_width: int width of the slice
    :param t_height: int height of the slice
    :param t_add_small_slice: boolean value If True and last slice is too small, add it to the previous
    :param t_save_folder: string absolute path to folder for slices
    """

    for img_path in t_images:
        path, name, extension = parse_image_path(img_path)


def parse_image_path(t_img_path):
    """ Parse path to image and return it's parts: path, image name, extension
    :param t_img_path: string with path to image
    :return: tuple of strings that hold path to image file, image name and image extension
    """

    *path_parts, image_name = str.split(t_img_path, '/')
    path = "/".join(path_parts)
    *image_name_parts, extension = str.split(image_name, '.')
    name = ".".join(image_name_parts)
    return path, name, extension


if __name__ == '__main__':
    arguments = parse_arguments()
    isOk = check_arguments(arguments[0], arguments[1], arguments[2], arguments[4])
    if isOk is True:
        start_slicing(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4])
    else:
        print("Invalid arguments. Try again!")