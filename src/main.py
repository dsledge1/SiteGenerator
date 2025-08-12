import os
from os import path
import shutil
from blocks import *
from htmlnode import *
from splitnode import *
from textnode import *

def rec_copy(source, dest):
    pwd = "/home/dsledge1/workspace/github.com/dsledge1/SiteGenerator"
    s = os.path.join(pwd, source)
    d = os.path.join(pwd, dest)
    print(f"copying from {s} to {d}")
    print(f"items to be copied: {os.listdir(s)}")
    if os.path.exists(d):
        if os.listdir(d):
            print(f"Destination is not empty, deleting destination tree at {d}")
            shutil.rmtree(d)
            print(f"making fresh directory {d}")
            os.mkdir(d)
    for item in os.listdir(s):
        i = os.path.join(s, item)
        print(f"processing {i}")
        if os.path.isdir(i):
            print(f"{item} is a directory")
            new_dest = os.path.join(d, item)
            print(f"{new_dest} is the new correponding target directory")
            if not os.path.exists(new_dest):
                print(f"{new_dest} does not exist, creating directory")
                os.makedirs(new_dest)
            print(f"Recursively copying files inside {item}")
            rec_copy(os.path.join(s, item), new_dest)
        elif not os.path.isdir(i):
            print(f"Copying {item} from {s} to {d}")
            shutil.copy(os.path.join(s,item), d)
            print(f"{item} copied successfully")

def extract_title(markdown):
    string = markdown.strip()
    lines = string.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ").strip()
        else:
            raise Exception("No header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    md = open(from_path, "r").read()
    template = open(template_path, "r").read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", f"{title}")
    template = template.replace("{{ Content }}", f"{html}")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dest_file = os.path.join(dest_path, "index.html")
    with open(dest_file, "w") as f:
        f.write(template)



def main():
    rec_copy("static", "public")
    generate_page("content/index.md","template.html","public")


if __name__ == "__main__":
    main()
