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

if __name__ == "__main__":
    unittest.main()
