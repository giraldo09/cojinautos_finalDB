# Technical instructions

## Create and activate Python virtual environment
bash
    python -m venv venv
    .\venv\Scripts\Activate

## Activar permisos para inicia el entorno, solo sino lo 
´´´bash
    Set-ExecutionPolicy RemoteSigned
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
´´´
## Install dependencies
Create file requirements.txt

bash
    pip install -r requirements.txt


## Run FastAPI

bash
    FastAPI uvicorn app.main:app --reload
 


## Run streamlit project

bash
    streamlit run app.py 


# Utilities
## Steps to remove virtual environment
bash
    deactivate
    rm -rf venv


## Steps to remove files uploaded to github with gitignore
bash
    git rm --cached -r .


## Steps to create a new branch 
bash
    git checkout -b feature/"name of the branch"


## Steps to fetch changes from main branch
bash
    git fetch#   c o j i n a u t o s _ f i n a l 
 
 #   c o j i n a u t o s _ f i n a l D B  
 