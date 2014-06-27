import os

def populate():
	Jean = User.objects.create_user('Jean',None, 'Jeanpassword')
	Jean.save()
	Wen = User.objects.create_user('Wen',None, 'Wenpassword')
	Wen.save()
	f_Misc_Trees_and_Graphs_Wen = add_folder(name='Misc Trees and Graphs',times_used=4,user=Wen)
	f_Online_Editors_Jean = add_folder(name='Online Editors',times_used=4,user=Jean)




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
	from dragondrop.models import User, Bookmark, Folder, BinFolder, BookmarkToFolder 
	populate()