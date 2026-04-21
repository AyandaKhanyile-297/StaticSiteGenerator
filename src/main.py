from generator import copy_file_content, extract_title, generate_page, generate_pages_recursive

def main():
    copy_file_content("static", ".", "public")
    try:
        generate_pages_recursive("content", "template.html", "public")
    except Exception as e:
        print(e)
main()
