"""
Used to match token-tag pairs with a tag.
"""

token_tag_match = {

        ### Determiners ###

        ## possessive determiners ##

        ('her', 'APPGE'): (('pp$', 0), ('pp3', 1)),             # pp$+pp3+++

        ### Modals ###

        # modals that aren't homographs with other POSs are in token_match

        ## Possibility ##
        ('may', 'VM') : (('md', 0), ('pos', 1)),                # md+pos+++
        ('might', 'VM') : (('md', 0), ('pos', 1)),              # md+pos+++
        ('can', 'VM') : (('md', 0), ('pos', 1)),                # md+pos+++


        ## Prediction ##

        ('will', 'VM'): (('md', 0), ('prd', 1)),
        ('wilt', 'VM'): (('md', 0), ('prd', 1)),


}