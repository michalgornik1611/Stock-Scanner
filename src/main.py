from indicators import run
from classes import run_info, run_chart
from forecast import run_forecast


if __name__ == "__main__":
    ticker = input("Type ticker of stock to see indicator analysis:")
    try:
        run(ticker)
        question1 = (input("Do you want to see personalized chart? y/n"))
        if question1 == 'y':
            run_chart(ticker)
        elif question1 == 'n':
            pass
    except:
        print ("Wrong input!")

    try:
        question2 = (input("Do you want to see main information about company and latest recommendations? y/n"))
        if question2 == 'y':
            run_info(ticker)
        elif question2 == 'n':
            pass
        else:
            print ("Wrong input!")
    except:
        print("Wrong input!")

    try:
        question3 = (input("Do you want to see our forecast of results in 2023? y/n"))
        if question3 == "y":
            run_forecast(ticker)
        else:
            print ("Bye!")
    except:
        print ("Wrong input!")