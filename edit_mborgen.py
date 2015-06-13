from __future__ import print_function
import html_img
import sys
import os

def print_out(string):
    print(string, file=sys.stdout)

if __name__ == "__main__":
    website = html_img.Website()
    for page in website.gallery_files:
        print(page.img_list.get_titles())
    print("ready",file=sys.stdout)
