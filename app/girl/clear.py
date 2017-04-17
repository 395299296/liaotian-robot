import os
import os.path

def	remove_files(path, sub=None, remain=True):
	'''
	删除所有文件
	'''
	sub = sub if sub else path;
	if not os.path.exists(sub): return;
	
	if os.path.isdir(sub):
		files = os.listdir(sub);
		for item in files:
			curr = os.path.join(sub, item);
			if item.find('.svn') != -1:
				if remain: continue;
				os.chmod(curr, '777');
			if os.path.isdir(sub):
				remove_files(path, curr);
			else:
				os.remove(curr);
		if path == sub and remain: return;
		
		files = os.listdir(sub);
		if 0 < len(files):
			time.sleep(0.1);
		os.rmdir(sub);
	else:
		os.remove(sub);

remove_dirs = []
for parent,dirnames,filenames in os.walk('.'):
	for x in dirnames:
		file = '%s/个人简介.txt' % x
		if not os.path.exists(file):
			remove_dirs.append(x)
		else:
			with open(file, 'r') as file_object:
				data = file_object.read()
				if '微博' not in data:
					remove_dirs.append(x)

for x in remove_dirs:
	remove_files(x, x, False)
	file = '%s.jpg' % x
	if os.path.exists(file): 
		os.remove(file)