# ♠️ Poker hand evaluator

[![Test](https://github.com/Kaltsoon/poker-hand-evaluator/actions/workflows/test.yml/badge.svg)](https://github.com/Kaltsoon/poker-hand-evaluator/actions/workflows/test.yml)

Poker hand evaluator implemented with Python.

## How to use

Run the code with `python3 src/index.py`. The code generates a new hand and evaluates its rank.

## Running tests 

1. Create a virtual environmennt by running `python3 -m venv env` and activate it by running `source env/bin/activate`.
2. Install dependencies inside the virtual environment by running `pip3 install -r requirements.txt`.
3. Inside the virtual environment run the tests with `inv test`. Coverage report can be generated with `inv coverage-report`.
