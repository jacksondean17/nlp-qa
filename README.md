# CS 5340 Question Answering System
## Team Members
* Jackson Dean (solo team)

## Running the Program
1. Navigate to the root directory of the project.
   If you are running it on the CADE machines, this will be
    ```
    /home/u1100004/cs5340-qa/
    ```
   The project was tested on machine `lab1-14.eng.utah.edu`.

2. Activate the virtual environment 
    ```
    source ./venv/bin/activate.csh
    ```
3. Run the program
    ```
    python3 qa.py <path to input file>
    ```
## Options
Optionally, you can provide one or two extra files to the program
```
python3 qa.py <path to input file> <path to output file> <path to answer file>
```
If you provide the output file, the program will write the output to that file rather than printing to `stdout`.

If you provide the answer file as well, the program will write the output to the output file, then compare the answers
to those given in the answer file and print the accuracy of the system as determined by `score-answers.pl`

## External Libraries
* [NLTK](http://www.nltk.org/) - Natural Language Toolkit
    * Tokenization
    * POS tagging
* [spaCy](https://spacy.io/) - Industrial-Strength Natural Language Processing
    * NER
    * Used model `en_core_web_sm`
* [scikit-learn](http://scikit-learn.org/stable/) - Machine Learning in Python
    * TF-IDF vectorization
    * SVM classifier
* [rake-nltk](https://pypi.org/project/rake-nltk/) - Rapid Automatic Keyword Extraction
    * *Unused in final version but still present in codebase*
    * Keyword extraction
* [numpy](https://numpy.org/) - Numerical Python
    * Required by other libraries
* [scipy](https://www.scipy.org/) - Scientific Python
    * Parameter optimization

### NLTK Data
The following nltk datasets are required to be downloaded before running.
* punkt
* stopwords
* wordnet
* omw-1.4
* averaged_perceptron_tagger
* words

### spaCy Data
The following spaCy model is required to be downloaded before running.
* en_core_web_sm

## Time Estimate
The QA tool takes approximately **6.25s** to process a single story. However, some of this time is spent on initial 
setup which is only required once, not for every story.

This startup time includes training a question classifier using the training data in test-files/question_training.txt.

## Known Problems
None
