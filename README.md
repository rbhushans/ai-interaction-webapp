# TEA - Transparency and Education of Artificial Intelligence Web-App


## Setup Instructions:
1. Clone the repository
2. Make sure you have [Python 3.9](https://www.python.org/downloads/release/python-390/) installed and you're running all commands from now on with version 3.9
3. In the root directory of the cloned repo, run the following commands  
    1. Remove any existing virtual environments:  
    `$ rm -rf env`  
    2. Create a virtual environment:   
    `$ python -m venv env`   
    3. Activate the virtual env and set correct Flask variables:  
        - (Linux/Mac):  
        `$ source env/bin/activate && export FLASK_APP=run.py && export FLASK_ENV=development && flask run`  
        - (Windows)  
        `$ source env/Scripts/activate && export FLASK_APP=run.py && export FLASK_ENV=development`  
    4. Upgrade pip:  
    `$ pip install --upgrade pip`
    5. Install all required python packages:  
    `$ pip install -r requirements.txt` 

## Run Instructions:  
1. Start up Python virtual environment:  
    - (Linux/Mac):  
    `$ source env/bin/activate`  
    - (Windows)  
    `$ source env/Scripts/activate`    
2. Run the application:  
`$ flask run`  
3. Open browser and navigate to **localhost:5000**

