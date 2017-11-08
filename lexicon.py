import basic_features as bf

lexicon = {

    'basic_features': bf.basic_features,

    'necessity_modals': [['must'], ['should'], ['had', 'better'], ["'d", 'better'], ['better'], ['have', 'to'],
                                 ['need', 'to'], ['ought', 'to'], ["'s", 'got', 'to'], ["'ve", 'got', 'to'],
                                 ['have', 'got', 'to'], ['be', 'supposed', 'to'], ["'m", 'supposed', 'to'],
                                 ['am', 'supposed', 'to'], ['is', 'supposed', 'to'], ["'s", 'supposed', 'to'],
                                 ['are', 'supposed', 'to'], ["'re", 'supposed', 'to'], ['was', 'supposed', 'to'],
                                 ['were', 'supposed', 'to'], ['being', 'supposed', 'to']],

    # Passive post-nominal modifiers
    # Types below come from Longman Corpus
    'vwbn': {

        # suasive
        'vsua': {'drawn', 'ordained', 'undertook', 'granted', 'ordered', 'resolved', 'resulted', 'requested',
                 'recommended', 'advocated', 'reminded', 'conceded', 'urged', 'proposed', 'persuaded', 'enjoined',
                 'demanded', 'provided', 'intended', 'argued', 'arranged', 'desired', 'advanced'},

        # public
        'vpub': {'emphasized', 'signalled', 'misled', 'answered', 'remarked', 'shouted', 'questioned', 'explained',
                    'reported', 'announced', 'said', 'contended', 'confirmed', 'displayed', 'declared', 'told', 'hinted',
                   'expressed', 'insisted', 'acknowledged', 'stated', 'boasted', 'swore', 'assured', 'admitted',
                   'maintained', 'informed', 'bought', 'charged', 'recorded', 'alleged', 'emphasised', 'claimed',
                   'drafted', 'guaranteed', 'protested', 'intimated', 'added', 'testified', 'suggested', 'denied',
                   'telephoned', 'honoured', 'pleaded', 'mentioned', 'advised', 'replied', 'predicted', 'objected',
                   'submitted', 'complained', 'promised', 'asked', 'stressed', 'asserted', 'warned', 'agreed'},

        # private
        'vprv': {'presupposed', 'realized', 'learnt', 'hoped', 'confessed', 'imagined', 'recalled', 'noted',
                    'supposed', 'used', 'demonstrated', 'presumed', 'proven', 'accepted', 'saw', 'concerned',
                    'forgotten', 'thought', 'read', 'estimated', 'reflected', 'appreciated', 'perceived', 'observed',
                    'determined', 'decided', 'established', 'known', 'preferred', 'assumed', 'believed', 'realised',
                    'noticed', 'reasoned', 'considered', 'concluded', 'remembered', 'proved', 'sensed', 'held', 'shown',
                    'learned', 'grasped', 'found', 'anticipated', 'expected', 'felt', 'revealed', 'wrote', 'discovered',
                    'showed', 'heard', 'recognized', 'recognised', 'forgot', 'suspected', 'feared', 'calculated', 'seen',
                    'pretended', 'indicated', 'defined', 'knew', 'wished', 'meant', 'reached', 'implied', 'persisted',
                    'understood', 'prayed', 'ensured', 'doubted', 'worried', 'succeeded', 'reckoned', 'judged',
                    'followed'},


    }

}