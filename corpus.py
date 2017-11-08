from os import walk, mkdir, path
from time import time

from text import Text


class Corpus:
    """
    Used to manage corpora of CLAWS-tagged texts.
    
    Example:
        >>> c = Corpus('/home/mike/corpora/Mini-CORE_tagd_H')
        >>> c.convert('/home/mike/corpora/Mini-CORE_tagd_H_BTT')
    """

    def __init__(self, folder):

        self.files = []
        self.folder = folder
        self.dirs = []

        for dir_path, dir_names, file_names in walk(folder):
            for fn in file_names:
                self.files.append(path.join(dir_path, fn))
            self.dirs.append(dir_path)

    def convert(self, new_folder, ext='tec', stop_at=None):
        """Converts all CLAWS tagged texts in a directory to Biber tagged texts.
        
        Arguments:
            new_folder: Path to the new folder. New folder and subdirectories matching self.folder will be made if 
            they do not already exist.
        
        Keyword arguments:
            ext: File extension for new files.
            stop_at: maximum number of files to convert
        """
        t = time()
        self.copy_dir_tree(new_folder)

        for i, file_name in enumerate(self.files):
            text = Text(file_name)
            file_name = path.join(new_folder, file_name[len(self.folder) + 1:-3] + ext)
            text.write(file_name)

            if i == stop_at:
                break

        print('Converted', len(self.files), 'texts in', time() - t, 'seconds')

    def copy_dir_tree(self, new_folder):
        """Makes new folder containing subfolders structured in the same way as the self.folder"""
        for d in self.dirs:
            d = new_folder + d[len(self.folder):]
            if not path.exists(d):
                mkdir(d)

    def find(self, word, tag, lowercase=True, max_matches=None):
        """
        Finds a matching word, tag or word-tag list in the Corpus.
        
        Arguments:
            word: a string representing a word; set to non-True value to omit from search
            tag: a string representing a tag; set to non-True value to omit from search
            
        Keyword arguments:
            lowercase: determines case sensitivity for matching words; set to True to ignore case
            max_matches: number of results returned; set to non-True value to have no maximum limit
        """
        matches = []

        for file_name in self.files:
            text = Text(file_name, lowercase=lowercase)

            for sent in text.sents:
                if word and tag and [word, tag] in sent:
                    matches.append(sent)
                elif word and word in set(word for word, tag in sent):
                    matches.append(sent)
                elif tag and tag in set(tag for word, tag in sent):
                    matches.append(sent)

                if max_matches and len(matches) == max_matches:
                    break

        return matches