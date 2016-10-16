# Create a python3 virtualenv
virtualenv venv -p $(which python3)
# Enter python virtualenv
. venv/bin/activate
# Install python packages: flask
pip install -r requirements.txt

