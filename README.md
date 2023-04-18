# Legalsong
* A website that analyzes the probability of conviction under Korea's insult law in Korean sentences. <br>
* Provides similar cases related to insult law. <br>

We trained 187 insult law judgment documents. <br>
Getting an idea from sentiment analysis, we labeled each case as guilty or innocent, and then ran a classification. <br>

## Dataset
Crawled judgment documents related to insult law from [CaseNote](https://casenote.kr/) and [LegalSearch](https://legalsearch.kr/) using <img src="https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=Selenium&logoColor=white"/> <br>
Then, extracted the insult sentences from each case and labeled them as guilty or innocent.
* Guilty 152, Innocent 35
* Added the Korean SNS dataset(AI hub) as innocent case to address class imbalance.
* Text augmentation using [ktextaug](https://github.com/jucho2725/ktextaug) : Guilty 760, Innocent 760

## Classification
Logistic Regression, LSTM, Transformer <br>
...

## Text similarity
Calculate the __Cosine similarity__ between the input sentece and the entire case dataset. <br>
Used: KoNLPy(Okt), Scikit-learn


## Web
Tech stack: <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white"/>  <img src="https://img.shields.io/badge/MariaDB-003545?style=flat&logo=mariaDB&logoColor=white"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=HTML5&logoColor=white"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=white"/>
