class QAOptions:
    def __init__(self, num_candidate_sentences=3):
        self.num_candidate_sentences = num_candidate_sentences
        self.sentence_scoring_weights = {
            'keyword_exact_match': 1,
            'keyword_synonym_match': 0.5,
            'wh_word_ner_category': 1
        }
