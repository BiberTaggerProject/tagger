"""
These classes and functions have been used for debugging the tagger.
They are not part of the tagger.
"""

from corpus import Corpus
from text import Text
from collections import defaultdict
import re


class CorpusTester(Corpus):
    """
    Calls parse on every text in a corpus. Useful for debugging a method in Text() using print() inside of the method.

    To use this, add print() into your code, create an instance of CorpusTester(), and call the dry_run() method.
    This way, a bunch of files won't be created every time you want to test something on a lot of files.

    For example:

    >>> from dev_tools import CorpusTester
    >>> c = CorpusTester('/home/mike/corpora/Mini-CORE_tagd_H')
    >>> c.dry_run()
    """

    def dry_run(self):
        for file in self.files:
            t = Text(file)
            a = t.parse()






class BiberCorpus(Corpus):
    nouns = ['nn++++', 'nn+nom+++', 'nvbg+++xvbg+', 'nn+++xvbn+', 'nns++++',
             'nns+nom+++', 'nnu++++', 'np++++', 'nps++++', 'npl++++', 'npt++++', 'npts++++',
             'nr++++', 'nrs++++']

    pronouns = ['ppla+pp1+++', 'ppla+pp1+++', 'pplo+pp1+++', 'pp$+pp1+++', 'ppl+pp1+++',
                'ppls+ppI+++', 'pp2+pp2+++', 'pp$+pp2+++', 'ppl+pp2+++', 'pp3a+pp3+++', 'pp3o+pp3+++',
                'pp3+pp3+++', 'pp$+pp3+++', 'ppl+pp3+++', 'ppls+pp3+++', 'pp3+it+++', 'pp$+it+++',
                'pp$$++++', 'pn"++++', 'pn++++']


    def __init__(self, folder, filter_files=True):
        super().__init__(folder, encoding_in='ascii')

        if filter_files:
            # If using the Longman Corpus, this excludes untagged and old directories
            self.files = [f for f in self.files if 'Old' not in f and 'Tagd' in f]

    def tagset(self, freqs=False):
        """Returns a set of tags in a corpus."""
        all_tags = []

        if freqs:
            freq_dist = defaultdict(int)


        for file in self.files:
            with open(file, encoding=self.encoding_in, errors="ignore") as f:
                text = f.read().splitlines()

            text_tags = []

            for i, line in enumerate(text):
                # Skips metadata
                if not line or line[0] == '{':
                    continue

                line = line.strip().split(' ')
                # Regexp makes this super slow but couldn't think of a better way to exclude tags with unicode decode errors
                if len(line) != 2 or line[1][0] != '^' \
                    or not re.match("^[a-z0-9\.\,\+\-\!\@\#\$\%\^\&\*\(\)\_\[\]\:\;\"\'\<\>\?\`\=]*$", line[1][1:], re.IGNORECASE):
                    continue

                if freqs:
                    freq_dist[line[1][1:]] += 1
                else:
                    text_tags.append(line[1][1:])

            all_tags += text_tags
            all_tags = list(set(all_tags))

        if freqs:
            return freq_dist
        else:
            return set(all_tags)


    def word_list(self, tag):
        """Returns types that have the given tag."""
        matches = self.find(tag, before=0, after=0, printing=False)
        return set(item[0].lower().split()[0] for item in matches)

    def find(self, tag,  encoding_errors='ignore', before=5, after=5, printing=True):
        """
        Searches through Biber tagged texts and prints results with tags matching `tag`

        Example:
            >>> bc = BiberCorpus('/home/mike/corpora/Mini-CORE_tagd_H_BTT')
            >>> bc.find('vpsv++agls+xvbn+')

        Example of output:

            Mini-CORE_tagd_H_BTT/1+SP+IT+NA-SP-SP-SP+NE-IT-IT-IT+NNNN+0474475.tec
            1717

            that ^++++ ^CST
            felt ^++++ ^VVD
            currencies ^++++ ^NN2
            are ^++++ ^VBR
            being ^++++ ^VBG
            debased ^vpsv++agls+xvbn+ ^VVN
            through ^++++ ^II
            those ^++++ ^DD2
            actions ^++++ ^NN2
            . ^.+clp+++ ^.
            I ^ppla+pp1+++ ^PPIS1

        """
        if tag[0] == '^':
            tag = tag[1:]

        results = []

        for file in self.files:
            with open(file, encoding=self.encoding_in, errors=encoding_errors) as f:
                text = f.read().splitlines()

            for i, line in enumerate(text):
                # Skips metadata
                if not line or line[0] == '{':
                    continue

                line = line.split(' ^')

                if len(line) >= 2 and tag == line[1][:len(tag)]:
                    b_ind = i - before

                    if before < 0:
                        b_ind = 0

                    if printing:
                        # Adds filename, index of match, and match with surrounding lines
                        print(file, i, '\n', '\n'.join(text[b_ind:i + 1 + after]), sep='\n',
                              end='\n\n--------------------\n\n')
                    else:
                        results.append(text[b_ind:i + 1 + after])

        if not printing:
            return results

    def tag_freq(self, token, encoding_errors='ignore'):
        """Returns conditional frequency distribution of tag based on token"""
        freq_dist = defaultdict(int)

        for file in self.files:
            with open(file, encoding=self.encoding_in, errors=encoding_errors) as f:
                text = f.read().splitlines()

            for i, line in enumerate(text):
                # Skips metadata
                if not line or line[0] == '{':
                    continue

                line = line.split(' ^')

                # Makes sure there is really a token tag pair
                if len(line) < 2:
                    continue

                w, t = line[0].lower(), line[1].strip()

                if token.lower() == w.lower():
                    freq_dist[t] += 1

        return freq_dist


    def lex_freq(self, *tags, encoding_errors='ignore', partial_tag_keys=False):
        """
        Returns conditional frequency distribution of words based on the beginning of * tags.
        
        Output is a dict of dicts.
        
        >>> bc = BiberCorpus('/home/mike/corpora/Longman Spoken and Written Corpus (FOR GRAMMAR PROJECT USE ONLY!)')
        >>> fd = bc.lex_freq('vwbn', 'vpsv')
        
        Arguments:
            *tags: tags to use in the search
        Keyword Arguments:
            encoding: encoding of input files
        """
        freq_dist = {}
        tags = list(tags)

        # Cleans *tags items
        for i, tag in enumerate(tags):
            if tag[0] == '^':
                tags[i] = tags[1:]


        for file in self.files:
            with open(file, encoding=self.encoding_in, errors=encoding_errors) as f:
                text = f.read().splitlines()

            for i, line in enumerate(text):
                # Skips metadata
                if not line or line[0] == '{':
                    continue

                line = line.split(' ^')

                # Makes sure there is really a token tag pair
                if len(line) < 2:
                    continue

                w, t = line[0].lower(), line[1]

                for tag in tags:
                    if tag == t[:len(tag)]:

                        # Adds tag from arg as key
                        if partial_tag_keys:
                            if not freq_dist.get(w, False):
                                freq_dist[w] = {tg.strip(): 0 for tg in tags}
                            freq_dist[w][tag.strip()] += 1
                        # Adds tag from token-tag dyad as key
                        else:
                            if not freq_dist.get(w, False):
                                freq_dist[w] = {t.strip(): 0}
                            elif not freq_dist[w].get(t.strip(), False):
                                freq_dist[w][t.strip()] = 0

                            freq_dist[w][t.strip()] += 1

        return freq_dist




    def find_in_sent(self, tags, encoding_errors='ignore'):

        for i, tag in enumerate(tags):
            if tag[0] == '^':
                tag[i] = tag[1:]

        results = {tag: [] for tag in tags}
        cur_sent = []
        add_sent = False
        tag_cat = []
        sent_count = 0

        for file in self.files:
            with open(file, encoding=self.encoding_in, errors=encoding_errors) as f:
                text = f.read().splitlines()

            for i, line in enumerate(text):
                # Skips metadata
                if not line or line[0] == '{':
                    continue

                line = line.split(' ^')

                if len(line) < 2:
                    continue

                w, t = line[0], line[1]
                cur_sent.append([w, t])

                if t in tags:
                    add_sent = True
                    tag_cat.append(t)

                if 'clp' in t:
                    if add_sent:

                        for tc in set(tag_cat):
                            results[tc].append(cur_sent)

                    cur_sent = []
                    tag_cat = []
                    add_sent = False
                    sent_count += 1

        results['sent_count'] = sent_count
        return results

    def colloc(self, tags, match_to, within=-4):
        """
        >>> from dev_tools import BiberCorpus
        >>> bc = BiberCorpus('/home/mike/corpora/Longman Spoken and Written Corpus (FOR GRAMMAR PROJECT USE ONLY!)')
        >>> mc = bc.colloc(['vpsv++agls+xvbn+', 'vpsv++by+xvbn+'], bc.nouns + bc.pronouns)
        >>> pnm = bc.colloc(['vwbn+++xvbn+', 'vwbn+vprv++xvbn+', 'vwbn+vpub++xvbn+', 'vwbn+vsua++xvbn+'], bc.nouns + bc.pronouns)
        """
        sents = self.find_in_sent(tags)
        matches = []
        for tag in tags:
            matches += sents[tag]

        results = {tag: [] for tag in tags}

        for sent in matches:
            for i, (word, tag) in enumerate(sent):
                if tag in tags:
                    bound = i + within
                    if 0 > bound:
                        bound = 0
                    if 0 > within:
                        gap = reversed(sent[bound:i])

                    else:
                        if bound > len(sent):
                            bound = len(sent)
                        if i + 1 == len(sent):
                            break
                        else:
                            gap = sent[i + 1:bound]

                    for w, t in gap:
                        if t in match_to:
                            results[tag].append([w, t])
                            break
                    else:
                        results[tag].append(['', ''])

        results['fd'] = {
            'words': defaultdict(int),
            'tags': defaultdict(int)
        }

        for tag in tags:
            for w, t in results[tag]:
                results['fd']['words'][w] += 1
                results['fd']['tags'][t] += 1

        results['fd']['words'] = sorted(((key, results['fd']['words'][key]) for key in results['fd']['words']),
                                        reverse=True,
                                        key=lambda x: x[1])

        results['fd']['tags'] = sorted(((key, results['fd']['tags'][key]) for key in results['fd']['tags']),
                                       reverse=True,
                                       key=lambda x: x[1])

        results['sent_count'] = sents['sent_count']

        return results


def txt_to_list(txt_file):
    "Returns the content of a txt file as a list of lists. Each item in a sublist is a token."
    with open(txt_file) as f:
        lines = f.read().lower().splitlines()

    return [line.strip().split() for line in lines]