import argparse
import os
from bs4 import BeautifulSoup
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html_file", help="path to the HTML file")
    args = parser.parse_args()

    output_path = "output"
    # ensure path exists
    Path(output_path).mkdir(parents=True, exist_ok=True)

    with open(args.html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style tags and their content
    for tag in soup(["script", "style"]):
        tag.decompose()
    
    # remove all CSS link tags
    # (for better HTML debug, as the linked CSS breaks scroll)
    for tag in soup.select("link"):
        tag.decompose()
    
    # remove the title tag, as it bleeds into the rendered text
    for tag in soup.select("title"):
        tag.decompose()
    
    
    sidebar = ".dark"
    # let beautifulsoup remove all divs with class dark
    for tag in soup.select(sidebar):
        tag.decompose()

    # pseudo-classes removed, as BS don't support them
    # classes with forward slashes removed, as BS don't support them
    human_class = "group w-full text-gray-800 border-b"
    # gpt_class = "group w-full text-gray-800 border-b bg-gray-50"
    # let beautifulsoup remove all divs with human_class, but keep the gpt_class
    for tag in soup.select(".group"):
        # if tag has class bg-gray-50, then keep it
        if tag.has_attr('class') and 'bg-gray-50' in tag['class']:
            continue
        tag.decompose()
    
    # remove footer, which has class .bottom-0
    for tag in soup.select(".bottom-0"):
        tag.decompose()

    # Remove HTML tags and keep only the text content
    text = soup.get_text()

    with open(f"{output_path}/output.txt", "w") as f:
        f.write(text)
    
    # print out .group divs line by line, with line break, to a text file
    with open(f"{output_path}/output_formatted.txt", "w") as f:
        for tag in soup.select(".group"):
            f.write(tag.text)
            # get os-specific line break
            f.write(os.linesep)
            f.write(os.linesep)


    # also save the modified html to a new file
    input_folder, input_html_file = os.path.split(args.html_file)
    output_html_file = "modified_" + input_html_file
    output_html_path = os.path.join(input_folder, output_html_file)
    with open(output_html_path, "w") as f:
        f.write(str(soup))


if __name__ == "__main__":
    main()
