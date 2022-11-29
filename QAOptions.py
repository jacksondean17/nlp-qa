class QAOptions:
    def __init__(self, num_candidate_sentences=3):
        self.num_candidate_sentences = num_candidate_sentences
        self.sentence_scoring_weights = {
            'keyword_exact_match': 1,
            'keyword_synonym_match': 0.5,
            'q_type_ner_category': {
                'HUM': 0.1,
                'NUM': 0.1,
                'LOC': 0.25,
                'ENT': 0.25,
                'DES': 0
            },
            'q_type_ner_category_fine': {
                'DES.definition': 0.5,
                'DES.description': 0.5,
                'DES.reason': 0.5,
                'ENT.animal': 2.5,
                'ENT.event': 2.5,
                'ENT.other': 0.5,
                'ENT.term': 0.5,
                'HUM.description': 2.5,
                'HUM.group': 2.5,
                'HUM.individual': 3.5,
                'LOC.city': 2.5,
                'LOC.country': 2.5,
                'LOC.other': 2.5,
                'NUM.age': 2.5,
                'NUM.count': 2.5,
                'NUM.date': 2.5,
                'NUM.distance': 2.5,
                'NUM.money': 4.5,
                'NUM.other': 2.5,
                'NUM.period': 2.5
            }
        }
