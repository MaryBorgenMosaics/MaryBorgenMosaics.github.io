from __future__ import print_function
import sys
import os
import string
import re

IMG_DIR_PREFIX = "img/"
img_start_tag = "<!--{IMGSTART}-->"
img_end_tag = "<!--{IMGEND}-->"

def print_out(string):
    print(string, end="", file=sys.stdout)

def print_separate():
    print_out("\n\n\n")
    print_out("-"*50)
    print_out("\n\n\n")

class HTML_Img:
    def __init__(self, html_page, src1, src2, src3, title, size, third_line=""):
        self.src1, self.src2, self.src3 = src1, src2, src3
        self.title = title
        self.size = size
        self.html_page = html_page
        self.third_line = third_line

class Arr_HTML_Img:
    def __init__(self):
        self.imgs = []

    def add_img(self, img):
        self.imgs.append(img)

    def remove_by_title(self, title):
        titles = get_titles()
        if title not in titles:
            return

        for img in self.imgs:
            if img.title == title:
                deleted_img = img

        self.imgs.remove(deleted_img)

    def get_titles(self):
        return [img.title for img in self.imgs]

class HTML_Page:
    def __init__(self, filename):
        self.filename = filename
        self.category = filename.split(".")[0]
        self.has_images = self.determine_gallery()
        self.img_list = self.populate_arr()

    def determine_gallery(self):
        with open(self.filename, 'r') as open_html:
            text = open_html.read()
            return img_start_tag in text and img_end_tag in text

    def populate_arr(self):
        arr = Arr_HTML_Img()
        with open(self.filename, 'r') as open_html:
            text = open_html.read()
            #pattern = r'src="(.*)">\s*<figcaption.*><i>(.*)<\/i><\/p><p>(.*)<\/p><p>(.*)<\/p><\/figcaption>'
            pattern = r'src="(.*)".*\n.*src="(.*)".*\n.*src="(.*)">\s*.*><i>(.*)<\/i><\/p><p>(.*)<\/p><p>(.*)<\/p>'
            match = re.findall(pattern, text)
            for img in match:
                src1,src2,src3,title,size,third_line = img
                arr.add_img(HTML_Img(self.filename,src1,src2,src3,title,size,third_line))

        if len(arr.imgs) > 0:
            return arr
        else:
            return None

class Website:
    def __init__(self):
        self.base_dir = sys.path[0]
        self.img_id = 0L

        self.html_files = [HTML_Page(filename) for filename in \
                    os.listdir(self.base_dir) if filename.endswith(".html")]

        self.gallery_files = [page for page in self.html_files \
                                if page.has_images]

    def edit(self):
        html_obj = self.get_html_file_to_edit()
        print(html_obj)

    def next_img_id(self):
        value = self.img_id
        self.img_id += 1
        return value

    def get_html_file_to_edit(self):
        print_separate()
        print_out("Found the following pages with images:\n")
        for num, html_obj in enumerate(self.gallery_files):
            # adjust the choices for human-readable, e.g. start at 1
            print_out(str(num + 1) + ": " + html_obj.category + "\n")

        resp = -1
        while True:
            try:
                resp = int(raw_input("Enter the number of the page to edit: "))
            except ValueError:
                print_out("Cannot convert your response into number\n")
                continue

            resp -= 1 # account for human-readable number choices
            if resp < 0 or resp > len(self.gallery_files):
                print_out("Invalid selection\n")
                continue
            else: return self.gallery_files[resp]

    def write_pages(self):
        for gal_page in self.gallery_files:
            open_file = open(gal_page.filename, 'r')
            text = open_file.read()
            open_file.close()

            new_img_html = self.generate_html(gal_page)
            img_start = text.index(img_start_tag)
            img_end = text.index(img_end_tag) + len(img_end_tag)
            write_text = text[:img_start] + new_img_html + text[img_end:]

            with open(gal_page.filename, 'w') as updated_file:
                updated_file.write(write_text)

    def generate_html(self, gal_page):
        html = img_start_tag + "\n"
        for img in gal_page.img_list.imgs:
            print("Generating HTML for " + img.title)
            category = gal_page.category
            html = html + "<figure>\n"
            html = self.add_img_to_html(html, category, img.src1)
            html = self.add_img_to_html(html, category, img.src2)
            html = self.add_img_to_html(html, category, img.src3)
            html = html + "\t<figcaption class=\"text-center\">"
            html = html + "<div></div><p><i>" + img.title + "</i></p>"

            html = html + "<p>" + img.size + "</p>"
            html = html + "<p>" + img.third_line + "</p>"
            html = html + "</figcaption>"

            html = html + "\n"
            html = html + "</figure>\n<hr>\n"

        html = html + img_end_tag
        return html

    def add_img_to_html(self, html, category, src):
        html = html + "\t<img class=\"" + category + "_"
        html = html + str(self.next_img_id()) + "\" "
        html = html + "src=\"" + src + "\">\n"
        return html
