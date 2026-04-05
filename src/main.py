from textnode import TextNode, TextType
from extrator import split_nodes_image, split_nodes_link

def main():
    node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT)
    new_nodes = split_nodes_image([node])
    node2 = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT)
    new_nodes2 = split_nodes_link([node2])
    print(new_nodes)
    print("#######################")
    print(new_nodes2)

main()