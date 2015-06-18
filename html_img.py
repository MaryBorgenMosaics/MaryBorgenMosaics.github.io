from __future__ import print_function
import sys
import os
import string
import re

IMG_DIR_PREFIX = "img/"

img_start_tag = "<!--{IMGSTART}-->"
img_end_tag = "<!--{IMGEND}-->"
css_start_tag = "<!--{CUSTOMCSSSTART}-->"
css_end_tag = "<!--{CUSTOMCSSEND}-->"

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
        self.fields = ["image 1","image 2", "image 3", "title", "size", \
                "third line"]

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
        self.edit_options = ["add", "remove", "reorder", "change info"]

        self.html_files = [HTML_Page(filename) for filename in \
                    os.listdir(self.base_dir) if filename.endswith(".html")]

        self.gallery_files = [page for page in self.html_files \
                                if page.has_images]

    def edit(self):
        resp = ""
        while True:
            html_obj = self.get_html_file_to_edit()
            print_separate()
            print_out("How would you like to modify '" + html_obj.category + "'?\n")
            for num, option in enumerate(self.edit_options):
                print_out(str(num + 1) + ": " + option + "\n")

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
            elif resp_int == 1:
                self.remove(html_obj)
            elif resp_int == 2:
                self.reorder(html_obj)
            elif resp_int == 3:
                self.change_info(html_obj)
            else:
                print_out("Unknown option.  Try again, ya dangus...\n")

            print_separate()
            resp = ""
            while True:
                resp = raw_input("Have another change to make? (y/n) ")
                if resp != 'y' and resp != 'n': continue

                break

            if resp == 'n': break

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
        print_separate()
        for num, image in enumerate(html_obj.img_list.imgs):
            print_out(str(num + 1) + ": " + image.title + "\n")
        print_out(str(len(html_obj.img_list.imgs) + 1) + ": last on page\n")

        choice = -1
        while choice < 0 or choice > len(html_obj.img_list.imgs):
            choice = self.numeric_input("Select a position on the page " + \
                "for the new work.\n(This will move down all mosaics that " + \
                "come after it): ", "Invalid choice\n")
            choice -= 1

        if choice == len(html_obj.img_list.imgs) - 1:
            html_obj.img_list.imgs.append(new_img)
        else:
            html_obj.img_list.imgs.insert(choice, new_img)

                
    def remove(self, html_obj):
        img_list = html_obj.img_list.imgs
        print_separate()
        print_out("Found the following images on " + html_obj.category + "\n")
        for num, name in enumerate(html_obj.img_list.get_titles()):
            print_out(str(num + 1) + ": " + name + "\n")

        choice = -1
        while choice < 0 or choice > len(html_obj.img_list.imgs):
            choice = self.numeric_input("Select the image to remove: ", \
                            "Invalid choice\n")
            choice -= 1

        html_obj.img_list.imgs.pop(choice)

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

    def change_info(self, html_obj):
        img_list = html_obj.img_list.imgs
        print_separate()
        print_out("Found the following images on " + html_obj.category + "\n")
        for num, name in enumerate(html_obj.img_list.get_titles()):
            print_out(str(num + 1) + ": " + name + "\n")

        choice = -1
        while choice < 0 or choice > len(html_obj.img_list.imgs):
            choice = self.numeric_input("Select the image to change: ", \
                            "Invalid choice\n")
            choice -= 1

        print_separate()
        print_img_fields = html_obj.img_list.imgs[choice]
        print_out("Current information for " + print_img_fields.title + ":\n")
        print_out("\tTitle: " + print_img_fields.title + "\n")
        print_out("\tSize: " + print_img_fields.size + "\n")
        if print_img_fields.src1:
            print_out("\tFile 1: " + print_img_fields.src1 + "\n")
        if print_img_fields.src2:
            print_out("\tFile 2: " + print_img_fields.src2 + "\n")
        if print_img_fields.src3:
            print_out("\tFile 3: " + print_img_fields.src3 + "\n")
        if print_img_fields.third_line:
            print_out("\tThird description line: " + print_img_fields.third_line + "\n")

        print_out("\n\n")
        fields = html_obj.img_list.imgs[choice].fields
        for num, field in enumerate(fields):
            print_out(str(num + 1) + ": " + field + "\n")
        
        field_choice = -1
        while field_choice < 0 or field_choice > len(fields):
            field_choice = self.numeric_input("Select the field you want to change: ", \
                            "Invalid choice\n")
            field_choice -= 1

        if field_choice >= 0 and field_choice <= 2:
            new_value = self.get_new_source(html_obj)
        else:
            new_value = raw_input("New value for " + fields[field_choice] + ": ")

        if field_choice == 0:
            html_obj.img_list.imgs[choice].src1 = new_value
        elif field_choice == 1:
            html_obj.img_list.imgs[choice].src2 = new_value
        elif field_choice == 2:
            html_obj.img_list.imgs[choice].src3 = new_value
        elif field_choice == 3:
            html_obj.img_list.imgs[choice].title = new_value
        elif field_choice == 4:
            html_obj.img_list.imgs[choice].size = new_value
        elif field_choice == 5:
            html_obj.img_list.imgs[choice].third_line = new_value    

    def get_new_source(self, html_obj):
        html_page = html_obj.filename

        # FIND the directory the photo resides in
        print_separate()
        img_path = "img/"
        directories = [direc for direc in os.listdir(sys.path[0] + "/"+ img_path) if \
                            "." not in direc]
        for num, direc in enumerate(directories):
            print_out(str(num + 1) + ": " + direc + "\n")
        print_out(str(len(directories) + 1) + ": remove image\n")

        choice = -1
        while choice < 0 or choice > len(directories):
            choice = self.numeric_input("Choose where (inside the " + \
                    "img/ folder) that the " + \
                    "image(s) resides in (or 'q'): ", "Invalid choice\n")
            choice -= 1

        if choice == len(directories): return ""
        img_path = img_path + directories[choice] + "/"

        # SET all required sources
        imgs = [img for img in os.listdir(sys.path[0] + "/" + img_path) if img[-3:] in img_exts]
        print_separate()
        # make a list of all items that end with an image extension
        for num, filename in enumerate(imgs):
            print_out(str(num + 1) + ": " + filename + "\n")

        choice = -1
        while choice < 0 or choice >= len(imgs):
            choice = self.numeric_input("Choose which file you want to " + \
                    "add: ", "Invalid choice\n")
            choice -= 1

        return img_path + imgs[choice]

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

            new_html_css_tuple = self.generate_html_css_codes(gal_page)
            new_img_html, new_img_css = new_html_css_tuple
            #new_img_html = self.generate_html(gal_page)
            css_path = "bootstrap-3.3.4-dist/bootstrap-3.3.4-dist/css/"
            css_path = css_path + gal_page.category + "_css.css"

            css_meta_tag = css_start_tag + "\n\t"
            css_meta_tag = css_meta_tag + "<link rel=\"stylesheet\" href=\""
            css_meta_tag = css_meta_tag + css_path + "\">\n"
            css_meta_tag = css_meta_tag + "\t" + css_end_tag 

            css_start = text.index(css_start_tag)
            css_end = text.index(css_end_tag) + len(css_end_tag)
            write_text = text[:css_start] + css_meta_tag + text[css_end:] 

            img_start = write_text.index(img_start_tag)
            img_end = write_text.index(img_end_tag) + len(img_end_tag)
            write_text = write_text[:img_start] + new_img_html + write_text[img_end:]

            with open(gal_page.filename, 'w') as updated_file:
                updated_file.write(write_text)

            with open(css_path, 'w') as new_css:
                for cur_id in new_img_css:
                    new_css.write(self.gen_css(gal_page.category, cur_id))

    def gen_css(self, category, cur_id):
        css = "." + category + "_" + str(cur_id) + " {\n"
        css = css + "\tpadding: 70px;\n\tdisplay: block;\n"
        css = css + "\tmargin-left: auto;\n\tmargin-right: auto;\n"
        css = css + "\tmax-width: 60%;\n\tmax-height: 60%;\n"
        css = css + "\tborder-style: solid;\n\tborder-color: #000;\n"
        css = css + "\tborder-width: thin;\n}\n"

        return css

    def generate_html_css_codes(self, gal_page):
        css_codes = []
        html = img_start_tag + "\n"
        for img in gal_page.img_list.imgs:
            print("Generating HTML for " + img.title)
            new_id1 = self.next_img_id()
            if img.src1: css_codes.append(str(new_id1))
            new_id2 = self.next_img_id()
            if img.src2: css_codes.append(str(new_id2))
            new_id3 = self.next_img_id()
            if img.src3: css_codes.append(str(new_id3))
            category = gal_page.category
            html = html + "<figure>\n"
            html = self.add_img_to_html(html, category, img.src1, new_id1)
            html = self.add_img_to_html(html, category, img.src2, new_id2)
            html = self.add_img_to_html(html, category, img.src3, new_id3)
            html = html + "\t<figcaption class=\"text-center\">"
            html = html + "<div></div><p><i>" + img.title + "</i></p>"

            html = html + "<p>" + img.size + "</p>"
            html = html + "<p>" + img.third_line + "</p>"
            html = html + "</figcaption>"

            html = html + "\n"
            html = html + "</figure>\n<hr>\n"

        html = html + img_end_tag
        return (html, css_codes)

    def add_img_to_html(self, html, category, src, new_id):
        html = html + "\t<img class=\"" + category + "_"
        html = html + str(new_id) + "\" "
        html = html + "src=\"" + src + "\">\n"
        return html
