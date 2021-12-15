# Trans-Calc

Trans-Calc is a very simple rate calculator for freelance translators.

Translation agencies often apply word discounts depending on translation memory matches. Therefore, it's not always very straightforward to calculate your total rate for an assignment.

A typical discount matrix from an agency can look like this:

> ICE match -> 25% of rate
> 100% match -> 25% of rate
> 95-99 Fuzzy match -> 30% of rate
> 50-94 Fuzzy match -> 60% of rate
> 50-0 New words -> 100% of rate

With Trans-Calc, you can define specific matrices for each client, and insert the word count for each type of match.

If you would like to see a specific feature, please create an issue.

## For developers

If you would like to contribute to Trans-Calc, thank you! You are most welcome to do so.

To start, please follow these steps:

1. Fork the repository and `git clone` it to your local machine
2. Create a virtual environment and activate it
   - Mac/Linux: `python3 -m venv env` -> `source env/bin/activate`
   - Windows: `py -m venv env` -> `env\Scripts\activate`
3. Download the necessary dependencies for development
   - Mac/Linux/Windows `pip install -r requirements-dev.txt`
4. Happy coding!
