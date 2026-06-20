# PulseAPI

A machine learning model-serving API. Trains a `RandomForestClassifier` on the
Wine dataset and serves predictions through a FastAPI REST API.

## What It Does

Send a `POST` request with 13 wine chemistry measurements, get back a predicted
wine class with a confidence score — all over HTTP.

## Tech Stack

- **Python 3.13**
- **FastAPI** — web framework
- **scikit-learn** — model training
- **Pydantic** — request/response validation
- **pytest** — testing
- **GitHub Actions** — CI

## Project Structure
