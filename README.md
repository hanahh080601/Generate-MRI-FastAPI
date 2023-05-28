# Sentiment Classification using BERT model (Pytorch, FastAPI, MongoDB & Jinja2)

## Tasks 
* Preprocessing data
  * Loading data.
  * Bert tokenizing.
* Building model
  * Load Bert-based model and config with Dropout & Linear layers at last.
  * Override forward function.
* Training
  * Define criterion, optimizer.
  * Execute (train, validate).
  * Early stopping. 
  * Save model.
* Evaluating
  * Accuracy: approx 93% on test set.


## Installation

Clone the repo from Github and pull the project.
```bash
git clone https://github.com/hanahh080601/Sentiment-Classification.git
git checkout front-end (if necessary: includes UI)
git pull
cd sentiment-classification/sentiment-classification
poetry install
poetry config virtualenvs.in-project true
poetry update
```

# Project tree 
```bash
.  
├── sentiment-classification            
│     ├── .venv               
│     ├── poetry.lock      
│     ├── pyproject.toml     
│     ├── README.rst    
│     └── sentiment-classification      
│           ├── database              
│           │      ├── __init__.py       
│           │      └── database.py                 
│           ├── models          
│           │      ├── bert.py      
│           │      ├── best_model.pt (not pushed)        
│           │      └── comment.py        
│           ├── predict         
│           │      ├── __init__.py       
│           │      └── train.py     
│           ├── routes                
│           │      └── comment.py     
│           ├── schemas                
│           │      └── comment.py    
│           ├── static                
│           │      └── style.css    
│           ├── templates                
│           │      └── index.html     
│           ├── notebooks         
│           │      ├── Sentiment-Classification.ipynb        
│           │      └── test.ipynb         
│           ├── __init__.py  
│           ├── main.py         
│           └── config    
│                  ├── config.py              
│                  └── mongodb.py    
├── tests           
│     ├── __init__.py            
│     └── test_sentiment_classification.py             
├── .gitignore                         
└── README.md       
```

## Usage: 
```bash
cd sentiment-classification/sentiment-classification
uvicorn main:app --reload
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Lê Hoàng Ngọc Hân - Đại học Bách Khoa - Đại học Đà Nẵng (DUT)](https://github.com/hanahh080601) 
