import tkinter as tk
from tkinter import filedialog
import getopt
import sys
import os
import re
from tqdm import tqdm

### Get command-line arguments
args = sys.argv[1:]
options = "hg:s:d:"
long_options = ["help", "garmin-directory=", "strengthlevel-directory=", "directory="]

garmin_md_path = "interactive"
sl_md_path = "interactive"
output_dir = os.getcwd() + "/output"

try:
    arguments, values = getopt.getopt(args, options, long_options)
    for arg, val in arguments:
        if arg in ("-h", "--help"):
            help_string = \
"""Usage: garminslcombinemd.py [-h] [-g <garmin directory>] [-s <strength level directory>] [-d <output directory>]
Options:
    -h --help                       : Print this help and exit.
    -g --garmin-directory           : Path to directory with Garmin markdown files or "interactive". Default: interactive.
    -s --strengthlevel-directory    : Path to directory with Garmin markdown files or "interactive". Default: interactive.
    -d --directory                  : Output directory to save .md files to. Default: working directory."""

            print(help_string)
            sys.exit()

        if arg in ("-g", "--garmin-directory"):
            garmin_md_path = val
            if not os.path.exists(garmin_md_path):
                raise FileExistsError("\nProvided Garmin markdown directory path does not exist.")

        if arg in ("-s", "--strengthlevel-directory"):
            sl_md_path = val
            if not os.path.exists(sl_md_path):
                raise FileExistsError("\nProvided Strength Level markdown directory path does not exist.")

        if arg in ("-d", "--directory"):
            output_dir = val
            if not os.path.exists(output_dir):
                try:
                    os.mkdir(output_dir)
                except Exception as e:
                    raise FileExistsError("\nProvided output directory does not exist and could not be created.") from e
            
#        if arg in ("-o", "--frontmatter"):
#            frontmatter = val
#            if frontmatter not in ["none", "joplin"]:
#                raise ValueError("\nProvided frontmatter is not supported. Possible values: none, joplin.")

except getopt.error as err:
    print(str(err))

print(" ")
print(f"Running garminslcombinemd with the following parameters:\n   Garmin input directory: {garmin_md_path}\n   Strength Level input directory: {sl_md_path}\n   Output directory: {output_dir}\n")

### Get input directories
if garmin_md_path == "interactive":
    root = tk.Tk()
    root.withdraw()
    root.call("wm", "attributes", ".", "-topmost", True)
    garmin_md_path = filedialog.askdirectory(
        title="Select Garmin markdown directory", initialdir=os.getcwd()
    )
    print("Selected Garmin markdown directory:")
    print(garmin_md_path, "\n")

if sl_md_path == "interactive":
    root = tk.Tk()
    root.withdraw()
    root.call("wm", "attributes", ".", "-topmost", True)
    sl_md_path = filedialog.askdirectory(
        title="Select Strength Level markdown directory", initialdir=os.getcwd()
    )
    print("Selected Strength Level markdown directory:")
    print(sl_md_path, "\n")

### Add SL summary to garmin files
garmin_files = [file for file in os.listdir(garmin_md_path) if file.endswith(".md")]
sl_files = [file for file in os.listdir(sl_md_path) if file.endswith(".md")]

if not garmin_files:
    print("Selected Garmin markdown directory does not contain .md files, exiting.")
    sys.exit()
if not sl_files:
    print("Selected Strength Level markdown directory does not contain .md files, exiting.")
    sys.exit()

with tqdm(total=len(garmin_files), desc="Combining markdown files") as pbar:
    for garmin_file in garmin_files:
        # Use Garmin markdown file as basis (including frontmatter if available)
        with open(garmin_md_path + "/" + garmin_file, 'r', encoding="utf-8") as f:
            garmin_content_string = f.read()

        # Check activity type
        activity_type = re.compile("Activity type: (.*)\n").search(garmin_content_string).group(1)

        if activity_type == "Strength Training":
            # Add SL content if available
            date = garmin_file.split("_")[0]
            sl_file = f"Strength_Level_Workout_{date}.md"
            if sl_file in sl_files:
                with open(sl_md_path + "/" + sl_file, 'r', encoding="utf-8") as f:
                    sl_content_string = f.read()
                
                sl_content_string = re.sub("---\n(.*\n)*---\n\n.*\n", "", sl_content_string)
                content_string = garmin_content_string + "\n" + sl_content_string
            else:
                content_string = garmin_content_string
        else:
            content_string = garmin_content_string
            
        with open(f"{output_dir}{"/" if output_dir[-1] != "/" else ""}{garmin_file}", "w", encoding="utf-8") as md_file:
            md_file.write(content_string)

        pbar.update(1)
