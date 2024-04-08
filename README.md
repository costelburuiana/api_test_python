# API testing with Python, Pytest and pytest-allure plugin to generate a report

### In this folder, I created automation tests using https://airportgap.com/ API.

All the tests are running in a virtual environment (pipenv). To run the tests in the same enviroment, please follow these steps:

* `pip install pipenv` → to install Pipenv on your local machine
* `pipenv install` → the command will look for a Pipenv file. If it doesn’t exist, it will create a new environment and activate it. After the above command is run, we’ll find two new files: Pipfile and Pipenv.lock
* `pipenv shell` → to activate already created pipenv environment
* `pipenv install -r requirements.txt` → install dependencies from requirements.txt

Bellow are the commands to run the tests on local machine:

1. `pytest --alluredir=report` → will generate the JSON files for each test case in the `report` folder that will be used to view the report.
2. `allure serve report` → report will open in the default browser.
 
The credentials that generated the `bearer token` are stored in the `.env` file on local machine.

### An HTML report can be visualized on https://costelburuiana.github.io/api_test_python/