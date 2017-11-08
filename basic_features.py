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

    # PUNCTUATION
    # Still needed: '    "   -   $   %

    ',': ((',', 0),),                       # ,     ,+clp+++
    ';': ((';', 0), ('clp', 1)),            # ;     ;+clp+++
    ':': ((':', 0), ('clp', 1)),            # :     :+clp+++
    '?': (('?', 0), ('clp', 1)),            # ?     ?+clp+++
    '!': (('!', 0), ('clp', 1)),            # !     !+clp+++
    '.': (('.', 0), ('clp', 1)),            # .     .+clp+++
    '(': (('(', 0),),                       # (     (++++
    ')': ((')', 0),),                       # )     )+clp+++

    # PRONOUNS
    # Note that some pronouns with two separate tags in CLAWS might only have one tag in Biber (e.g. i & we)

    'PPIS1': (('ppla', 0), ('pp1', 1)),     # i     ppla+pp1+++ first person subject pronoun + first person pronoun
    'PPIS2': (('ppla', 0), ('pp1', 1))      # we    ppla+pp1+++ first person subject pronoun + first person pronoun

}