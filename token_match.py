"""
Used to match single words with a tag
"""

token_match = {
        'not':  (('xnot', 0), ('not', 2)),                  # xnot++not++
        "n't":  (('xnot', 0), ('not', 2), ('0', 4)),        # xnot++not++0
        # Should go through tagging methods for passives and perfect before going through lexical_match()
        # 'done': (('xvbn', 0), ('xvbn', 3))                  # past part. w/ indeterminte function xvbn+++xvbn+
    }