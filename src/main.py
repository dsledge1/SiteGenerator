import os
from os import path
import shutil
from blocks import *
from htmlnode import *
from splitnode import *
from textnode import *
import sys

print("main.py is running!")

def rec_copy(source, dest):
    pwd = "/home/ostrich/workspace/github.com/dsledge1/SiteGenerator"
    s = os.path.join(pwd, source)
    d = os.path.join(pwd, dest)
    print(f"copying from {s} to {d}")
    print(f"items to be copied: {os.listdir(s)}")
    if not os.path.exists(d):
        os.makedirs(d)
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

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    md = open(from_path, "r").read()
    template = open(template_path, "r").read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", f"{title}")
    template = template.replace("{{ Content }}", f"{html}")
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    if not os.path.isdir(dest_path):
        os.remove(dest_path)
        os.makedirs(dest_path)
    dest_file = os.path.join(dest_path, "index.html")
    with open(dest_file, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    print("Beginning recursive generator")

    dir = dir_path_content
    pwd = os.path.join("/home/ostrich/workspace/github.com/dsledge1/SiteGenerator",dir)
    print(f"Current directory is {dir} and contents are {os.listdir(dir)}")
    for item in os.listdir(dir):
        current_path = os.path.join(pwd,item)
        print(f"current path is {current_path}")
        if os.path.isdir(os.path.join(pwd,item)):
            print(f"Directory found {item}")
            new_dir = os.path.join(pwd, item)
            new_des = os.path.join(dest_dir_path, item)
            print(f"Directory found, moving into {new_dir}, new destination is {new_des}")
            generate_pages_recursive(new_dir, template_path, new_des, basepath)
        elif os.path.isfile(os.path.join(pwd,item)) and item.endswith(".md"):
            print(f"Markdown file found: {item}")
            generate_page(os.path.join(pwd,item), template_path, dest_dir_path, basepath)
        


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    rec_copy("static","docs")
    #generate_page("content/index.md","template.html","public")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
