""""
Command line app for the tagger.

How to use:

1.  Open up the terminal.

2.  Navigate to where this file is located

3.  Enter: python3 claws2biber.py path-to-folder-of-the-claws-corpus folder-name-for-the-new-corpus
    
    For example:    
    python3 claws2biber.py  /home/mike/corpora/Minicore /home/mike/corpora/Minicore-BT

    Use --ext to change the file extensions. .tec is the default, but say you want everything
    to be saved as a .txt file:
    
    python3 claws2biber.py /home/mike/corpora/Minicore /home/mike/corpora/Minicore-BT --ext txt
    
    NOTE: If python3 is not the environmental variable for Python 3 on your computer, then replace
    python3 with either
        (a) whatever the environmental variable for Python 3 is
        (b) the path to python3.exe on your computer
    
    For example: C:\Python35\python.exe claws2biber.py home/mike/corpora/Minicore /home/mike/corpora/Minicore-BT
    
"""
import argparse

from corpus import Corpus

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('folder')
    parser.add_argument('new_folder')
    parser.add_argument('--ext', dest='ext', default='tec', type=str)

    args = parser.parse_args()

    c = Corpus(args.folder)
    c.convert(args.new_folder, ext=args.ext)
