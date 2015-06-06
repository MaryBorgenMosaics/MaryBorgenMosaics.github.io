''' ALLOWS EDITING OF MARYBORGENMOSAICS.GITHUB.IO
    assumes images have been added to the site with a .jpg or .png extension
    (or .JPG and .PNG), and that each is marked with a <!--{#}--> identifier
    before the <figure> tag.
'''
from __future__ import print_function
import sys
import os

def print_out(string):
    print(string, file=sys.stdout, end="")

def print_err(string):
    print(string, file=sys.stderr, end="")

def init_menu():
    attempts = 0
    html_file = get_html_file_to_edit()
    print_out("\n\n")
    while attempts < 75:
        print_out("Options:\n")
        print_out("\t1) Add an image\n")
        print_out("\t2) Remove an image\n")
        print_out("\t3) Quit\n")

        choice = "?"
        while True:
            choice = raw_input('Enter your choice as a single digit without ' + \
                '\nparentheses (ex. "1" without quotation marks)... ')
            if choice == "1":
                add_image(html_file)
                return
            elif choice == "2":
                remove_image(html_file)
                return
            elif choice == "3":
                print_out("Quitting. Catch ya on the flip side!\n")
                sys.exit()
            else:
                print_out("\nError in your choice...\n")
                attempts += 1
                break

    print_out("Too many bad attempts.  Please restart.  Quitting...\n")
    sys.exit()

def main():
    print_out("Editing MaryBorgenMosaics.github.io\n")
    print_out("Code written and maintained by Graham Goudeau\n")
    print_out("\n\n")

    init_menu()

    sys.exit()

def get_html_file_to_edit():
    html_ext = ".html"
    cur_path = sys.path[0]
    print_out("\n")
    print_out("Which file do you want to edit? (the name " + \
            "of the file corresonds to title of gallery page)\n\n")
    print_out("Please be sure NOT to select the 'index' option.  IMPORTANT!\n")
    html_files = [f for f in os.listdir(cur_path) if \
            os.path.splitext(f)[1] == html_ext]

    # add 1 to num so it looks normal, so we must adjust later
    for num, html_file in enumerate(html_files):
        print_out(str(num + 1) + ") " + html_file.split(".")[0] + "\n")
    print_out("\n")

    response = "?"
    while True:
        response = raw_input("Your choice (or 'quit' to exit): ")
        if response == "quit":
            print_out("See ya later alligator!\n")
            sys.exit()
        if response.isdigit():
            # adjust for adding 1 above
            int_response = int(response) - 1
            if int_response < 0 or int_response >= len(html_files):
                print_out("\n\nInvalid selection.  Try again!\n")
                return get_html_file_to_edit()

            return html_files[int_response]


def add_image(html_file):
    response = get_add_option()

def get_add_option():
    print_out("\n\n")
    print_out("Add image at the end of the page, or insert it at a " + \
            "particular location on the page?\n")
    print_out("e.g., location 1 would be the top of the page, position 2 " + \
            "second from the top, etc.\n")
    print_out("\n")
    response = "?"
    while True:
        response = raw_input("Type 'end' for end of page, or a number " + \
                "for that position on the page (or 'quit')... ")
        if response == "quit":
            print_out("I'm peacin' out...\n")
            sys.exit()
        if response == "end" or response.isdigit():
            return response

def remove_image(html_file):
    print_out("remove image got " + html_file)


if __name__ == "__main__":
    main()
