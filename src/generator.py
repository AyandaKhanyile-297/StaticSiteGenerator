import os
import shutil

def file_transfers(from_name, to_name):
    for _file in os.listdir(from_name):
        src_file = os.path.join(from_name, _file)
        if os.path.isfile(src_file):
            shutil.copy(src_file,to_name)
        else:
            dest_file = os.path.join(to_name, _file)
            os.mkdir(dest_file)
            file_transfers(src_file, dest_file)
                
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
        file_transfers(from_name, to_name)
        
    except Exception as e:
        return (f"Error: {e}")

###
def extract_title(markdown):
    markdown_title = ""
    markdown_tag = "# "
    lines = markdown.split("\n\n")
    for line in lines:
        block = line.strip()
        if block.startswith(f"{markdown_tag}"):
            markdown_title = block.replace(f"{markdown_tag}","")
    
    if markdown_title == "":
        raise Exception("No valid title!")
    return markdown_title
    