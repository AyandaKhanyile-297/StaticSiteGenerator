from generator import copy_file_content, extract_title, generate_page

def main():
    copy_file_content("static", ".", "public")
    try:
        generate_page("content/index.md", "template.html", "public/index.html")
        
        generate_page("content//blog/glorfindel/index.md", "template.html", "public//blog/glorfindel/index.html")
        generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
        generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
        generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
        
    except Exception as e:
        print(e)
main()
