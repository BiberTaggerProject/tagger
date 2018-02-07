from itertools import chain
from re import split
from collections import defaultdict
from basic_features import basic_features as bf

from errors import TextError


class Text:
    """
    Reads and annotates CLAWS tagged texts

     Arguments:
            filepath: path to CLAWS tagged text
    Keyword arguments:
        register: register of the text
        encoding: encoding of the file located at filepath
        open_errors: value of ignore kwarg of of open() when filepath is opened
        lowercase: if True, words in sents will be lowercase
    """
    # regexp pattern used for sentence tokenization
    # Could probably be improved so that `if s.strip()` does not have to be used in self.sents comprehension
    sentence_delimiter = '\n?</?s>\n?'
    # regexp pattern used to separate words from tags.
    # Uses negative and positive lookbehind to catch _ while omitting patterns like _________
    word_tag_delimiter = '_'

    # Passed by default as **kwargs to the methods called in self.parse
    parser_config = {
        'phrasal_verb_range': 4,
        'passive_range': 4
    }

    lexicon = {
        'basic_features': bf,
        'necessity_modals': [['must'], ['should'], ['had', 'better'], ["'d", 'better'], ['better'], ['have', 'to'],
                             ['need', 'to'], ['ought', 'to'], ["'s", 'got', 'to'], ["'ve", 'got', 'to'],
                             ['have', 'got', 'to'], ['be', 'supposed', 'to'], ["'m", 'supposed', 'to'],
                             ['am', 'supposed', 'to'], ['is', 'supposed', 'to'], ["'s", 'supposed', 'to'],
                             ['are', 'supposed', 'to'], ["'re", 'supposed', 'to'], ['was', 'supposed', 'to'],
                             ['were', 'supposed', 'to'], ['being', 'supposed', 'to'], ['has', 'got', 'to'],
                             ['been', 'supposed', 'to'], ['be', 'to'], ['is', 'to'], ["'s", 'to'], ['am', 'to'],
                             ["'m", 'to'], ['are', 'to'], ["'re", 'to'], ['was', 'to'], ['were', 'to'], ['been', 'to'],
                             ['being', 'to']],
        'possibility_modals': [['can'], ['could'], ['may'], ['might'],['is', 'able', 'to'], ["'s", 'able', 'to'],
                               ['am', 'able', 'to'], ["'m", 'able', 'to'], ['be', 'able', 'to'], ['are', 'able', 'to'],
                               ["'re", 'able', 'to'], ['was', 'able', 'to'], ['were', 'able', 'to'], ['is', 'able', 'to'],
                               ["being", 'able', 'to'], ['been', 'able', 'to'], ['be', 'permitted', 'to'],
                               ['is', 'permitted', 'to'], ["'s", 'permitted', 'to'], ['am', 'permitted', 'to'],
                               ["'m", 'permitted', 'to'], ['are', 'permitted', 'to'], ["'re", 'permitted', 'to'],
                               ['was', 'permitted', 'to'], ['were', 'permitted', 'to'], ['been', 'permitted', 'to'],
                               ['being', 'permitted', 'to'], ['be', 'allowed', 'to'], ['is', 'allowed', 'to'],
                               ["'s", 'allowed', 'to'], ['am', 'allowed', 'to'], ["'m", 'allowed', 'to'],
                               ['are', 'allowed', 'to'], ["'re", 'allowed', 'to'], ['was', 'allowed', 'to'],
                               ['were', 'allowed', 'to'], ['been', 'allowed', 'to'], ['being', 'allowed', 'to']],
        'prediction_modals': [['will'], ['would'], ['shall'], ['sha'], ['wo'], ['is', 'going', 'to'], ["'s", 'going', 'to'],
                              ['are', 'going', 'to'], ["'re", 'going', 'to'], ['am', 'going', 'to'],
                              ["'m", 'going', 'to'], ['be', 'going', 'to'], ['was', 'going', 'to'],
                              ['were', 'going', 'to'], ['been', 'going', 'to'], ['be', 'about' 'to'], ['am', 'about', 'to'],
                              ['are', 'about', 'to'], ['is', 'about', 'to'], ["'m", 'about', 'to'], ["'s", 'about', 'to'],
                              ["'re", 'about', 'to'], ['being', 'about', 'to'], ['was', 'about', 'to'],
                              ['were', 'about', 'to'], ['being', 'about', 'to']
                                                                                                            ]
    }

    def __init__(self, filepath, register='written', encoding='UTF-8', open_errors='ignore', lowercase=False):
        self.parsers = [self.passives, self.proper_nouns, self.basic_features, self.modal_types]
        self.register = register
        self.filepath = filepath

        with open(filepath, encoding=encoding, errors=open_errors) as f:
            self.text = f.read()

        # makes self.text into a list of sentences
        # sentences are tuples of lists of word-tag pairs
        if lowercase:
            self.sents = tuple(
                tuple(['_'.join(element.split(self.word_tag_delimiter)[:-1]).lower(),
                       element.split(self.word_tag_delimiter)[-1]]
                      for element in s.strip().split())
                for s in split(self.sentence_delimiter, self.text) if s.strip()
            )
        else:
            self.sents = tuple(
                tuple(['_'.join(element.split(self.word_tag_delimiter)[:-1]),
                       element.split(self.word_tag_delimiter)[-1]]
                      for element in s.strip().split())
                for s in split(self.sentence_delimiter, self.text) if s.strip()
            )

    def tokens(self):
        """Returns a list of lists of tagged tokens without sentence boundaries."""
        return tuple(chain(*self.sents))

    def freq_dist(self, element_i=1, formatting_func=None):
        """Returns a dictionary of word or tag frequencies. Returns tags by default.

        Keyword arguments:
            element_i: Index of the tag-token pair used in the frequency distribution.
            Set to 0 for tokens, 1 for tags, or None or False for (token, tag)
            formatting_func: a function used on each item in the frequency distribution. Set to a non-true value if
            no function is wanted (e.g. None, False)

        Examples:
            Frequency distribution of lowercase tokens:
            >>> t = Text('some_file.cls')
            >>> t.freq_dist(0, str.lower)
            Frequency distribution of (token, tag) tuples.
            >>> t = Text('some_file.cls')
            >>> t.freq_dist(None)
        """
        fd = defaultdict(int)

        for element in self.tokens():
            # determines what the keys in the frequency distribution dictionary are
            if type(element_i) == int:
                element = element[element_i]
            elif element_i is None or element_i is False:
                element = tuple(element)

            # makes the frequency distribution
            if formatting_func:
                fd[formatting_func(element)] += 1
            else:
                fd[element] += 1

        return fd

    def parse(self):
        """Calls the items in self.parsers on every sentence in self.sents."""

        parsed_sents = []

        for sent in self.sents:
            # Adds list that will contain biber tags to each element in sent
            # If this is done another way, then replace the value of parsed_sent below with copy.deepcopy(sent)
            # Otherwise parsed_sent will be a pointer to sent, even if [:] is used, because of its embedded lists
            parsed_sent = tuple(element + [['', '', '', '', '']] for element in sent)
            for parser in self.parsers:
                parsed_sent = parser(parsed_sent)

                # Raises exception if tags are not in the right format
                ps = [ps for ps in parsed_sent if len(ps) != 3]
                if ps:
                    error_message = 'Sentence returned by {parser_name} has {n} element(s) that do(es) not have 3 items:' \
                                    '\n{sent}'.format(parser_name=parser.__name__, n=len(ps), sent=parsed_sent)

                    raise TextError(error_message)

            parsed_sent = self.make_biber_tag(parsed_sent)
            parsed_sents.append(parsed_sent)

        return parsed_sents

    def make_biber_tag(self, sent):
        """This is a placeholder for now. Will convert tuples of lists to tuples of strings."""
        return sent

    @staticmethod
    def sent_tails(sent, start, tail_length=4, ind=None, entity=None):
        """
        Returns specified number of tokens after an index

        Arguments:
            sent: a sentence from self.sents
            start: the index that the sentence tail starts at

        Keyword Arguments:
            tail_length: the length of the tail. Setting tail length to a negative index will return a tail up until
            that index in a sentence. For example, tail_length=-1 would the rest of a sentence.
            ind: an integer representing the index of subitems in sent. sent=0 returns a list of words and sent=1
            returns a list of tags
            entity: a string that determines the value of ind. Value must be "tags" or "words" for it to do anything.
        """
        if entity and entity.lower() == 'tags':
            ind = 1
        elif entity and entity.lower() == 'words':
            ind = 0

        if ind is not None and ind is not False:
            if 0 > tail_length:
                return [elem[ind] for elem in sent[start + 1:tail_length]]
            else:
                return [elem[ind] for elem in sent[start + 1:start + 1 + tail_length]]
        elif 0 > tail_length:
            return sent[start + 1:tail_length]
        else:
            return sent[start + 1:start + 1 + tail_length]



    def passives(self, sent):
        """
        Appends tags to auxilliary and main verbs in passive verb phrases.
        Gap allowed between auxilliary and main verb determind by parser_config['passive_range']
        """
        for i, (word, tag, biber_tags) in enumerate(sent):

            if tag[:2] == 'VB':
                sent_tail_tags = self.sent_tails(sent,
                                                 i,
                                                 tail_length=self.parser_config['passive_range'],
                                                 entity='tags')

                if 'VVN' in sent_tail_tags:

                    main_verb_i = [i + n + 1 for n, elem in enumerate(sent_tail_tags) if elem == 'VVN']
                    sent_tail_words = self.sent_tails(sent,
                                                      max(main_verb_i),
                                                      tail_length=-1,
                                                      entity='words')

                    for mvi in main_verb_i:

                        if 'by' in sent_tail_words:
                            # vpsv++by+xvbn+    main clause passive verb + + by passive
                            sent[mvi][2][0] = 'vpsv'
                            sent[mvi][2][2] = 'by'
                            sent[mvi][2][3] = 'xvbn'
                        else:
                            # vpsv++agls+xvbn+ main clause passive verb + + agentless passive
                            sent[mvi][2][0] = 'vpsv'
                            sent[mvi][2][2] = 'agls'
                            sent[mvi][2][3] = 'xvbn'
        return sent

    def proper_nouns(self, sent):
        """Adds Biber tags for proper nouns."""
        for i, (word, tag, biber_tags) in enumerate(sent):

            if tag == 'NP' or tag == 'NP1':
                # Sets the first item in the biber tag to the singular proper noun tag
                sent[i][2][0] = 'nps'
            elif tag == 'NP2':
                sent[i][2][0] = 'np'

        return sent

    def basic_features(self, sent):
        """
        Adds Biber tags are easy to match with CLAWS tags by finding them in  self.parser_config['basic_features'].

        proper_nouns() should be added to this eventually, but I haven't put it in so that it can serve as a basic
        example of how Text() works.
        """
        for i, (word, tag, biber_tags) in enumerate(sent):
            match = self.lexicon['basic_features'].get(tag, False)

            if match:
                for biber_tag, ind in match:
                    sent[i][2][ind] = biber_tag

        return sent

    # modals of necessity
    def modal_types(self, sent):
        # divides sentences into bigrams
        sent_bigrams = [[w.lower(), sent[i + 1][0].lower()] for i, (w, t, bt) in enumerate(sent) if i < len(sent) - 1]

        for i, (word, tag, biber_tags) in enumerate(sent):
            # checks to see if the modal is in the corresponding lexicon and checks the tags to make sure they are correct
            if ([word.lower()] in self.lexicon['necessity_modals'] and tag == 'VM')\
                    or (word.lower() == 'better' and tag[0:2] == 'VV'):

                # tags the words with biber tags
                sent[i][2][0] = 'VM'
                sent[i][2][2] = 'NEC'

            elif [word.lower()] in self.lexicon['possibility_modals'] and tag == 'VM':

                sent[i][2][0] = 'VM'
                sent[i][2][2] = 'POS'

            elif [word.lower()] in self.lexicon['prediction_modals'] and tag == 'VM':
                sent[i][2][0] = 'VM'
                sent[i][2][2] = 'PRD'

            else:
                # checks bigrams and finds matches in the lexicon
                for nec_modal in self.lexicon['necessity_modals']:
                    if (len(nec_modal) > 2 and nec_modal[0] == word.lower() and nec_modal[1:] in sent_bigrams[i + 1:i + 3]) \
                        or (i < len(sent) - 1 and len(nec_modal) == 2 and nec_modal[0] == word.lower() and
                        nec_modal[1] == sent[i + 1][0].lower() and (sent[i + 1][1] == 'TO')):
                        print(sent[i + 1])
                        print("3")
                        print(sent[i + 1][1])
                        print("4")

                        # tags the words with biber tags
                        for n in range(len(nec_modal)):
                            # Adds the VM++NEC+MULTI+ tag to all words in a multi-word modal
                            sent[i + n][2][0] = 'VM'
                            sent[i + n][2][1] = 'NEC'
                            sent[i + n][2][4] = 'MULTI'

                for pos_modal in self.lexicon['possibility_modals']:
                    if (len(pos_modal) > 2 and pos_modal[0] == word.lower() and pos_modal[1:] in sent_bigrams[i + 1:i + 3]) \
                        or (i < len(sent) - 1 and len(pos_modal) == 2 and pos_modal[0] == word.lower() and
                                        pos_modal[1] == sent[i + 1][0].lower()):

                        for n in range(len(pos_modal)):
                            # Adds the md+nec+++ tag to all words in a multi-word modal
                            sent[i + n][2][0] = 'VM'
                            sent[i + n][2][1] = 'POS'
                            sent[i + n][2][4] = 'MULTI'

                for prd_modal in self.lexicon['prediction_modals']:
                    if (len(prd_modal) > 2 and prd_modal[0] == word.lower() and prd_modal[1:] in sent_bigrams[i + 1:i + 3]) \
                        or (i < len(sent) - 1 and len(prd_modal) == 2 and prd_modal[0] == word.lower() and
                                        prd_modal[1] == sent[i + 1][0].lower()):

                        for n in range(len(prd_modal)):
                            # Adds the md+prd+++ tag to all words in a multi-word modal
                            sent[i + n][2][0] = 'VM'
                            sent[i + n][2][1] = 'PRD'
                            sent[i + n][2][4] = 'MULTI'

        return sent



    def write(self, file_name, header='', encoding='UTF-8', errors='ignore', keep_claws=True):
        """
        Saves text with Biber Tags added as a file. Items without Biber tags will have ++++ as a tag.

        Arguments:
            file_name: filename of the new file
        Keyword arguments:
            header: string inserted at beginning of the saved file
            encoding: character encoding of the saved file
            errors: how encoding errors are handled when writing the file
            keep_claws: retains claws tag if True

            Example line of output when keep_claws is False:

            structured ^vpsv++agls+xvbn+

            Example line of output when keep_claws is True:

            structured ^vpsv++agls+xvbn+ ^VVN
        """
        parsed_text = self.parse()

        if keep_claws:
            line = '{0}^{1}^{2}'
            parsed_text = '\n'.join(
                line.format(word, '+'.join(biber_tag), tag) for word, tag, biber_tag in chain(*parsed_text))
        else:
            line = '{0}^{1}'
            parsed_text = '\n'.join(
                line.format(word, '+'.join(biber_tag)) for word, tag, biber_tag in chain(*parsed_text))

        if header:
            parsed_text = header + '\n' + parsed_text


        with open(file_name, 'w', encoding=encoding, errors=errors) as f:
            f.write(parsed_text)
