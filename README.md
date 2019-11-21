# Toxicity-Classifier
 Classifier of toxic language

## Development

### Setup
These were confirmed on macOS Catalina with both python (2.2.7) and python3 (3.7.5) binaries installed. You may need to use just `python` instead of `python3` and `pip` instead of `pip3` depending on your environment:
- `virtualenv --python=/usr/bin/python3 .`
- `pip3 install -r requirements.txt`
- `python3 -m spacy download en_core_web_sm`

### Run
- `python manage.py runserver`
