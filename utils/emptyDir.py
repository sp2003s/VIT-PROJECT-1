import os, shutil

def empty_dir(dir_name):
    
    current_directory = os.path.dirname(__file__)
    directory_path = os.path.join(current_directory, dir_name)
    
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                
        return f'{dir_name} has been emptied'
    
    else:
        return f'{dir_name} does not exist'    