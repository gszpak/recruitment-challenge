The whole classification process consists of two main steps:

1. JSON preprocessing (json_transformer package), which includes:
    - extracting text from HTML and detecting language
    - translation to english
    - converting unicode to ascii equivalents
    - filtering non - words (URLS etc.)

    This step is performed by running run_transform_jsons.py script.

    WARNING: as translation step uses external API, it takes A LOT of time to complete.
    You will find translated jsons after performing 2 first substeps in data/companies_translated.txt


2. Building final model and running 3 - fold cross-validation (classifier package). This includes:
    - filtering parts of speech different than nouns and verbs
    - lemmatization
    - converting words to vector space
    - TF-IDF wieghting
    - running SVM classifier (gradient descent implementation)

    This step is performed by running run_classification.py script.

    NOTE: Cross - validation is performed only on one set of parameters (it will take
    too long otherwise) - you can find the whole grid in run_classification.py
