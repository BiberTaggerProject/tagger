import basic_features as bf


# Used to match single words with a tag
token_match = {
        'not':  (('xnot', 0), ('not', 2)),                  # xnot++not++
        "n't":  (('xnot', 0), ('not', 2), ('0', 4)),        # xnot++not++0
        # Should go through tagging methods for passives and perfect before going through lexical_match()
        # 'done': (('xvbn', 0), ('xvbn', 3))                  # past part. w/ indeterminte function xvbn+++xvbn+
    }

lexicon = {

    # might be more effient to do matches like this with nested dicts

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

    },

    # Tokens from the Longman Corpus that have the vwbn tag more frequently than the vpsv tag
    # The frequency distribution itself is saved as data/vwbn_vpsv_conditional_freq_dist.json
    # But only cases where vwbn are more frequent are in the set here in order to save processing time
    # In the future, it may be better to use the whole dataset to take a more nuanced approach or tag for uncertainty
    # or to redo the dataset to account for register
    # FYI: data/vwbn_vpsv_conditional_freq_dist.json was produced using the following code:
    # >>> from dev_tools import BiberCorpus
    # >>> bc = BiberCorpus('/home/mike/corpora/Longman Spoken and Written Corpus (FOR GRAMMAR PROJECT USE ONLY!)')
    # >>> fd = bc.lex_freq('vwbn', 'vpsv')

    'vwbn_gt_vpsv': {'blossomed', 'compounded', 'fell', 'became', 'saw', 'snared', 'stilled', 'lipsticked', 'idealised',
                     'sued', 'gaudied', 'dislocated', 'revisited', 'lamented', 'allied', 'went', 'came', 'resigned',
                     'collapsed', 'allotted', 'gave', 'began', 'remained', 'blueprint', 'took', 'amounted', 'consisted',
                     'failed', 'contributed', 'connected', 'incurred', 'rumbled', 'pursued', 'grew', 'lavished',
                     'to"sudden', 'emanated', 'surrendered', 'espoused', 'which"employed', 'ensured', 'wrought', 'sank',
                     'dated', 'portrayed', 'elapsed', 'cited', 'demanded', 'embodied', 'surveyed', 'expended',
                     'delineated', 'differed', 'entailed', 'drew', 'ran', 'lay', 'showed', 'appeared', 'won',
                     'prevailed', 'declined', 'engendered', 'rose', 'arose', 'chose', 'emerged', 'converged', 'enacted',
                     'depended', 'reverted', 'insisted', 'attuned', 'problem/need', 'totaled', 'endeavoured', 'figured',
                     'donated', 'invaded', 'enjoyed', 'sown', 'phased', 'being"wasted', 'induced', 'suffered',
                     'emitted', 'sounded', 'fashioned', 'perturbed', 'momen', 'fled', 'plunged', 'opted', 'deviated',
                     'pared', 'knew', 'resulted', 'trebled', 'deteriorated', 'dwarfed', 'flattened', 'rested',
                     'stained', 'vacated', 'emaciated', 'consecrated', 'accorded', 'overcame', 'tended', 'condoned',
                     'perpetrated', 'disrupt', 'creased', 'buffered', 'regimen', 'spaced', 'existed', 'been',
                     'responded', 'occurred', 'belonged', 'wished', 'tempered', 'bonded', 'roughened', 'shorn',
                     'penned', 'abstained', 'predominated', 'overlaid', 'bore', 'persisted', 'of"hidden', 'seemed',
                     'nought', 'scrambled', 'totalled', 'soared', 'complained', 'averaged', 'partitioned', 'wrote',
                     'ensued', 'testified', 'disagreed', 'instilled', 'replied', 'risen', 'partaken', 'unadapted',
                     'strove', 'lasted', 'underlay', 'retaliated', 'withdrew', 'wed', 'fared', 'of"guilt',
                     'criminology"developed', 'inflicted', 'conferred', 'exerted', 'and"bottomed', 'of"given',
                     'constricted', 'arrsnged', 'morphqqevidenced', 'ceased', 'inhabited', 'constraint', 'nonfronted',
                     'unaccented', 'pierced', 'bordered', 'undivided', 'tabulated', 'slung', 'harvested',
                     'unidentified', 'distilled', 'expreienced', 'comtinued', 'pretreated', 'extrapolated', 'prceded',
                     'coincided', 'fertilized', 'bowed', 'coexisted', 'born/hatched', 'lined', 'plummeted',
                     'originated', 'agglutinated', 'rebound', 'shunt', 'rebled', 'malabsorbed', 'crypt', 'pepsinogen',
                     'flanked', 'irradiated', 'retreated', 'nevalainen', 'resembled', 'polyunsaturated', 'percept',
                     'yielded', 'flourished', 'headmen', 'broadcasted', 'undeclared', 'matured', 'behaved', 'woven',
                     'unredressed', 'vested', 'introjected', 'bruised', 'grappled', 'notified', 'spiked', 'laced',
                     'resided', 'oscillated', 'urobilinogen', 'end.point', 'cached', 'are"rounded', 'climbed',
                     'contended', 'kl,k2,...then', 'ovulated', 'sexed', 'unbanded', 'required/produced', 'overlearned',
                     'floating.point', 'disallowed', 'gated', 'rundown', 'spanned', 'hilt', 'sunt', 'zweien',
                     'einfachen', 'that"crossed', 'sewn', 'arrayed', 'looted', 'flocked', 'opined', 'humped',
                     'means"based', 'wore', 'undertook', 'marketwomen', 'despaired', 'parallelled', 'endpoint',
                     'interacted', 'innvervated', 'lacked', 'unasserted', 'unconsidered', 'ered', 'blasted', 'harden',
                     'flowed', 'for"gifted', 'professed', 'sprang', 'undersown', 'ate', 'is"organised', 'starred',
                     'stemmed', 'coshed', 'dassault', 'camouflaged', 'ensnared', 'bequeathed', 'the"enchanted',
                     'articled', 'have"puzzled', 'versed', 'of"green', 'the"objects"concerned', 'subtended', 'liganded',
                     'equivalenced', 'geometry/simulated', 'resupplemented', 'clay/calcite/silt', 'doped', 'midpoint',
                     'steinkern', 'erupted', 'demarcated', 'infrared', 'jammed', 'unstandardized', 'between', 'shone',
                     'proliferated', 'unhindered', 'prograded', 'chopped', 'surfaced', 'mashed', 'nailed', 'sweetened',
                     'clasped', 'perched', 'airfreighted', 'recurred', 'edged', 'orbitalswhen', 'leaved', 'depolarised',
                     'pattrn', 'hasbeen', 'concentratiown', 'white"point', 'need', 'signified', 'available/produced',
                     'sang', 'undressed', 'ren', 'messed', 'shitted', 'flavoured', 'vixen', 'breaded', 'tangled', 'alt',
                     'corned', 'eagled', 'exploded', 'inbetween', 'crazed', 'swelled', 'shooted', 'threw', 'flew',
                     'huddled', 'draped', 'grilled', 'mangled', 'waylaid', 'unsliced', 'crept', 'sprechen', 'explosed',
                     'catapult', 'sheered', 'snowmen', 'setted', 'sobered', 'shook', 'woke', 'ployed', 'cooped',
                     'fathomed', 'tarted', 'grunt', 'glisten', 'unclothed', 'togged', 'skied', 'blew', 'fern', 'kommen',
                     'subscribed', 'salted', 'pickled', 'pranged', 'legged', 'fabled', 'disassociated', 'aint', 'dared',
                     'parallelized', 'fatheaded', 'personalized', 'tattooed', 'rhapsodised', 'upturn', 'dropdown',
                     'ven', 'cheapened', 'destabilized', 'masted', 'brailled', 'niffed', 'wrinkled', 'toffeenosed',
                     'grinned', 'martialled', 'reconditioned', 'pindown', 'pronged', 'retailed', 'proceded', 'whizzed',
                     'rubbished', 'sharpen', 'parachuted', 'reblocked', 'ondssed', 'hoiked', 'blooded', 'unburnt',
                     'forlled', 'encumbered', 'mailshotted', 'downturn', 'vowed', 'dwelled', 'condoled', 'deputized',
                     'roomed', 'reneged', 'belted', 'underlinen', 'malt', 'genned', 'moussed', 'unelected', 'protested',
                     'sniggered', 'noncommissioned', 'anxietyridden', 'instrumented', 'seafront', 'shod', 'conjured',
                     'reprint', 'enumerated', 'cairn', 'umpteen', 'oozed', 'outvoted', 'clouted', 'tern', 'chiselled',
                     'er..consumed', 'noninvolved', 'kindergarten', 'faceted', 'intern', 'aspired', 'flavored',
                     'disheveled', 'unaspirated', 'creamed', 'copped', 'witted', 'teamed', 'scarfed', 'pummeled',
                     '\tthen', 'flirted', 'madwomen', 'knifed', 'prepped', 'birdseed', 'cept', '\tdifficult', 'riled',
                     'parodied', 'thatsupposed', 'he', 'youthought', "who'd", 'everything...when', 'vanished', 'flaunt',
                     'barbequed', 'agen', 'dialed', 'unglued', 'markdown', 'hugged', 'horsedrawn', 'therewhen',
                     'overfed', 'dolt', 'demoed', 'rayed', 'barricaded', 'i', 'rusted', 'reframed', 'thrived',
                     'greatened', 'smooshed', 'deadlocked', 'riveted', 'barked', 'amped', 'spawned', 'letdown',
                     'bighorn', 'brokered', 'crackdown', 'maneuvered', 'joked', 'memorialized', 'belched', 'boycotted',
                     'donned', 'choreographed', 'chairwomen', 'caved', 'surged', 'emblazoned', 'interred', 'crewmen',
                     'polled', 'nestled', 'drizzled', 'handprint', 'napped', 'clapped', 'dangled', 'retorted',
                     'swooped', 'blanketed', 'quintupled', 'bankrupted', 'huffed', 'bullpen', 'embroidered', 'dwindled',
                     'splendored', 'shredded', 'inched', 'lakefront', 'battled', 'foresaw', 'lobbed', 'dissented',
                     'gusted', 'patrolled', 'skirted', 'slumped', 'ducked', 'lingered', 'militiamen', 'thundered',
                     'preconceived', 'shrank', 'hovered', 'rallied', 'barged', 'muttered', 'pounced', 'shivered',
                     'cushioned', 'flitted', 'panned', 'unpunished', 'retooled', 'signaled', 'triumphed', 'spattered',
                     'maintainted', 'prowled', 'ballyhooed', 'grumbled', 'shined', 'glared', 'flashpoint', 'fluttered',
                     'well-developed', 'refocused', 'whistled', 'excercised', 'wandered', 'gowned', 'refaced', 'tugged',
                     'misdated', 'internreted', 'unconditioned', 'foundered', 'proclalsned', 'grudged', 'hummed',
                     'storeyed', 'pervaded', 'officiated', 'welleducated', 'ovnt', 'dreyen', 'kosheren', 'blanked',
                     'brimmed', 'resubmitted', 'mushroomed', 'betokened', 'conduced', 'intervened', 'forbade',
                     'skidded', 'mogulled', 'untracked', 'unopened', 'wielded', 'pokerfaced', 'carpentered', "'unt",
                     'slaughtred', 'aught', 'isfinished', 'resounded', 'limbed', 'unsmirched', 'citified',
                     'unpressurized', 'khalichen', 'mercerized', 'unapproved', 'unanalysed', 'unrequited', 'mehmed',
                     'carbonized', 'receded', "'.'this", 'cabled', 'acquiesced', 'extern', 'unstoried', 'dreadnought',
                     'capitulated', 'eked', 'ked', 'materialized', 'depoliticised', "'i',rn", 'lrint', 'itemsoften',
                     'workrelated', 'riitered', 'wellanalyzed', 'nucleated', 'swarmed', 'wellinformed', 'well-liked',
                     'brained', 'sconed', 'staunched', 'anglicized', 'unespoused', 'dithered', 'unransomed', 'dunned',
                     'tenanted', 'was.delivered', 'earthborn', 'floured', 'rarefied', 'stagnated', 'frostbelt',
                     'areabased', 'flatted', 'untrodden', 'battlemented', 'windswept', 'clean-bred', 'quantized',
                     'unconcealed', 'petered', 'boomed', 'mesmerised', 'covenanted', 'tarboushed', 'footprint',
                     'yawned', 'caroused', 'skinned', 'trickled', 'squatted', 'crenellated', 'skirmished', 'angled',
                     'nudged', 'cased', 'harrowed', 'columned', 'scurried', 'deadfaced', 'quicken', 'unmeasured',
                     'halated', 'photosensitized', 'berated', 'throated', 'bodied', 'engined', 'emigrated',
                     'strongpoint', 'overtook', 'sufficed', 'jockeyed', 'negatived', 'roundheaded', 'sed', 'unsalted',
                     'chromiumplated', 'unpasteurized', 'ceilinged', 'unfrequented', 'coachmen', 'unformed',
                     'unengendered', 'uncanonized', 'expiated', 'yearned', 'sizzled', 'franchised', 'wellborn',
                     'thiamineenriched', 'wellgreased', 'herbseasoned', 'sauted', 'diced', 'blared', 'sortied', 'sped',
                     'trespassed', 'omened', "'-indeed", 'nodded', 'yearsthen', 'creellt', 'afiiiiyfitnded', 'cantered',
                     'galloped', 'glowed', 'tasselled', 'unleavened', 'verbalized', 'totalized', 'sexlinked',
                     'burnished', 'paled', 'soothed', 'embrowned', 'nightmen', 'timekept', 'beingpilloried', 'spired',
                     'communinscribed', 'shafted', 'greenhorn', 'snugged', 'satiated', 'immeshed', 'unfathomed',
                     'countermarched', 'endeavored', 'undiscovered', "'en", 'uncanned', 'presliced', 'comminuted',
                     'argned', 'quarreled', 'geed', 'tenderharted', 'counterfeited', 'clutched', 'befogged',
                     'syllabled', 'suceed', 'slipt', 'pickmen', 'inriched', 'spoyled', 'forteen', 'threteen', 'seaven',
                     'stollen', 'boated', 'meshed', 'disfranchized', 'absconded', 'empty-headed', 'alloted',
                     'skyrocketed', 'jogged', 'clubfooted', 'mustached', 'cowered', 'hagen', 'copulated', 'readdressed',
                     'lshed', 'prosed', 'twicedivided', 'bellshaped', 'vamped', 'unasked', 'it1ept', 'uiunt', 'ied',
                     'helieved', 'obscurantisrn', 'dqqfint', "'lt", 'rechristen', 'wrongheaded', 'velarized', 'ladled',
                     'unimagined', 'batterypowered', 'lacerated', 'bladed', 'doublechecked', 'pivot-pattern',
                     'tasseled', 'atrutonen', 'newlyqqdiscovered', 'unconquered', 'oetween', "'.'that", 'raid.when',
                     'quaked', 'unshackled', 'unforgiven', 'configurated', 'farsighted', 'custombased', 'fizzled',
                     'glamourized', "'e.stern", 'brassfaced', 'keled', 'gabbled', 'pipped', 'decamped', 'atomised',
                     'batsmen', 'unexceeded', 'undefeated', 'scouted', 'crystalized', 'screeched', 'pedailed',
                     'pummelled', 'philibustered', 'midden', 'unlicensed', 'majority.owned', 'writted', 'vied',
                     'marveled', 'tellen', 'unenclosed', 'fine-drawn', 'eyren', 'abasshed', 'downrazed', 'unhedged',
                     'boded', 'longestablished', 'ofblyden', 'weredivided', 'bewailed', 'worseegypt', 'flagellated',
                     'weresummoned', 'whocalled', 'regar:led', 'eiupted', 'thatraged', 'wasdescribed', 'thenserved',
                     'everconceived', 'community,modeled', 'communiqueissued', 'wasconditioned', 'wereincorporated',
                     'wasupgraded', 'hetween', 'principled', 'organizationincorporated', 'officialunited', 'wasbrought',
                     'hisunauthorized', 'hasinfected', 'mqqnt', 'planked', 'necked', 'singlehanded', 'roofed',
                     'nimroded', 'rainswept', 'rouged', 'wheezed', 'hiccuped', 'hadappended', 'wereintended',
                     'bebought', 'ofseamen', 'toadopt', 'hadextended', 'raged', 'hasswallowed', 'whichenjoyed',
                     'nrnhlprn', 'andmanned', 'manyseamen', 'wassubjected', 'thenmounted', 'wereissued', 'wastaken',
                     'thelaundrymen', 'hadbeen', 'itseemed', 'ctrirrlrn', 'theneed', 'hadcommandeered', 'dinned',
                     'werefined', 'andseamen', 'itremained', 'tooprotracted', 'howled', 'delegatesclaimed',
                     'whoattended', 'shipsdevised', 'toaccept', 'half-timbered', 'selfcontained', 'pigged', 'barrelled',
                     'deputised', 'thlt', 'suiiiered', 'bhhorn', 'to0senbliqqqqqqenqqqqen', 'inilncnced', 'crnt',
                     'ea:ercised', 'summareed', 'havered', 'refrained', 'brummagen', 'recommissioned', 'selfproduced',
                     'electronicsrelated', 'beaded', 'unconsecrated', 'bearchildren', 'theunborn', 'ofunmarried',
                     'hadencouraged', 'fromsouthern', 'becomeslegitimatized', 'andwhen', 'himexpelled', 'hestudied',
                     'wasproduced', 'wasdiscredited', 'lectures,extended', 'hadsynthesized', 'liquorcured', 'unsifted',
                     'wasreplaced', 'hetraveled', 'discuiied', 'sicklied', 'wasillustrated', 'formationbetween',
                     'perceptivelylinked', 'broughtincreased', 'insouthern', 'ineastern', 'fondled', 'ofacquired',
                     'heestablished', 'thatdeemphasized', 'weredestroyed', 'thatcontributed', 'establishmentshelped',
                     'probablyrejected', 'theorized', 'anddecided', 'andeven', 'wasthreatened', 'andabandoned',
                     'wasappropriated', 'rebelled', 'vowelled', 'boasted', 'browed', 'cameramen', 'milkmen',
                     'pitchforked', 'hooted', 'undimmed', 'yen', 'footmen', 'sunburnt', 'mildflavoured'}

}
