# Combine Garmin and Strength Level markdown files

### Introduction

This script allows you to combine the markdown files resulting from [garmintomd](https://github.com/nelisss/garmintomd) and [strengthleveltomd](https://github.com/nelisss/strengthleveltomd) into single markdown files.

### Requirements

- Python 3.8 or higher

### Installation

1. Clone this repository into a directory of your choice

```
cd /path/to/directory
git clone https://github.com/nelisss/garminslcombinemd
```

1. Run install.sh to create a virtual environment with the required python packages installed

```
chmod +x install.sh
./install.sh
```

### Usage

1. Run [garmintomd](https://github.com/nelisss/garmintomd) and [strengthleveltomd](https://github.com/nelisss/strengthleveltomd) individually.
2. Activate the virtual environment

```
source venv/bin/activate
```

1. Run the python script

```
python garminslcombinemd.py [options]
```

The following options are recognized:

| Option                       | Description                                                                                  | Possible values                                                                                      |
|------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| \-h --help                    | Print help.                                                                                  | \-                                                                                                    |
| \-g --garmin-directory        | Path to directory with Garmin markdown files. Default: interactive directory picker.         | Valid path to directory with Garmin markdown files or "interactive" to be prompted with file picker. |
| \-s --strengthlevel-directory | Path to directory with Strength Level markdown files. Default: interactive directory picker. | Valid path to directory with Garmin markdown files or "interactive" to be prompted with file picker. |
| \-d --directory               | Output directory to save .md files to. Default: \<working directory\>/output.                  | Valid path to folder. Can create one folder, but not recursively.                                    |
