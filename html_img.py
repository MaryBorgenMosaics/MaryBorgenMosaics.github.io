from __future__ import print_function
import sys
import os
import string
import re

IMG_DIR_PREFIX = "img/"

class HTML_Img:
    def __init__(self, html_page, src, title, size, third_line=""):
        if not src.startswith(IMG_DIR_PREFIX):
            self.src = IMG_DIR_PREFIX + src
        else:
            self.src = src

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
                print(img.src)

    def determine_gallery(self):
        with open(self.filename, 'r') as open_html:
            text = open_html.read()
            return self.img_start_tag in text and self.img_end_tag in text

    def populate_arr(self):
        arr = Arr_HTML_Img()
        with open(self.filename, 'r') as open_html:
            text = open_html.read()
            pattern = r'src="(.*)">\s*<figcaption.*><i>(.*)<\/i><\/p><p>(.*)<\/p><p>(.*)<\/p><\/figcaption>'
            match = re.findall(pattern, text)
            for img in match:
                src,title,size,third_line = img
                arr.add_img(HTML_Img(self.filename,src,title,size,third_line))

        if len(arr.imgs) > 0:
            return arr
        else: return None

class Website:
    def __init__(self):
        self.base_dir = sys.path[0]

        self.html_files = [HTML_Page(filename) for filename in \
                    os.listdir(self.base_dir) if filename.endswith(".html")]

        self.gallery_files = [page for page in self.html_files \
                                if page.has_images]

        for page in self.html_files:
            print(page.filename)
        for page in self.gallery_files:
            print(page.category)



'''
page = HTML_Page("test.html")
print(page.has_images)
img = HTML_Img("img.JPG","newMosaic","60' x 40'","testpage.html")
arr = Arr_HTML_Img()
arr.add_img(img)
arr.add_img(HTML_Img("new.JPG","oldMosaic","100","newpage.html"))
dump = pickle.dumps(arr)
new_arr = pickle.loads(dump)
print(new_arr)
for img in new_arr.imgs:
    print(img.html_page)
'''
website = Website()
