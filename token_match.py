"""
Used to match single words with a tag
"""

token_match = {
        'not':  (('xnot', 0), ('not', 2)),                  # xnot++not++
        "n't":  (('xnot', 0), ('not', 2), ('0', 4)),        # xnot++not++0
        # Should go through tagging methods for passives and perfect before going through lexical_match()
        # 'done': (('xvbn', 0), ('xvbn', 3))                  # past part. w/ indeterminte function xvbn+++xvbn+

        ### modals ###

        'would': (('md', 0), ('prd', 1)),                   # md+prd+++
        'shall': (('md', 0), ('prd', 1)),                   # md+prd+++
        "'ll": (('md', 0), ('prd', 1), ('0', 4)),           # md+prd+++
        "'d": (('md', 0), ('prd', 1), ('0', 4)),           # md+prd+++

        'cannot': (('md', 0), ('pos', 1)),                  # md+pos+++
        'could': (('md', 0), ('pos', 1)),                   # md+pos+++
    }