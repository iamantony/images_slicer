__author__ = 'Antony Cherepanov'

import unittest
import os
import shutil
import images_slicer


SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEST_SAVE_FOLDER = SCRIPT_FOLDER + "/test_folder"


class CheckArgumentsTest(unittest.TestCase):
    def test_valid_folder(self):
        self.assertTrue(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 1, ""))

    def test_invalid_folder(self):
        self.assertFalse(images_slicer.check_arguments("/invalid/folder", 1, 1, ""))

    def test_invalid_width(self):
        self.assertFalse(images_slicer.check_arguments(SCRIPT_FOLDER, -10, 1, ""))

    def test_invalid_height(self):
        self.assertFalse(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 0, ""))

    def test_invalid_save_folder(self):
        self.assertFalse(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 1, "../fake/"))

    def test_save_folder_creation(self):
        self.assertTrue(images_slicer.check_arguments(SCRIPT_FOLDER, 1, 1, TEST_SAVE_FOLDER))

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
        test_img_path = SCRIPT_FOLDER + "/test.png"
        test_img_path = os.path.normpath(test_img_path)
        paths = [test_img_path]
        self.assertEqual(images_slicer.get_images_paths(SCRIPT_FOLDER), paths)


class GetExtensionTest(unittest.TestCase):
    def test_get_extension(self):
        test_img_path = SCRIPT_FOLDER + "/test.png"
        test_img_path = os.path.normpath(test_img_path)
        self.assertEqual(images_slicer.get_extension(test_img_path), "png")

    def test_get_extension_several_dots(self):
        test_img_path = SCRIPT_FOLDER + "/test.hey.jpeg"
        test_img_path = os.path.normpath(test_img_path)
        self.assertEqual(images_slicer.get_extension(test_img_path), "jpeg")


class ParsePathTest(unittest.TestCase):
    def test_get_parts(self):
        test_img_path = SCRIPT_FOLDER + "/test.png"
        test_img_path = os.path.normpath(test_img_path)
        self.assertEqual(images_slicer.parse_image_path(test_img_path), (SCRIPT_FOLDER, "test", "png"))

        test_img_path = SCRIPT_FOLDER + "/test.hey.png"
        test_img_path = os.path.normpath(test_img_path)
        self.assertEqual(images_slicer.parse_image_path(test_img_path), (SCRIPT_FOLDER, "test.hey", "png"))


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

if __name__ == "__main__":
    unittest.main()
