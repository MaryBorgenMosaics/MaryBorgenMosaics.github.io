from __future__ import print_function
import html_img
import sys
import os

def print_out(string):
    print(string, end="",file=sys.stdout)

def print_separate():
    print_out("\n\n\n")
    print_out("-"*50)
    print_out("\n\n\n")

def prologue_info():
    print_out("Editing MaryBorgenMosaics.github.io\n")
    print_out("Code written and maintained by Graham Goudeau\n\n")
    resp = "?"
    while True:
        resp = raw_input("Begin editing? y/n ('n' to quit)... ")
        print_out("\n")
        if resp != 'y' and resp != 'n': continue
        if resp == 'y': return 
        if resp == 'n': sys.exit()

if __name__ == "__main__":
    prologue_info()
    print_separate()
    website = html_img.Website()
    print_out("Website model built...\n")
    print_out("Found gallery pages:\n")
    for page in website.gallery_files:
        print_out("*** " + page.filename + "\n")
        print_out(page.img_list.get_titles())
        print_out("\n")
    website.edit()
    #website.write_pages()
