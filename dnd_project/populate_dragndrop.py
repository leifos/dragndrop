import os

def populate():
    Jean = User.objects.create_user('Jean',None, 'password')
    Jean.save()
    Wen = User.objects.create_user('Wen',None, 'password')
    Wen.save()
    f_Misc_Trees_and_Graphs_Wen = add_folder(name='Misc Trees and Graphs',times_used=4,user=Wen)
    f_1_Wen = add_folder(name='Folder 1',times_used=4,user=Wen)
    f_2_Wen = add_folder(name='Folder 2',times_used=4,user=Wen)
    f_3_Wen = add_folder(name='Folder 3',times_used=4,user=Wen)
    f_4_Wen = add_folder(name='Folder 4',times_used=4,user=Wen)
    f_5_Wen = add_folder(name='Folder 5',times_used=4,user=Wen)
    f_Online_Editors_Jean = add_folder(name='Online Editors',times_used=4,user=Jean)
    google = add_bookmark("Google", "A search engine", "http://www.google.com", 2, f_Misc_Trees_and_Graphs_Wen)
    yahoo = add_bookmark("Yahoo!", "An old website", "http://www.yahoo.com", 4, f_Misc_Trees_and_Graphs_Wen)
    github = add_bookmark("Github", "A code site", "http://www.github.com", 5, f_Online_Editors_Jean)
    bookmark1 = add_bookmark("cat", "search for cat", "https://www.google.com/?pws=0&q=cat", 5, f_1_Wen)
    bookmark2 = add_bookmark("dog", "search for dog", "https://www.google.com/?pws=0&q=dog", 5, f_1_Wen)
    bookmark3 = add_bookmark("horse", "search for horse", "https://www.google.com/?pws=0&q=horse", 5, f_1_Wen)
    bookmark4 = add_bookmark("cow", "search for cow", "https://www.google.com/?pws=0&q=cow", 5, f_1_Wen)
    bookmark5 = add_bookmark("fish", "search for fish", "https://www.google.com/?pws=0&q=fish", 5, f_1_Wen)


def add_bookmark(title, summary, url, clicks, folder):
    bm = Bookmark.objects.get_or_create(title=title, summary=summary, url=url,
                                        clicks=clicks, folder=folder)[0]
    return bm

def add_folder(name, times_used, user):
    f = Folder.objects.get_or_create(name=name, times_used=times_used, user=user)[0]
    return f

def add_profile(histories, popular, recently_used, user):
    p = Folder.objects.get_or_create(histories=histories, popular=popular,
                                     recently_used=recently_used, user=user)[0]
    return p


# Start execution here!
if __name__ == '__main__':
    print 'Starting DragonDrop population script...'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnd_project.settings')
    from dragndrop.models import User, Bookmark, Folder, Profile
    populate()