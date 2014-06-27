"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Folder
from find.search.response import Result
from django.contrib.auth.models import User
from models import Bookmark
import re
from folders import create_folder, get_user_folders, remove_folder, get_folder, add_result_to_folder, get_folder_results, get_user_folders, suggest_folders

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

    def test_get_results_of_folder(self):
        f1 = create_folder(self.ie,'test')

        r1 = Result(title='r1',url='www.love.com',summary="Gambo Gambo")
        r2 = Result(title='r2',url='www.isinthe.com',summary="Gambo Gambo")
        r3 = Result(title='r3',url='www.air.com',summary="Gambo Gambo")

        b1 = add_result_to_folder(f1.id, r1)
        b2 = add_result_to_folder(f1.id, r2)
        b3 = add_result_to_folder(f1.id, r3)

        b4 = get_folder_results(f1.id)

        self.assertItemsEqual([b1, b2, b3], b4)

    def test_addition_of_results_to_folder(self):
        f1 = create_folder(self.ie,'test')

        r1 = Result(title='r1',url='www.love.com',summary="Gambo Gambo")

        b1 = Bookmark(folder=f1,title=r1.title, url=r1.url, summary=r1.summary)
        b1.save()

        b2 = add_result_to_folder(f1.id, r1)
        self.assertEquals(b1,b2)

    def test_get_user_folders(self):
        f1 = create_folder(self.ie,'test')
        f2 = create_folder(self.ie,'temp')

        f3 = get_user_folders(self.ie)

        self.assertItemsEqual([f1,f2],f3)

    def test_suggestion_of_folders(self):
        f1 = create_folder(self.ie,'test this')
        f2 = create_folder(self.ie,'test that')
        f3 = create_folder(self.ie,'test everything')

        r1 = Result(title='r1',url='www.love.com',summary="Gambo Love")
        r2 = Result(title='r2',url='www.isinthe.com',summary="Gambo Food")
        r3 = Result(title='r3',url='www.air.com',summary="Gambo Money")
        r4 = Result(title='r4',url='www.james.com',summary="Gambo Food")
        r5 = Result(title='r5',url='www.ryanair.com',summary="Gambo Money")

        b1 = add_result_to_folder(f1.id, r1)
        b2 = add_result_to_folder(f1.id, r2)
        b3 = add_result_to_folder(f1.id, r3)
        b4 = add_result_to_folder(f2.id, r4)
        b5 = add_result_to_folder(f3.id, r5)

        f5 = suggest_folders(self.ie,'money')

        self.assertItemsEqual([f1,f3], f5)


class ReallySimpleTest(TestCase):

    def setUp(self):
        self.ie = User(username='james')
        self.ie.save()
        self.f1 = create_folder(self.ie,'test this')
        self.f2 = create_folder(self.ie,'test that')
        self.f3 = create_folder(self.ie,'test everything')

        self.r1 = Result(title='r1',url='www.love.com',summary="Gambo Love")
        self.r2 = Result(title='r2',url='www.isinthe.com',summary="Gambo Food")
        self.r3 = Result(title=' coin gambo collection', url='www.air.com',summary="Gambo Money")
        self.r4 = Result(title='gambo coin collection',url='www.james.com',summary="Gambo Food")
        self.r5 = Result(title='r5',url='www.ryanair.com',summary="Gambo Money")

        self.b1 = add_result_to_folder(self.f1.id, self.r1)
        self.b2 = add_result_to_folder(self.f1.id, self.r2)
        self.b3 = add_result_to_folder(self.f1.id, self.r3)
        self.b4 = add_result_to_folder(self.f2.id, self.r4)
        self.b5 = add_result_to_folder(self.f3.id, self.r5)

    def test_summary_suggestion(self):
        suggestions = suggest_folders(self.ie,'money')

        self.assertItemsEqual([self.f1,self.f3], suggestions)

    def test_title_suggestion(self):
        suggestions = suggest_folders(self.ie,'coin')

        self.assertItemsEqual([self.f1], suggestions)

    def test_title_suggestion(self):
        suggestions = suggest_folders(self.ie,'coin collectio')

        self.assertItemsEqual([self.f1, self.f2], suggestions)