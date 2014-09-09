__author__ = 'Antony Cherepanov'

import unittest
import os
import shutil
import images_slicer
from PIL import Image


SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEST_SAVE_FOLDER = SCRIPT_FOLDER + str(os.sep) + "test_folder"
TEST_IMG_PATH = SCRIPT_FOLDER + str(os.sep) + "test.png"


class CheckArgumentsTest(unittest.TestCase):
    def test_valid_folder(self):
        self.assertTrue(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 1, ""))

    def test_invalid_folder(self):
        self.assertFalse(
            images_slicer.check_arguments("/invalid/folder", 1, 1, ""))

    def test_invalid_width(self):
        self.assertFalse(
            images_slicer.check_arguments(SCRIPT_FOLDER, -10, 1, ""))

    def test_invalid_height(self):
        self.assertFalse(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 0, ""))

    def test_invalid_save_folder(self):
        self.assertFalse(
            images_slicer.check_arguments(SCRIPT_FOLDER, 1, 1, "../fake/"))

    def test_save_folder_creation(self):
        self.assertTrue(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 1,
                                                      TEST_SAVE_FOLDER))

    def tearDown(self):
        if os.path.exists(TEST_SAVE_FOLDER):
            try:
                shutil.rmtree(TEST_SAVE_FOLDER, True)
            except Exception as err:
                print("Error during folder remove: {0}".format(err))
                return


class GetImagesPathsTest(unittest.TestCase):
    def test_invalid_folder(self):
        self.assertEqual(images_slicer.get_images_paths("../fake/"), list())

    def test_valid_folder(self):
        paths = [TEST_IMG_PATH]
        self.assertEqual(images_slicer.get_images_paths(SCRIPT_FOLDER), paths)


class GetExtensionTest(unittest.TestCase):
    def test_get_extension(self):
        self.assertEqual(images_slicer.get_extension(TEST_IMG_PATH), "png")

    def test_get_extension_several_dots(self):
        test_img_path = SCRIPT_FOLDER + str(os.sep) + "test.hey.jpeg"
        self.assertEqual(images_slicer.get_extension(test_img_path), "jpeg")


class ParsePathTest(unittest.TestCase):
    def test_get_parts(self):
        self.assertEqual(images_slicer.parse_image_path(TEST_IMG_PATH),
                         (SCRIPT_FOLDER, "test", "png"))

        test_img_path = SCRIPT_FOLDER + str(os.sep) + "test.hey.png"
        self.assertEqual(images_slicer.parse_image_path(test_img_path),
                         (SCRIPT_FOLDER, "test.hey", "png"))


class ListSplitTest(unittest.TestCase):
    def test_simple_list(self):
        simple = [1, 2, 3]
        result = images_slicer.list_split(simple, len(simple))
        for i in range(len(simple)):
            self.assertEqual(next(result), simple[i:i+1])

    def test_big_list(self):
        big_list = [1, 2, 3, 4, 5]
        result = images_slicer.list_split(big_list, 3)
        self.assertEqual(next(result), big_list[0:1])
        self.assertEqual(next(result), big_list[1:2])
        self.assertEqual(next(result), big_list[2:])
        self.assertRaises(StopIteration, lambda: next(result))


class ImagesSlicingTest(unittest.TestCase):
    def test_slicing(self):
        width, height = 200, 100
        slices_paths = images_slicer.slice_images([TEST_IMG_PATH],
                                                  width, height, False, "")
        self.assertEqual(len(slices_paths), 6)
        for path in slices_paths:
            img = Image.open(path)
            self.assertEqual(img.size, (width, height))

    def test_slice_with_add(self):
        width, height = 200, 100
        big_width, big_height = 245, 106
        slices_paths = images_slicer.slice_images([TEST_IMG_PATH],
                                                  width, height, True, "")
        self.assertEqual(len(slices_paths), 6)
        for path in slices_paths:
            img = Image.open(path)
            slice_wdt, slice_hgt = img.size
            self.assertIn(slice_wdt, [width, big_width])
            self.assertIn(slice_hgt, [height, big_height])

    def test_slicing_with_add_and_folder(self):
        width, height = 200, 100
        big_width, big_height = 245, 106
        os.makedirs(TEST_SAVE_FOLDER)
        slices_paths = images_slicer.slice_images([TEST_IMG_PATH],
                                                  width, height,
                                                  True, TEST_SAVE_FOLDER)
        self.assertEqual(len(slices_paths), 6)
        for path in slices_paths:
            img = Image.open(path)
            slice_wdt, slice_hgt = img.size
            self.assertIn(slice_wdt, [width, big_width])
            self.assertIn(slice_hgt, [height, big_height])

    def test_big_slice(self):
        width, height = 1000, 1000
        slices_paths = images_slicer.slice_images([TEST_IMG_PATH],
                                                  width, height,
                                                  False, "")
        self.assertEqual(len(slices_paths), 0)

        width, height = 500, 150
        slices_paths = images_slicer.slice_images([TEST_IMG_PATH],
                                                  width, height,
                                                  True, "")
        self.assertEqual(len(slices_paths), 0)

    def tearDown(self):
        images = images_slicer.get_images_paths(SCRIPT_FOLDER)
        filtered_paths = \
            [path for path in images if not path.endswith("test.png")]

        if os.path.exists(TEST_SAVE_FOLDER):
            slices = images_slicer.get_images_paths(TEST_SAVE_FOLDER)
            filtered_paths.extend(slices)

        remover = map(os.remove, filtered_paths)
        for i in range(len(filtered_paths)):
            next(remover)

        if os.path.exists(TEST_SAVE_FOLDER):
            shutil.rmtree(TEST_SAVE_FOLDER, True)


class StartSlicingTest(unittest.TestCase):
    def test_start_slicing(self):
        width, height = 200, 100
        os.makedirs(TEST_SAVE_FOLDER)
        images_slicer.start_slicing(SCRIPT_FOLDER, width, height, False,
                                    TEST_SAVE_FOLDER)

        slices_paths = images_slicer.get_images_paths(TEST_SAVE_FOLDER)
        self.assertEqual(len(slices_paths), 6)
        for path in slices_paths:
            img = Image.open(path)
            self.assertEqual(img.size, (width, height))

    def tearDown(self):
        images = images_slicer.get_images_paths(SCRIPT_FOLDER)
        filtered_paths = \
            [path for path in images if not path.endswith("test.png")]

        if os.path.exists(TEST_SAVE_FOLDER):
            slices = images_slicer.get_images_paths(TEST_SAVE_FOLDER)
            filtered_paths.extend(slices)

        remover = map(os.remove, filtered_paths)
        for i in range(len(filtered_paths)):
            next(remover)

        if os.path.exists(TEST_SAVE_FOLDER):
            shutil.rmtree(TEST_SAVE_FOLDER, True)

if __name__ == "__main__":
    unittest.main()
