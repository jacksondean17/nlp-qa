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
            }
        }
