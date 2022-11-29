from scipy.optimize import minimize
from qa import QA
from qa_evaluator import QAEvaluator
from QAOptions import QAOptions
import numpy as np

# f = 'testset1'
f = 'full-devset'

class QAOptimizer:
    def __init__(self):
        self.options = QAOptions()
        self.qa = QA(f'./test-files/{f}.input', options=self.options)
        self.qa_eval = QAEvaluator()
        pass

    def evaluate_with_weights(self, weights, flip=False):
        self.options.sentence_scoring_weights['keyword_exact_match'] = weights[0]
        self.options.sentence_scoring_weights['keyword_synonym_match'] = weights[1]
        '''
        self.options.sentence_scoring_weights['q_type_ner_category']['HUM'] = weights[2]
        self.options.sentence_scoring_weights['q_type_ner_category']['NUM'] = weights[3]
        self.options.sentence_scoring_weights['q_type_ner_category']['LOC'] = weights[4]
        self.options.sentence_scoring_weights['q_type_ner_category']['ENT'] = weights[5]
        self.options.sentence_scoring_weights['q_type_ner_category']['DES'] = weights[6]
        '''
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['DES.definition'] = weights[2]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['DES.description'] = weights[3]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['DES.reason'] = weights[4]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['ENT.animal'] = weights[5]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['ENT.event'] = weights[6]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['ENT.other'] = weights[7]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['ENT.term'] = weights[8]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['HUM.description'] = weights[9]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['HUM.group'] = weights[10]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['HUM.individual'] = weights[11]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['LOC.city'] = weights[12]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['LOC.country'] = weights[13]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['LOC.other'] = weights[14]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.age'] = weights[15]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.count'] = weights[16]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.date'] = weights[17]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.distance'] = weights[18]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.money'] = weights[19]
        self.options.sentence_scoring_weights['q_type_ner_category_fine']['NUM.period'] = weights[20]

        self.qa.answer_questions()
        self.qa.save_answers(f'./test-files/{f}.response')

        res = self.qa_eval.evaluate_quiet(f'./test-files/{f}.response', f'./test-files/{f}.answers')
        print(res)
        if flip:
            return res
        else:
            return 1-res

i = 0
def callback(xk):
    global i
    i += 1
    print('Iter: ', i)
    return False

qa = QAOptimizer()
# for i in range(10):
    # print(qa.evaluate_with_weights([i/10]))


print('Starting optimization')
#res = minimize(qa.evaluate_with_weights, np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]), method='powell', options={'disp': True, 'adaptive': True}, callback=callback)
res = minimize(qa.evaluate_with_weights, np.ones(21), method='powell', options={'disp': True, 'adaptive': True}, callback=callback)
print(res.x)

print(qa.evaluate_with_weights(res.x, flip=True))

