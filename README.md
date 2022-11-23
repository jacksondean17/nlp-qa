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
    * Used for tokenization, POS tagging, NER
* [rake-nltk](https://pypi.org/project/rake-nltk/) - Rapid Automatic Keyword Extraction
    * Used for keyword extraction
* [numpy](https://numpy.org/) - Numerical Python
    * Required by other libraries

### NLTK Data
The following nltk datasets are required to be downloaded before running.
* punkt
* stopwords
* wordnet
* omw-1.4
* averaged_perceptron_tagger

(not sure if I need this yet)
* maxent_ne_chunker
* words

## Time Estimate
The QA tool takes approximately **6.25s** to process a single story.

## Known Problems
None
