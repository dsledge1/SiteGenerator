import os
from os import path
import shutil


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


def main():
    rec_copy("static","public")

   




if __name__ == "__main__":
    main()
