from indicators import run
from classes import run_info


if __name__ == "__main__":
    ticker = input("Type ticker of stock:")
    run(ticker)
    run_info(ticker)