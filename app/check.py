import os

input_dir = 'girl/'
large_files = []

for parent,dirnames,filenames in os.walk(input_dir):
    if len(dirnames) == 0:
        for x in filenames:
            file = '%s/%s' % (parent, x)
            extname = os.path.splitext(x)[1]
            if extname == '.jpg':
                if os.path.getsize(file) > 1024 * 1024:
                    large_files.append(file)

for x in large_files:
    print('remove:', x)
    os.remove(x)