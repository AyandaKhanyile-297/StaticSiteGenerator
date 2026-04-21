from generator import copy_file_content, extract_title, generate_page

def main():
    copy_file_content("static", ".", "public")
    try:
        generate_page("content/index.md", "template.html", "public/index.html")
    except Exception as e:
        print(e)
main()
