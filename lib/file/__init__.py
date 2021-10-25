import os
import csv
import codecs

from termcolor import colored

output_path = "outputs"+os.sep

if not os.path.exists(output_path):
    os.mkdir(output_path)

def save2csv(filename, title, datas):
    try:
        with codecs.open(output_path+filename, "w", "utf_8_sig") as file:
            writer = csv.writer(file, lineterminator="\n")

            writer.writerow(title)

            writer.writerows(datas)

        print(colored("[*]", "blue"), "Write Success")
    except PermissionError:
        print(colored("[*]", "red"), "Write Failed, The file is being used.")
        rewrite = input("Whether to rewrite?[Y/n]")
        if rewrite.lower() != "y":
            return
        else:
            save2csv(filename, title, datas)