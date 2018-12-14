import os


types = {
    'images': ['jpg', 'png'],
    'sound':['ogg']
}

def static_path(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    static_dir = os.path.join(current_dir, 'static')
    if len(filename.split('.')) == 1:
        for root, dirs, files in os.walk(static_dir):
            if filename in files:
                return os.path.join(root, filename)
    else:
        file_type = filename.split('.')[-1]
        for folder, type_list in types.items():
            if file_type in type_list:
                return os.path.join(static_dir, folder, filename) 
        raise FileNotFoundError(filename)