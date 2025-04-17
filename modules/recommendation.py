from modules.stock_analysis import get_top_performers
from models.portfolio_optimizer import allocate_portfolio

def recommend_stocks(amount, duration, risk_level):
    top_stocks = get_top_performers(duration, risk_level)
    portfolio = allocate_portfolio(amount, top_stocks)
    
    recommendations = {
        "Stocks": top_stocks.to_dict(),
        "Portfolio Allocation": portfolio
    }
    
    return recommendations

if __name__ == "__main__":
    print(recommend_stocks(100000, 12, "medium"))
