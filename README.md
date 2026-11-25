# CogniSight

CogniSight is a Python and Streamlit application for exploring student-performance predictions. The bundled scikit-learn random forest accepts 13 numeric features and returns a class (High, Medium or Low) and class probabilities. Its inputs cover study habits, attendance, previous GPA, and cognitive and logic assessments.

## Run locally

Use Python 3.12 in a virtual environment. From the repository root, run:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the URL printed by Streamlit. Use the built-in demo profile to explore a prediction without entering personal information.

## Deployment

Build the included Dockerfile and route traffic to port 8501, or set the PORT environment variable to the port assigned by your host. The model ships with the repository and does not require an inference API key.

## Model verification

The deployed artifact is a RandomForestClassifier. The repository contains the application and serialized model. Reproducing model selection or reporting held-out accuracy requires training data, split definitions, and evaluation artifacts. Treat its outputs as exploratory estimates.
