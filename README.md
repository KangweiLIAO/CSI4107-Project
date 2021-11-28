# CSI4107 Assignment 2
## Teamwork Distribution
Langqing Zou (300035036)
- Responsible for **Processing section**.
- Responsible for **Returing result file section**.
- Responsible for **doc2vec implementation and evaluation**
- Responsible for writing **README.md**.

Kangwei Liao (8568800)
- Responsible for **Indexing Section**.
- Responsible for **Evaluation Section**.
- Responsible for **word2vec implementation and evaluation**
- Responsible for **code integration** and **final check**.

Aozhuo Zhang (300057882)
- Responsible for **Retrieval and Ranking Section**.
- Responsible for writing **README.md**.

## Steps To Run (Python 3.9 required)
1. Make sure the python version == 3.9
2. Create a virtual environment under project directory:
   - using ```python3 -m venv venv``` (Linux / [Mac OS](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html))
   - using ```python3 -m venv /path/to/new/virtual/environment```
   under project directory ([Windows](https://docs.python.org/3/library/venv.html))
3. Activate the virtual environment:
   - using ```source venv/bin/activate``` (Linux / Mac OS)
   - using ```python -m venv c:\path\to\myenv``` (Windows)
4. Install the packages specified in ```requirements.txt``` using the venv created
   - execute ```python -m spacy download en_core_web_sm``` if the language model ```en_core_web_sm``` is missing
5. Run ```main.py``` using the **Python interpreter in virtual environment**