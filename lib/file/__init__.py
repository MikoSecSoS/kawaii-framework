import os
import csv

from termcolor import colored

output_path = "outputs"+os.sep

if not os.path.exists(output_path):
    os.mkdir(output_path)

def save2csv(filename, title, datas):
    with open(output_path+filename, "w") as file:
        writer = csv.writer(file, lineterminator="\n")

        writer.writerow(title)

        writer.writerows(datas)

    print(colored("[*]", "blue"), "Write Success")