<div style="text-align:center">
    <p align="center">
        <img src="https://img.icons8.com/nolan/100/000000/book-shelf.png">
    </p>

# Octane
A Client-Side Resource Manager written using HTML, CSS, JS, and Python for those who want to finally get some value from their heap of bookmarked/saved resources.

![status-wip](https://img.shields.io/badge/Status-Work%20in%20Progress-red.svg)
</div>

<!-- # <img src="https://img.icons8.com/nolan/100/000000/book-shelf.png" height="100" align="left" /> Octane: Bookmark Manager

![status-wip](https://img.shields.io/badge/Status-Work%20in%20Progress-red.svg) -->

---


#### In Progress Tasks
1. Tree view for showing bookmarks within their folders
2. Adding support for collections
3. Server and Frontend Implementation to interact with the data.
    1. Implement Pre-Building of Search Index using node.js for better client performance.
4. Tags Implementation
5. New Implementation of Search using MiniSearch or FlexSearch


# Dev Installation
To setup this project on your machine for development, clone the repo as usual and follow the following steps to setup your environment.
> Note: This works well for the Bash Shell, found in Linux and MacOS by default and also, the given instructions for installing Python Dependencies are for Anaconda. If you don't have it, try downloading the Python3.x version from [Anaconda's Official Website](https://www.anaconda.com/distribution/) or use any other virtual environment manager that you'd like to use, as it's not recommended to install packages into your system's installation of python...
<!-- conda env create -f environment.yml -->

```sh
    conda create -n yourenvname python=3.7.3
    conda activate yourenvname
    pip install -r requirements.txt
```

**Colorama Download Instructions:** You may face an problem, when installing and using colorama through pip. This requires a manual fix. Download `.tar.gz` package for colorama from https://pypi.python.org/packages/source/c/colorama/colorama-0.3.3.tar.gz, extract it and run the following commands in the terminal.
```sh
    conda activate yourenvname
    cd ~/Downloads/colorama*
    python setup.py install
```

> Note: The above `cd` command (2nd Line) assumes that the path to your extracted folder containing the colorama files is "~/Downloads/colorama*", this assumption might not hold in many cases, hence consider making sure that this path is correct in your case.

For instructions on the Data.World and IFTTT Integration for pulling medium bookmarks in realtime, [read this](docs/DataworldIFTTT.md).



# Concepts used
* [Object-relational mapping](https://stackoverflow.com/a/1152323/7800641) to add flexibility in the data handling.


---
<sup>Icon used: <a href="https://icons8.com/icon/44780/book-shelf">Book Shelf icon by Icons8</a></sup>
