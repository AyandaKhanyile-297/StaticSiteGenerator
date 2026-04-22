import os
import shutil
from extrator import markdown_to_html_node

# copy_file_content -> Helper
def file_transfers(from_name, to_name):
    for _file in os.listdir(from_name):
        src_file = os.path.join(from_name, _file)
        if os.path.isfile(src_file):
            shutil.copy(src_file,to_name)
        else:
            dest_file = os.path.join(to_name, _file)
            os.mkdir(dest_file)
            file_transfers(src_file, dest_file)
                
# Copies files and sub-directories to another directory
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

# Extracts a title from a markdown file
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
   
# Generates a webpage using a markdown file and template (generate_pages_recursive -> Helper)
def generate_page(from_path, template_path, dest_path, basepath):
    from_dir = os.path.abspath(from_path)
    temp_dir = os.path.abspath(template_path)
    dest_dir = os.path.abspath(dest_path)
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}\n")
    
    contents_src = get_content(from_dir)
    contents_temp = get_content(temp_dir)
    
    ext_title = extract_title(contents_src)
    converted_markdown = (markdown_to_html_node(contents_src)).to_html()
    contents_dest = replace_content(contents_temp, ext_title, converted_markdown)

    contents_dest = contents_dest.replace("href=\"/", f"href=\"{basepath}")
    contents_dest = contents_dest.replace("src=\"/", f"src=\"{basepath}")
    contents_dest = contents_dest.replace("href=/", f"href={basepath}")
    contents_dest = contents_dest.replace("src=/", f"src={basepath}")
    
    print(write_content(dest_dir, contents_dest))  

# generate_page -> Helper 
def get_content(pathname):
    try:
        if not os.path.isfile(pathname):
            return f"Error: File not found or is not a regular file: {pathname}"
        with open(pathname, "r") as f:
            file_contents = f.read()
        return file_contents
    except Exception as err:
        return f"Error: {err} has occurred!"

# generate_page -> Helper 
def replace_content(original, rep_Title, rep_Content):  
    newContent = original.replace("{{ Title }}",rep_Title)
    newContent = newContent.replace("{{ Content }}",rep_Content)
    return newContent
    
# generate_page -> Helper 
def write_content(pathname, data):
    try:
        valid_dir = pathname.replace("/index.html","")
        if not os.path.isdir(valid_dir):
            os.makedirs(valid_dir)
        with open(pathname, "w") as f:
            f.write(data)
        return f'Successfully wrote to "{pathname}".'
    except Exception as err:
        return f"Error: {err}!"   
        
# Generates a webpages using a directory of markdown file and a template
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, newBasepath="/"):
    for directory in os.listdir(dir_path_content):
        from_filepath = os.path.join(dir_path_content, directory)
        if os.path.isfile(from_filepath):
            dest_filepath = os.path.join(dest_dir_path, "index.html")
            generate_page(from_filepath, template_path, dest_filepath, newBasepath)
        else:
            dest_filepath = os.path.join(dest_dir_path, directory)
            generate_pages_recursive(from_filepath, template_path, dest_filepath, newBasepath)