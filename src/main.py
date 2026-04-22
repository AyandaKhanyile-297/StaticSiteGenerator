import sys
import os
from generator import copy_file_content, extract_title, generate_page, generate_pages_recursive

def main():
    basepath = sys.argv[1]
    copy_file_content("static", ".", "docs")
    try:
        if len(basepath) > 0:
            generate_pages_recursive("content", "template.html", "docs", basepath)
        else:
            generate_pages_recursive("content", "template.html", "docs")
    except Exception as e:
        print(e)
main()
