"""
CLAWS tags that have a one-to-one match with a Biber tag.

Values must be a tuple of 1 to 5 tuples.

Format:

    CLAWS_tag:  ( (biber_tag, biber_tag_index), ...)

NOTE: Define a single-item tuple like this: ((',', 0),) and NOT like this ((',', 0))

Please leave an in-line comment for each tag that 
    (a) gives some indication of what the CLAWS tag represents
    (b) shows what the biber tag will look like as a string
"""

basic_features = {

    ### PUNCTUATION ###
    # todo: CLAWS does not split -, $, and % into tokens but it seems that the biber tagger does. Decide if this is a feature worth preserving.

    ',': ((',', 0),),                       # ,     ,++++
    ';': ((';', 0), ('clp', 1)),            # ;     ;+clp+++
    ':': ((':', 0), ('clp', 1)),            # :     :+clp+++
    '?': (('?', 0), ('clp', 1)),            # ?     ?+clp+++
    '!': (('!', 0), ('clp', 1)),            # !     !+clp+++
    '.': (('.', 0), ('clp', 1)),            # .     .+clp+++
    '(': (('(', 0),),                       # (     (++++
    ')': ((')', 0),),                       # )     )++++
    '"': (('"', 0),),                       # "     "++++
    "'": (("'", 0),),                       # '     '++++
    '-': (('-', 0),),                       # -     -++++

    ### DETERMINERS ###

    'AT': (('ati', 0),),                    #   ati++++ singular definite article {the, no)
    'AT1': (('at', 0),),                    #   at++++  singular indefinite articles
    'DA1': (('ap', 0),),                    #   ap++++  singular post-determiner
    'DA2': (('aps', 0),),                   #   aps++++ plural post-determiner
    'DAR': (('ap', 0),),                    #   ap++++  comparative post-determiner
    'DAT': (('ap', 0),),                    #   ap++++  superlative post-determiner
    'DB': (('abn', 0),),                    #   abn++++ pre-quantifier
    'DB2': (('abx', 0),),                   #   abx++++ pre-quantifier / double conjunction ("both")

    ### PRONOUNS ###
    # Note that some pronouns with two separate tags in CLAWS might only have one tag in Biber (e.g. i & we)
    # todo: add method that adds 0 tag to subject pronouns if they are part of a contraction. Prev. entries for these are commented out.

    ## SUBJECT PRONOUNS ##

    # 'PPIS1': (('pp1a', 0), ('pp1', 1)),     # i         pp1a+pp1+++  first person subject pronoun + first person pronoun
    # 'PPHS1': (('pp3a', 0), ('pp3', 1)),     # he, she   pp3a+pp3+++  third person subject pronoun + third person personal pronoun

    #'PPIS2': (('pp1a', 0), ('pp1', 1)),     # we        pp1a+pp1+++ first person subject pronoun + first person pronoun
    # 'PPHS2': (('pp3a', 0), ('pp3', 1)),     # they      pp3a+pp3+++ singular third person subject pronoun + third person personal pronoun

    ## OBJECT PRONOUNS ##
    'PPIO1': (('pp1o', 0), ('pp1', 1)),     # me       pp1o+pp1+++ singular first person object pronoun
    'PPIO2': (('pp1o', 0), ('pp1', 1)),     # us       pp1o+pp1+++ singular first person object pronoun
    'PPHO1': (('pp3o', 0), ('pp3', 1)),     # him, her pp3o+pp3+++  third person  object pronoun
    'PPHO2': (('pp3o', 0), ('pp3', 1)),     # them     pp3o+pp3+++  third person  object pronoun

    ## YOU AND IT ##
    # Neither Biber nor CLAWS seems to distinguish between subject and object for you and it
    # 'PPH1': (('pp3', 0), ('it', 1)),        # it        pp3+it+++   third person pronoun + third person impersonal pronoun (it)
    #'PPY': (('pp2', 0), ('pp2', 1)),        # you       pp2+pp2+++  second person pronoun + second person pronoun

    ## POSSESSIVE PERSONAL PRONOUNS ##
    'PPGE': (('pp$$', 0),),                  # mine, yours, hers     pp$$++++ possessive personal pronoun

    ## INDEFINITE PRONOUNS ###
    'PN': (('pn', 0),),                      # none                  pn++++ indefinite pronoun
    'PN1': (('pn', 0),),                     # everybody, something  pn++++ indefinite pronoun

    ## REFLEXIVE PRONOUNS ##
    'PNX1': (('ppl1', 0),),                 # oneself               ppl1++++    indefinite reflexive pronoun
    
    ## EXISTENTIAL THERE ##
    'EX': (('ex', 0), ('pex', 1)),          # there     ex+pex+++


    ### NOUNS ###

    ## UNITS OF MEASUREMENT ##
    'NNU1': (('nnu', 0),),                  # singular unit of measurement  nnu++++
    'NNU2': (('nnus', 0),),                 # plural unit of measurement    nnus++++
    'NNU': (('nnu', 0),),                   # singular unit of measurement (neutral for number in CLAWS)    nu++++

    ## LOCATIVE NOUNS ##
    'NNL1': (('npl', 0),),                  # singular locative noun    npl++++
    'NNL2': (('npls', 0),),                 # plural locative noun      npls++++

    ## TITULAR NOUNS ##
    # These do not cover the full range of titular nouns. A lexicon will need to be used.
    # todo: add plural titular nouns
    # todo: find a way to tag singular titular nouns that are not included in the NNB and NNA tags
    'NNB': (('npt', 0),),                   # singular titular noun (preceding noun in CLAWS)   npt+++
    'NNA': (('npt', 0),),                   # plural titular noun (proceeding noun in CLAWS)    npt++++

    ## ADVERBIAL NOUNS ##
    # These do not cover the full range of adverbial nouns. A lexicon will need to be used.
    
    'NPD1': (('nr', 0),),               # adverbial noun (singular day of the week in CLAWS)            nr++++
    'NPD2': (('nrs', 0),),              # plural adverbial noun (plural day of the week in CLAWS)       nrs++++
    'NPM1': (('nr', 0),),               # singular adverbial noun (singular month in CLAWS)             nr++++
    'NPM2': (('nrs', 0),),              # plural adverbial noun (plural month in CLAWS)                 nrs++++
    'ND1': (('nr', 0),),                # singular adverbial noun (singular noun of direction in CLAWS) nr++++


    ### NUMBERS ###

    # todo: create method to distinguish between these. Both are MC2 in CLAWS
    # plural and > 1        cds++++ cardinal plural (tens, hundreds, thousands)
    # plural 1              cd1s++++ cardinal number: ones

    # todo: create method to find dates. There is no CLAWS tag for dates. Further research required.
    # cd+date++ + cardinal number + date (year only)

    # todo: figure out what to do with other claws tags for numbers (below)
    # MCGE	genitive cardinal number, neutral for number (two's, 100's)
    # MCMC	hyphenated number (40-50, 1770-1827)
    # MF	fraction,neutral for number (e.g. quarters, two-thirds)

    'MC1': (('cd1', 0),),                   # singular 1            cd1++++ cardinal number: I, one
    'MC': (('cd', 0),),                     # singular and > 1      cd++++ cardinal number (2, 3, 4, two, three, four, hundred, ...)
    'MD': (('od', 0),),                     # ordinal               od++++ ordinal number Ost, 2nd, first, second, ...)

    'NNO': (('cd1', 0),),                   # cardinal number (numeral noun neutral for number in CLAWS)    cd++++
    #NNO2 does not cover the full range of plural cardinal numbers.
    'NNO2': (('cds', 0),),                   # plural cardinal number (plural numeral noun in CLAWS)         cd+++

    'ZZ1': (('zz', 0),),                    # singular letter of the alphabet   zz++++
    'ZZ2': (('zz', 0),),                    # plural letter of the alphabet     zz++++

    ### PREPOSITIONS ###
    'TO': (('to', 0),),                     # infinitive marker     to++++

    ### SUBORDINATORS ###

    'CSA': (('cs', 0),),                    # as as a subordinator/conjunction      cs++++
    'CST': (('cs', 0),),                    # that as a subordinator/conjunction    cs++++
    'CSN': (('cs', 0),),                    # than as a subordinator/conjunction    cs++++
    'CSW': (('cs', 0), ('who', 1)),         # whether as a subordinator/conjunction cs+who+++


    ### MISCELLANEOUS ###

    'FW': (('&fw', 0),),                    # foreign word  &fw++++
    'GE': (('$', 0),),                      # genitive s    $++++
    'UH': (('uh', 0),),                     # interjection  uh++++



}