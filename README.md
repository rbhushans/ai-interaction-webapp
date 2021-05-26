# ai-interaction-webapp


Run the following commands from the root directory:
* Create virtual environment and set environment variables:

rm -rf env

python -m venv env

source env/bin/activate && export FLASK_APP=run.py && export FLASK_ENV=development && flask run
*If on Windows: source env/Scripts/activate && export FLASK_APP=run.py && export FLASK_ENV=development  

* Install dependencies:

pip install --upgrade pip

pip install -r requirements.txt

* Run the application:

flask run


# Notes
If no changes are seen after changing static files, do a hard refresh with CMD + SHIFT + R