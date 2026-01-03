from textnode import TextNode, TextType
def main():
    t = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(t)

if __name__ == "__main__":
    main()
