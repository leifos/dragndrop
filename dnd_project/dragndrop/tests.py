"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Folder
from find.search.response import Result
from django.contrib.auth.models import User
from folders import create_folder, get_user_folders, remove_folder, get_folder

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def setUp(self):
        self.ie = User(username='james')
        self.ie.save()


    def test_creation_of_folders(self):
        f1 = create_folder(self.ie,'test')
        f2 = create_folder(self.ie,'temp')
        folder_list = get_user_folders(self.ie)

        self.assertEquals(len(folder_list),2)

    def test_get_folder(self):
        f1 = create_folder(self.ie,'test')
        f2 = create_folder(self.ie,'temp')

        f3 = get_folder(f2.id)
        self.assertEquals(f2,f3)

    def test_removal_of_folders(self):
        f1 = create_folder(self.ie,'test')
        f2 = create_folder(self.ie,'temp')
        folder_list = get_user_folders(self.ie)
        self.assertEquals(len(folder_list),2)

        remove_folder(f1.id)
        folder_list = get_user_folders(self.ie)
        self.assertEquals(len(folder_list),1)

    def test_addition_of_results_to_folder(self):
        f1 = create_folder(self.ie,'test')



