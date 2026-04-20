from generator import copy_file_content, extract_title

def main():
    #copy_file_content("static", ".", "public")
    markdown = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts
"""
    try:
        extract_title(markdown)
    except Exception as e:
        print(e)
main()
