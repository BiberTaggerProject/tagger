from os import walk, mkdir, path
from time import time
from collections import defaultdict

from text import Text
from errors import CorpusError


class Corpus:
    """
    Used to manage corpora of CLAWS-tagged texts.
    
    Example:
        >>> c = Corpus('/home/mike/corpora/Mini-CORE_tagd_H')
        >>> c.convert('/home/mike/corpora/Mini-CORE_tagd_H_BTT')
        
    Arguments:
        folder: Directory containing corpus. Can have one ore more level of subfolders.
        encoding_in: Character set of corpus files e.g. UTF-8, ascii-us
    """


    def __init__(self, folder, encoding_in='UTF-8'):
        self.encoding_in = encoding_in
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
            text = Text(file_name, encoding=self.encoding_in)
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

    def find(self, *token_tags, lowercase=True, whole_sent=False, sent_tail=False, save=False):
        """
        Finds words and ngrams in a CLAWS tagged text.
        
        Arguments:
            token_tags: A tuple or tuples with token-tag pairs. Tuple item values must be str or NoneType.
            
        Keyword Arguments:
            lowercase: Makes the CLAWS tagged text tokens lowercase before comparing them with the token strings in token_tags
            whole_sent: Returns the whole sentence of a match if true or only the matching token_tag pair if False.
        
        Examples:
             >>> c = Corpus('/home/mike/corpora/Mini-CORE_tagd_H')
             Find a 'people' token with the 'NN' tag
             >>> r = c.find(('people', 'NN'))
             Find a 'people' token wih any tag followed by an 'in' token with any tag
             >>> r = c.find(('people', None), ('in', None))
             Find a 'people' token with a 'NN' tag followed by anything followed by any token with a 'VBZ' tag
             >>> r = c.find(('people', 'NN'), (None, None), (None, 'VBZ'))
        """

        matches = []

        if [item for item in token_tags if type(item) != tuple or len(item) != 2]:
            raise CorpusError("Token_tags must be tuples with two items having str or NoneType values")

        for file_name in self.files:
            text = Text(file_name, lowercase=lowercase)

            for sent in text.sents:
                match = []
                ngram_ind = 0

                for i, (word, tag) in enumerate(sent):
                    if lowercase: word = word.lower()

                    # word and tag must both match
                    if token_tags[ngram_ind][0] and token_tags[ngram_ind][1] and token_tags[ngram_ind] == (word, tag):
                        match.append((word,tag))
                        ngram_ind += 1
                    # word matches and no tag included in tuple for this item in token_tags
                    elif token_tags[ngram_ind][0] and token_tags[ngram_ind][1] is None and token_tags[ngram_ind][0] == word:
                        match.append((word, tag))
                        ngram_ind += 1
                    # tag matches and no word included in tuple for this item in token_tags
                    elif token_tags[ngram_ind][1] and token_tags[ngram_ind][0] is None and token_tags[ngram_ind][1] == tag:
                        match.append((word, tag))
                        ngram_ind += 1
                    elif token_tags[ngram_ind] == (None, None):
                        match.append((word, tag))
                        ngram_ind += 1
                    # No match
                    else:
                        match = []
                        ngram_ind = 0

                    # Adds to matches when finished
                    if ngram_ind == len(token_tags):
                        if whole_sent:
                            matches.append((file_name, sent))
                        elif sent_tail:
                            matches.append((file_name, sent[i:]))
                        else:
                            matches.append((file_name, match))

                        ngram_ind = 0
                        match = []
        if save:
            save_as = input('Save as: ')
            output = '\n'.join(' '.join(tok + '_' + tag for tok, tag in line) for fn, line in matches)

            with open(save_as, 'w', encoding='utf-8') as f:
                f.write(output)

        else:
            return matches

    def lex_freq(self, *tags, lowercase=True):
        """
        Makes conditional frequency distribution of words and tags in a claws tagged text with tags as search string.
        """
        freq_dist = {}

        for file_name in self.files:
            text = Text(file_name, lowercase=lowercase)

            for sent in text.sents:
                for word, tag in sent:
                    if tag in tags:
                        if not freq_dist.get(word, False):
                            freq_dist[word] = defaultdict(int)
                        freq_dist[word][tag] += 1

        return freq_dist

    def tag_freq(self, *words, lowercase=True):
        """
        Makes conditional frequency distribution of words and tags in a claws tagged text with words as search string.
        """
        freq_dist = {}

        for file_name in self.files:
            text = Text(file_name, lowercase=lowercase)

            for sent in text.sents:
                for word, tag in sent:
                    if word in words:
                        if not freq_dist.get(word, False):
                            freq_dist[word] = defaultdict(int)
                        freq_dist[word][tag] += 1

        return freq_dist