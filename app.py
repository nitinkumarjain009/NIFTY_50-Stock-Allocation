from modules.recommendation import recommend_stocks

def main():
    print("Welcome to the Nifty 50 Stock Recommendation System!")
    amount = float(input("Enter investment amount (INR): "))
    duration = int(input("Enter duration in months: "))
    risk_level = input("Enter risk level (low, medium, high): ")

    recommendations = recommend_stocks(amount, duration, risk_level)
    
    print("\nRecommended Stocks:")
    for stock, data in recommendations["Stocks"].items():
        print(f"{stock}: {data}")

    print("\nPortfolio Allocation:")
    for stock, amt in recommendations["Portfolio Allocation"].items():
        print(f"{stock}: ₹{amt}")

if __name__ == "__main__":
    main()
