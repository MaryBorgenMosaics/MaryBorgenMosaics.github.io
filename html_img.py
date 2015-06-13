from __future__ import print_function
import sys
import os
import string
import re

IMG_DIR_PREFIX = "img/"

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
        self.img_start_tag = "<!--{IMGSTART}-->"
        self.img_end_tag = "<!--{IMGEND}-->"
        self.has_images = self.determine_gallery()
        self.img_list = self.populate_arr()
        if self.img_list:
            for img in self.img_list.imgs:
                print(img.title)

    def determine_gallery(self):
        with open(self.filename, 'r') as open_html:
            text = open_html.read()
            print(self.filename + " determined: ", self.img_start_tag in text and self.img_end_tag in text)
            return self.img_start_tag in text and self.img_end_tag in text

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

    def next_img_id(self):
        value = self.img_id
        self.img_id += 1
        return value

    def write_pages(self):
        for gal_page in self.gallery_files:
            open_file = open(gal_page.filename, 'r')
            text = open_file.read()
            open_file.close()

            new_img_html = self.generate_html(gal_page)

    def generate_html(self, gal_page):
        html = ""
        for img in gal_page.img_list.imgs:
            print("Generating HTML for " + img.title)
            img_1_id_str = str(self.next_img_id())
            img_2_id_str = str(self.next_img_id())
            img_3_id_str = str(self.next_img_id())
            category = gal_page.category
            html = html + "<figure>\n"
            html = html + "\t<img class=\"" + category + "_" + img_1_id_str
            html = html + "\" src=\""
            print(html)
            print("\n\n")
