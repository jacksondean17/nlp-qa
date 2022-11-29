from preprocess import Preprocess as pp
import sklearn as sk
from sklearn import svm, naive_bayes
import numpy as np


class QuestionClassifier:
    """
    Question classes
    DES: Description
    ENT: Entity
    HUM: Human
    LOC: Location
    NUM: Number
    """
    def __init__(self, training_file=None):
        np.random.seed(0)

        self.classifier = None
        self.vectorizer = None
        self.label_encoder = None
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None
        self.training_file = training_file

        if training_file:
            self.train(self.training_file)

    def train(self, training_file):
        X = []
        y = []
        questions = self.parse_question_file(training_file)
        processed_questions = self.preprocess_questions(questions)

        # encode the labels
        # only doing coarse-grained classification for now
        # labels = [l[0] for q, l in questions]

        # trying fine-grained classification
        labels = ['.'.join(l) for q, l in questions]

        self.label_encoder = sk.preprocessing.LabelEncoder()
        Y = self.label_encoder.fit_transform(labels)

        # vectorize the questions
        self.vectorizer = sk.feature_extraction.text.TfidfVectorizer(max_features=5000)
        X = self.vectorizer.fit_transform([" ".join(q) for q in processed_questions])

        # split into training and test sets
        self.X_train, self.X_test, self.Y_train, self.Y_test = sk.model_selection.train_test_split(X, Y, test_size=0.2)

        # train the classifier with SVM
        self.classifier = sk.svm.SVC(kernel='linear', C=1.0)
        self.classifier.fit(self.X_train, self.Y_train)

    def evaluate(self):
        Y_pred = self.classifier.predict(self.X_test)
        print(sk.metrics.classification_report(self.Y_test, Y_pred, target_names=self.label_encoder.classes_, labels=self.label_encoder.transform(self.label_encoder.classes_)))

    def save(self, filename):
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        print('loading classifier')
        import pickle
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def preprocess_questions(questions):
        processed_questions = [pp.preprocess_question(q) for q, l in questions]
        # processed_questions = [pp.word_tokenize(q) for q, l in questions]
        # processed_questions = [pp.remove_stopwords(q, is_question=True) for q in processed_questions]
        # processed_questions = [pp.lemmatize(q) for q in processed_questions]
        return processed_questions

    def classify(self, question):
        x = self.vectorizer.transform([" ".join(question)])
        y = self.classifier.predict(x)
        return self.label_encoder.inverse_transform(y)

    @staticmethod
    def parse_question_file(file):
        questions = []
        with open(file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith("Question:"):
                    question = line[10:].strip()
                    line = f.readline()
                    label = tuple(line[7:].strip().split('.'))
                    questions.append((question, label))
                    continue

        return questions


if __name__ == "__main__":
    qc = QuestionClassifier("./test-files/question_training.txt")
    qc.evaluate()

    qc.save("./test-files/question_classifier.pkl")

    # print the results
#    print(sk.metrics.classification_report(Y_test, Y_pred, target_names=label_encoder.classes_))
#    print(sk.metrics.confusion_matrix(Y_test, Y_pred))

#    print(Y_pred)



