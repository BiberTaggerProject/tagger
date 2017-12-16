"""
Used to match single words with a tag
"""

token_match = {

        ### determiners ###

        ## possessive determiners ##

        'my': (('pp$', 0), ('pp1', 1)),                         # pp$+pp1+++
        'your': (('pp$', 0), ('pp2', 1)),                       # pp$+pp2+++
        'our': (('pp$', 0), ('pp2', 1)),                        # pp$+pp2+++
        'its': (('pp$', 0), ('it', 1)),                         # pp$+it+++
        'his': (('pp$', 0), ('pp3', 1)),                        # pp$+pp3+++
        'their': (('pp$', 0), ('pp3', 1)),                      # pp$+pp3+++

        ## other determiners ##

        'either': (('dtx', 0),),                                 # dtx++++


        ### modals ###

        'would': (('md', 0), ('prd', 1)),                       # md+prd+++
        'shall': (('md', 0), ('prd', 1)),                       # md+prd+++
        "'ll": (('md', 0), ('prd', 1), ('0', 4)),               # md+prd+++
        "'d": (('md', 0), ('prd', 1), ('0', 4)),                # md+prd+++

        'cannot': (('md', 0), ('pos', 1)),                      # md+pos+++
        'could': (('md', 0), ('pos', 1)),                       # md+pos+++


        ### not ###

        'not':  (('xnot', 0), ('not', 2)),                  # xnot++not++
        "n't":  (('xnot', 0), ('not', 2), ('0', 4)),        # xnot++not++0



    }