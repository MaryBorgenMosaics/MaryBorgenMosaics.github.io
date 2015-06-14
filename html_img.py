from __future__ import print_function
import sys
import os
import string
import re

IMG_DIR_PREFIX = "img/"

img_start_tag = "<!--{IMGSTART}-->"
img_end_tag = "<!--{IMGEND}-->"
img_exts = ["JPG","jpg","PNG","png"]

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
        self.edit_options = ["add", "remove", "reorder"]

        self.html_files = [HTML_Page(filename) for filename in \
                    os.listdir(self.base_dir) if filename.endswith(".html")]

        self.gallery_files = [page for page in self.html_files \
                                if page.has_images]

    def edit(self):
        html_obj = self.get_html_file_to_edit()
        print_separate()
        print_out("How would you like to modify '" + html_obj.category + "'?\n")
        for num, option in enumerate(self.edit_options):
            print_out(str(num + 1) + ": " + option + "\n")

        resp = ""
        while True:
            try:
                resp = raw_input("Enter the number of your choice " + \
                    "or 'q' to exit: ")
                if resp == 'q': sys.exit()
                resp_int = int(resp) - 1
            except ValueError:
                print_out("Cannot interpret your response as an number\n")
                continue

            if resp_int == 0:
                self.add(html_obj)
                return
            elif resp_int == 1:
                self.remove(html_obj)
                return
            elif resp_int == 2:
                self.reorder(html_obj)
                return
            else:
                print_out("Unknown option.  Try again, ya dangus...\n")

    # DOES NOT adjust for off by one errors
    def numeric_input(self, prompt, on_error):
        resp = ""
        resp_int = -1
        while True:
            try:
                resp = raw_input(prompt)
                if resp == "q": sys.exit()

                resp_int = int(resp)
            except ValueError:
                print_out(on_error)
                continue

            return resp_int

    def add(self, html_obj):
        print_separate()
        print_out("Adding a new image to " + html_obj.category + ":\n")
        print_out("Now we will add information to the image\n")
        print_out("\n")

        # SET the html page that the image resides on
        html_page = html_obj.filename

        # SET the number of sources for the photo(s)
        num_images = 0
        while num_images <= 0 or num_images > 3:
            num_images = self.numeric_input("Number of photos for this " + \
                "mosaic or 'q' to exit (max 3): ", "Invalid response\n")

        # FIND the directory the photo resides in
        print_separate()
        img_path = "img/"
        directories = [direc for direc in os.listdir(sys.path[0] + "/"+ img_path) if \
                            "." not in direc]
        for num, direc in enumerate(directories):
            print_out(str(num + 1) + ": " + direc + "\n")

        choice = -1
        while choice < 0 or choice >= len(directories):
            choice = self.numeric_input("Choose where (inside the " + \
                    "img/ folder) that the " + \
                    "image(s) resides in (or 'q'): ", "Invalid choice\n")
            choice -= 1

        img_path = img_path + directories[choice] + "/"

        # SET all required sources
        src1 = src2 = src3 = ""
        imgs = [img for img in os.listdir(sys.path[0] + "/" + img_path) if img[-3:] in img_exts]
        for num_src in range(num_images):
            print_separate()
            # make a list of all items that end with an image extension
            for num, filename in enumerate(imgs):
                print_out(str(num + 1) + ": " + filename + "\n")

            choice = -1
            while choice < 0 or choice >= len(imgs):
                choice = self.numeric_input("Photo " + str(num_src+1) + "; " + \
                    "Choose which file you want to " + \
                        "add: ", "Invalid choice\n")
                choice -= 1

            if num_src == 0:
                src1 = img_path + imgs[choice]
            elif num_src == 1:
                src2 = img_path + imgs[choice]
            elif num_src == 2:
                src3 = img_path + imgs[choice]

        # Set title, size, third line
        print_separate()
        title = raw_input("Title for this mosaic: ")
        print_separate()
        size = raw_input("Size of this mosaic: ")
        print_separate()
        third_line = raw_input("Third line (or press enter to leave blank): ")

        # generate the image
        new_img = HTML_Img(html_page,src1,src2,src3,title,size,third_line)

        # determine position on the page
        for num, image in enumerate(html_obj.img_list.imgs):
            print_out(str(num + 1) + ": " + image.title + "\n")
        print_out(str(len(html_obj.img_list.imgs) + 1) + ": last on page\n")

        choice = -1
        while choice < 0 or choice > len(html_obj.img_list.imgs):
            choice = self.numeric_input("Select a position on the page " + \
                "for the new work.\n(This will move down all mosaics that " + \
                "come after it): ", "Invalid choice")
            choice -= 1

        if choice == len(html_obj.img_list.imgs) - 1:
            html_obj.img_list.imgs.append(new_img)
        else:
            html_obj.img_list.imgs.insert(choice, new_img)

                
    def remove(self, html_obj):
        pass
    def reorder(self, html_obj):
        img_list = html_obj.img_list.imgs
        print_separate()
        print_out("Found the following images on " + html_obj.category + "\n")
        for num, name in enumerate(html_obj.img_list.get_titles()):
            print_out(str(num + 1) + ": " + name + "\n")

        resp = ""
        resp_int = -1
        while True:
            try:
                resp = raw_input("Enter the number of the image you want " + \
                    "to move, or 'q' to exit: ")
                if resp == "q": sys.exit()

                resp_int = int(resp)
            except ValueError:
                print_out("Whatchu talkin bout? Try again dog...\n")
                continue

            resp_int -= 1
            if resp_int < 0 or resp_int >= len(img_list):
                print_out("Invalid selection, try again\n")
                continue

            break

        original_index = resp_int
        resp = ""
        resp_int = -1
        while True:
            try:
                resp = raw_input("Enter the position on the page you want " + \
                    "to move the image to, or 'q' to exit: ")
                if resp == "q": sys.exit()

                resp_int = int(resp)
            except ValueError:
                print_out("Whatchu talkin bout? Try again dog...\n")
                continue

            resp_int -= 1
            if resp_int < 0 or resp_int >= len(img_list):
                print_out("Invalid selection, try again\n")
                continue

            break

        new_index = resp_int

        img = html_obj.img_list.imgs.pop(original_index)
        html_obj.img_list.imgs.insert(new_index, img)


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

        resp = ""
        while True:
            try:
                resp = raw_input("Enter the number of the page to edit " + \
                    "or 'q' to exit: ")
                if resp == 'q': sys.exit()
                resp_int = int(resp)
            except ValueError:
                print_out("Cannot interpret your response as a number\n")
                continue

            resp_int -= 1 # account for human-readable number choices
            if resp_int < 0 or resp_int >= len(self.gallery_files):
                print_out("Invalid selection\n")
                continue
            else: return self.gallery_files[resp_int]

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
        print(html)
        return html

    def add_img_to_html(self, html, category, src):
        html = html + "\t<img class=\"" + category + "_"
        html = html + str(self.next_img_id()) + "\" "
        html = html + "src=\"" + src + "\">\n"
        return html
