from __future__ import print_function
import sys
import os

# arg specification: arg 1 - filename ; arg 2 - img prefix
# images to be added with prefix [prfx] must be in img/[prfx]/

if len(sys.argv) != 3:
    print("incorrect usage", file=sys.stderr)
    sys.exit()

GIVEN_PREFIX = sys.argv[2]
IMG_EXT = [".jpg", ".png", ".JPG", ".PNG"]
IMG_PATH = sys.path[0] + "/img/" + GIVEN_PREFIX # add folder indicating prefix to the path
CSS_PATH = sys.path[0] + "/bootstrap-3.3.4-dist/bootstrap-3.3.4-dist/css/custom.css"
HTML_IMG_START = "<!--{IMGSTART}-->"
HTML_IMG_END = "<!--{IMGEND}-->"

# add all images in the directory to list of images
onlyimg = []
for f in os.listdir(IMG_PATH):
    if f[0] == '.': continue

    if os.path.splitext(f)[1] in IMG_EXT:
        onlyimg.append(f)

    # ambiguous file extension
    else:
        print("Add " + f + " to list of images? (y/n)", file=sys.stdout)
        while True:
            response = sys.stdin.read(1)
            if response != 'y' and response != 'n' and \
              response != 'Y' and response != 'N':
                print("Must enter y or n", file=sys.stdout)
                continue
            elif response == 'y' or respose == 'Y':
                onlyimg.append(f)
                break
            else: continue

img_html = ""
for count, img in enumerate(onlyimg):
    print("Adding " + img + " to html file...", file=sys.stdout)
    print("Include this file?", file=sys.stdout)
    add = False
    while True:
        #response = sys.stdin.read(1)
        response = raw_input()
        if response != 'y' and response != 'n' and \
          response != 'Y' and response != 'N':
            print("Must enter y or n; entered " + response + "...", \
                    file=sys.stdout)
            continue
        elif response == 'y' or response == 'Y':
            add = True
            break
        else: break

    if add:
        # image number given before <figure> tag
            # add image tag
        img_html = img_html + "<!--{" + str(count) + "}--><figure>\n" + \
            "\t<img class=\"" + GIVEN_PREFIX + "_" + str(count) + \
            "\" src=\"" + GIVEN_PREFIX + "/img/" + img + "\">\n"

        # add caption
        img_html = img_html + "\t<figcaption class=\"text-center\"><div></div>"
        title = raw_input("Mosaic title: ")
        img_html = img_html + "<p><i>" + title + "</i></p>"
        size = raw_input("Mosaic size: ")
        img_html = img_html + "<p>" + size + "<p></figcaption>\n"

        img_html = img_html + "</figure>\n<hr>\n"
        print(img_html)

img_html = img_html + HTML_IMG_END + "\n"
print(img_html)

filename = open(sys.argv[1], 'r')
text = filename.read()
filename.close()
str_displace = len(HTML_IMG_START) + 1
start_loc = text.index(HTML_IMG_START)

new_text = text[:start_loc + str_displace] + img_html + text[start_loc + str_displace:]
print(new_text)
sys.exit()


current_char = filename.read(1)
current_string = ""
while current_char != "":
    if current_char.isspace():
        current_string = ""
        continue

    #current_string = current_string _ current_
