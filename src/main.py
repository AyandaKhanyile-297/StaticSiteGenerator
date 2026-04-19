import os
import shutil

def copy_file_content(from_directory, directory, to_directory):
    try:
        from_dir = os.path.abspath(from_directory)
        from_name = os.path.normpath(os.path.join(from_dir, directory))
        
        to_dir = os.path.abspath(to_directory)
        to_name = os.path.normpath(os.path.join(to_dir, directory))
        
        if (not os.path.isdir(from_name)) or (not os.path.isdir(to_name)):
            return f'Error: "{directory}" is not a directory'
    
        shutil.rmtree(to_name)
        os.mkdir(to_name)
        
        for _file in os.listdir(from_name):
            src_file = os.path.join(from_name, _file)
            if os.path.isfile(src_file):
                shutil.copy(src_file,to_name)
            else:
                copy_file_content(src_file,to_name)
                
        return os.listdir(to_name)
        
    except Exception as e:
        return (f"Error: {e}")


def main():
    print(copy_file_content("static", ".", "public"))
main()
