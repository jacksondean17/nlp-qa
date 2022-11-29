class QAOptions:
    def __init__(self, num_candidate_sentences=3):
        self.num_candidate_sentences = num_candidate_sentences
        self.sentence_scoring_weights = {
            'keyword_exact_match': 2,
            'keyword_synonym_match': 0.67785672,
            'q_type_ner_category': {
                'HUM': 0.1,
                'NUM': 0.1,
                'LOC': 0.25,
                'ENT': 0.25,
                'DES': 0
            },
            'q_type_ner_category_fine': {
                'DES.definition': 11.35171585,
                'DES.description': 11.35171585,
                'DES.reason': 11.35171585,
                'ENT.animal': 11.35171585,
                'ENT.event': 11.35171585,
                'ENT.other': 11.35171585,
                'ENT.term': 11.35171585,
                # 'HUM.description': -0.55295808,
                'HUM.description': 1,
                'HUM.group': 1.39260914,
                # 'HUM.individual': -0.59016995,
                'HUM.individual': 1,
                'LOC.city': 2.,
                'LOC.country': 2.39668005,
                'LOC.other': -1.46443904,
                'NUM.age': 13.90968495,
                'NUM.count': 2.41707517,
                'NUM.date': 0.39260913,
                'NUM.distance': 16.46765406,
                'NUM.money': 13.90968495,
                'NUM.period': 1.02128626
            }
        }
