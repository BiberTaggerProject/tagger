from itertools import chain
from re import split
from collections import defaultdict

import lexicon as lx
import claws_replacements as cr
import tag_match as tagm
import token_match as tokm
import token_tag_match as toktagm
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

    # dicts with lexical and tag information used in methods
    lexicon_dict = lx.lexicon
    token_match_dict = tokm.token_match
    tag_match_dict = tagm.tag_match
    token_tag_match_dict = toktagm.token_tag_match
    claws_replacements_dict = cr.replacements

    def __init__(self, filepath, register='written', encoding='UTF-8', open_errors='ignore', lowercase=False):

        # The methods in this list will be applied to every sentence in the text when Text().parse() is called.
        self.parsers = [self.replace_in_claws,
                        self.phrasal_verbs,
                        self.passives,
                        self.proper_nouns,
                        self.modal_nec,
                        self.basic_matcher]

        # register is not used for anything yet
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
                    error_message = 'Sentence returned by {parser_name} has {n} element(s) that do(es) not have 3 items:'\
                        '\n{sent}'.format(parser_name=parser.__name__, n=len(ps), sent=parsed_sent)

                    raise TextError(error_message)

            parsed_sents.append(parsed_sent)

        return parsed_sents

    @staticmethod
    def sent_tails(sent, start, tail_length=4, ind=None, entity=None):
        """
        Returns specified number of tokens after an index
        
        Arguments:
            sent: a sentence from self.sents
            start: the index that the sentence tail starts at
        
        Keyword Arguments:
            tail_length: the length of the tail. Setting tail length to a negative index will return a tail up until
            that index in a sentence. For example, tail_length=-1 would return up to but not including -1
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

    def phrasal_verbs(self, sent):
        """
        Appends tags to the main verb and particle in phrasal verbs. 
        Gap allowed between verb and particle determined by  parser_config['phrasal_verb_range']
        """
        for i, (word, tag, biber_tags) in enumerate(sent):

            if i + 1 < len(sent) and tag[0] == 'V':
                sent_tail_tags = self.sent_tails(sent,
                                                 i,
                                                 tail_length=self.parser_config['phrasal_verb_range'],
                                                 entity='tags')

                if 'RP' in sent_tail_tags:
                    # Ensures that tags are not added
                    # if there is another verb between the current verb and the particle 'RP'
                    if [tg for tg in sent_tail_tags[:sent_tail_tags.index('RP')] if tg[0] == 'V']:
                        continue

                    particle_i = [n for n, elem in enumerate(sent_tail_tags) if elem == 'RP'][0]
                    sent[i + particle_i + 1][2][0] = 'rb'
                    sent[i + particle_i + 1][2][1] = 'phrv'

        return sent

    def passives(self, sent):
        """Appends tags to auxilliary and main verbs in passive verb phrases. Gap allowed between auxilliary and main 
        verb determind by parser_config['passive_range']"""

        #todo account for VDN (done) and VHN (had) tags

        existential_there_ind = None


        for i, (word, tag, biber_tags) in enumerate(sent):

            # the presence of existential there is used later to distinguish between a passive yes/no question and
            # a passive post-nominal modifier
            if tag == "EX":
                existential_there_ind = i

            # Finds be-verb
            if tag[:2] == 'VB' or word.lower() in ['get', 'gets', 'got', 'gotten']:
                sent_tail_tags = self.sent_tails(sent,
                                                 i,
                                                 tail_length=self.parser_config['passive_range'],
                                                 entity='tags')

                # Finds last participle coming after be-verb
                if 'VVN' in sent_tail_tags:

                    main_verb_i = [i + n + 1 for n, elem in enumerate(sent_tail_tags) if elem == 'VVN']

                    sent_tail_words = self.sent_tails(sent,
                                                      max(main_verb_i),
                                                      tail_length=len(sent) - max(main_verb_i),
                                                      entity='words')
                    post_nominal_modifier = False

                    #first two characters in tags between auxilliary verb and first main verb
                    aux_mv_gap_tags = [tag[:2] for  word, tag, bt in sent[i + 1:main_verb_i[0]]]

                    # If this evaluates to True, then it means there are no words between the aux. verb and main verb
                    # Ruling out the possibility of a post-nominal modifier
                    if not aux_mv_gap_tags:
                        pass

                    # matches post-nominal modifier -- tags added in for-loop below in case there are multiple main verbs
                    elif len(aux_mv_gap_tags[-1]) > 1 and aux_mv_gap_tags[-1][0] == 'N':
                        # PROBLEM: It is difficult to distinguish between (a) a post-nominal modifier in a question
                        # and (b) a question in passive voice.
                        #
                        # Some type of statistical solution will probably need to replace this part in the future.
                        # Maybe conditional probability using word frequencies of main verbs?
                        # For now, the only rule I can figure is that it will be a PNM after existential there
                        #
                        # I don't think that distinguishing between a passive question and a post-nominal modifier
                        # within an active-voice question can be determined using rules.


                            if '?' in sent_tail_words:
                                # tags as vwbn... if existential there is within eight tokens to the left
                                if existential_there_ind is not None and 8 > max(main_verb_i) - existential_there_ind:
                                    post_nominal_modifier = True

                                # tags as vpsv if there are coordinated main verbs
                                elif len(main_verb_i) > 1:
                                    pass

                                # tags as vwbn if the main verb is in a set of words from Longman that occur more frequently
                                # as vwbn than as vpsv
                                elif sent[main_verb_i[0]][0].lower() in self.lexicon_dict['vwbn_gt_vpsv']:
                                    post_nominal_modifier = True

                            else:
                                post_nominal_modifier = True

                    # Excludes because match is perfect aspect
                    elif 'VH' in aux_mv_gap_tags :
                        if 'VB' not in aux_mv_gap_tags:
                            continue
                        # Excludes because match is perfect aspect after a cleft e.g. what's happened is that we've now seen...
                        elif aux_mv_gap_tags.index('VB') < aux_mv_gap_tags.index('VH'):
                            continue


                    # Adds tags to main verbs (ahead of current index in sent)
                    for mvi in main_verb_i:

                        if post_nominal_modifier:
                            # vwbn+++xvbn+      passive postnominal modifier + + + past participle form
                            # Shouldn't these be able to have a by or agls tag too?
                            sent[mvi][2][0] = 'vwbn'
                            sent[mvi][2][3] = 'xvbn'

                            if 'that' not in [w.lower() for w, t, bt in sent[i:mvi]]:
                                sent[mvi][2][2] = 'tht0'

                            # assigns additional tag if main verb is in 1 of 3 semantic domains of PNMs
                            # public, private, or suasive
                            for semantic_domain in self.lexicon_dict['vwbn']:
                                if sent[mvi][0].lower() in self.lexicon_dict['vwbn'][semantic_domain]:
                                    sent[mvi][2][1] = semantic_domain
                                    break


                        elif 'by' in sent_tail_words:
                            # vpsv++by+xvbn+    main clause passive verb + + by passive
                            sent[mvi][2][0] = 'vpsv'
                            sent[mvi][2][2] = 'by'
                            sent[mvi][2][3] = 'xvbn'

                            # Adds tags to aux. verb (current index in sent)
                            sent[i][2] = self.be_aux_tag(word)


                        else:
                            # vpsv++agls+xvbn+  main clause passive verb + + agentless passive
                            sent[mvi][2][0] = 'vpsv'
                            sent[mvi][2][2] = 'agls'
                            sent[mvi][2][3] = 'xvbn'

                            # Adds tags to aux. verb (current index in sent)
                            sent[i][2] = self.be_aux_tag(word)


            # Checks for passive post-nominal modifiers after nouns that do not already have a BT added
            # VVD will sometimes be tagged as VVN in CLAWS and mess this up.
            elif tag[0] == 'N' \
                and not [bt for w, t, bt in sent[i+1:i+self.parser_config['passive_range']] if bt[0] in ['vpsv', 'vwbn']]:

                sent_tail_tags = self.sent_tails(sent,
                                                 i,
                                                 tail_length=self.parser_config['passive_range'],
                                                 entity='tags')

                banned_tags = 'N', 'V'

                if 'VVN' in sent_tail_tags and  not [t[0] for t in sent_tail_tags if t[0] in banned_tags and t != 'VVN']:
                    main_verb_i = [i + n + 1 for n, elem in enumerate(sent_tail_tags) if elem == 'VVN']


                    for mvi in main_verb_i:
                        # vwbn+++xvbn+      passive postnominal modifier + + + past participle form
                        # Shouldn't these be able to have a by or agls tag too?
                        sent[mvi][2][0] = 'vwbn'
                        sent[mvi][2][3] = 'xvbn'

                        if 'that' not in [w.lower() for w,t,bt in sent[i:mvi]]:
                            sent[mvi][2][2] = 'tht0'

                        # assigns additional tag if main verb is in 1 of 3 semantic domains of PNMs
                        # public, private, or suasive
                        for semantic_domain in self.lexicon_dict['vwbn']:
                            if sent[mvi][0].lower() in self.lexicon_dict['vwbn'][semantic_domain]:
                                sent[mvi][2][1] = semantic_domain
                                break


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


    def basic_matcher(self, sent):
        """
        Assigns a biber tag based on CLAWS tag. Matches are based on keys and values in self.tag_match_dict.
        
        proper_nouns() should be added to this eventually, but I haven't put it in so that it can serve as a basic
        example of how Text() works.
        """
        for i, (word, tag, biber_tag) in enumerate(sent):

            # only matches if there is not already a biber tag for the word
            if not [b for b in biber_tag if b]:
                tag_val = self.tag_match_dict.get(tag, False)

                if tag_val:
                    for bt, ind in tag_val:
                        sent[i][2][ind] = bt
                    continue

                token_val = self.token_match_dict.get(word.lower(), False)

                if token_val:
                    for bt, ind in token_val:
                        sent[i][2][ind] = bt
                    continue

                token_tag_val = self.token_tag_match_dict.get((word.lower(), tag), False)

                if token_tag_val:
                    for bt, ind in token_tag_val:
                        sent[i][2][ind] = bt
                        print(sent[i])

        return sent

    def modal_nec(self, sent):

        sent_bigrams = [[w.lower(), sent[i+1][0].lower()] for i, (w, t, bt) in enumerate(sent) if i < len(sent) - 1]

        for i, (word, tag, biber_tags) in enumerate(sent):

            if ([word.lower()] in self.lexicon_dict['necessity_modals'] and tag[0] == 'VM') \
                    or (word.lower() == 'better' and tag[0:2] =='VV'):
                sent[i][2][0] = 'md'
                sent[i][2][1] = 'nec'

            else:
                for nec_modal in self.lexicon_dict['necessity_modals']:
                    if (len(nec_modal) > 2 and nec_modal[0] == word.lower() and nec_modal[1:] in sent_bigrams[i+1:i+3])\
                        or (i < len(sent) - 1 and len(nec_modal) == 2 and nec_modal[0] == word.lower() and nec_modal[1] == sent[i+1][0].lower()):

                        for n in range(len(nec_modal)):
                            # Adds the md+nec+++ tag to all words in a multi-word modal
                            # NOTE: In Longman, md+nec+++ is only given to the last word, and preceeding words
                            # in the verb are given the md"++pmd"++ tag, but I don't know what this is
                            # also note that contracted forms should have 0 in as the final character in the biber tag
                            # which does not happen here
                            sent[i + n][2][0] = 'md'
                            sent[i + n][2][1] = 'nec'

        return sent

    def replace_in_claws(self, sent):
        """Replaces claws tags based on dictionary key matches in self.claws_replacements."""
        for i, (word, tag, biber_tag) in enumerate(sent):
            sent[i][1] = self.claws_replacements_dict.get(tag, tag)
        return sent

    @staticmethod
    def be_aux_tag(word):
        """
        Returns biber tag corresponding to the token of `to be` as an auxilliary verb. 
        
        Can only be used if it is already known that a verb is an aux verb. Therefore, within Text, this method should
        only be called by the methods tagging for passive voice, perfect aspect, and progressive aspect.
        
        Arguments:
            word: a string representing a token that is already known to be auxilliary `be` 
        """

        biber_tag = ['', '', '', '', '']
        word = word.lower()

        biber_tag[2] = 'aux'

        # PRESENT TENSE

        if word == 'are':
            # vb+ber+aux++      verb + are + auxiliary verb
            biber_tag[0] = 'vb'
            biber_tag[1] = 'ber'

        elif word == "'re":
            # vb+ber+aux++0     verb + are + auxiliary verb + + contracted ('re)
            biber_tag[0] = 'vb'
            biber_tag[1] = 'ber'
            biber_tag[4] = '0'

        elif word == 'is':
            # vbz+bez+aux++     3rd person sg. verb + is + auxiliary verb
            biber_tag[0] = 'vbz'
            biber_tag[1] = 'bez'

        elif word == "'s":
            # vbz+bez+aux++0    3rd person sg. + is + auxiliary verb. + + contracted (IS)
            biber_tag[0] = 'vbz'
            biber_tag[1] = 'bez'
            biber_tag[4] = '0'

        elif word == 'am':
            # vb+bem+aux++      verb + am + auxiliary verb
            biber_tag[0] = 'vb'
            biber_tag[1] = 'bem'

        elif word == "'m":
            # vb+bem+aux++0     verb + am + auxiliary verb + + contracted ('m)
            biber_tag[0] = 'vb'
            biber_tag[1] = 'bem'
            biber_tag[4] = '0'

        # PAST TENSE

        elif word == 'was':
            # vbd+bedz+aux++    past tense verb + was + auxiliary verb
            biber_tag[0] = 'vbd'
            biber_tag[1] = 'bedz'

        # BASE FORM

        elif word == 'be':
            # vb+be+aux++      base form of verb + be + auxiliary verb
            biber_tag[0] = 'vb'
            biber_tag[1] = 'be'

        # PERFECT ASPECT

        elif word == 'been':
            # vprf+ben+aux+xvbn+    perfect aspect verb + been + auxiliary verb
            biber_tag[0] = 'vprf'
            biber_tag[1] = 'ben'
            biber_tag[3] = 'xvbn'

        # PROGRESSIVE ASPECT

        elif word == 'being':
            # vbg +beg +aux +xvbg + present progressive verb + being + auxiliary verb
            biber_tag[0] = 'vbg'
            biber_tag[1] = 'bg'
            biber_tag[3] = 'xvbg'

        # IF STRING IS NOT PASSED AS ARGUMENT

        elif type(word) != str:
            raise TextError('Argument of Text.be_aux_tag() must be str.')

        return biber_tag

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
            line = '{0} ^{1} ^{2}'
            parsed_text = '\n'.join(line.format(word, '+'.join(biber_tag), tag) for word, tag, biber_tag in chain(*parsed_text))
        else:
            line = '{0} ^{1}'
            parsed_text = '\n'.join(line.format(word, '+'.join(biber_tag)) for word, tag, biber_tag in chain(*parsed_text))


        if header:
            parsed_text = header + '\n' + parsed_text

        print(file_name)

        with open(file_name, 'w', encoding=encoding, errors=errors) as f:
            f.write(parsed_text)


