import sys
import os
from dotenv import load_dotenv

load_dotenv()



from src.stock_analyst.crew import StockAnalystCrew

def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    print(f"\n=== Analysing {ticker} ===\n")

    crew = StockAnalystCrew(ticker)
    result = crew.kickoff()

    print("\n=== FINAL REPORT ===")
    print(result)

    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{ticker}_report.txt", "w") as f:
        f.write(str(result))
    print(f"\nReport saved to reports/{ticker}_report.txt")

if __name__ == "__main__":
    main()