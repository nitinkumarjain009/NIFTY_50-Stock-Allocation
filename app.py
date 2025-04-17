name: Stock Analysis Workflow
on:
  push:
    branches:
      - main
jobs:
  run-stock-analysis:
    runs-on: ubuntu-latest
    env:
      TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
      TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      INVESTMENT_AMOUNT: 100000    # Default investment: 100,000 INR
      INVESTMENT_DURATION: "12"      # Default duration: 12 months
      RISK_LEVEL: "medium"           # Default risk level: medium
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Verify project structure
        run: |
          ls -R
        working-directory: ${{ github.workspace }}

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Create and activate virtual environment
        run: |
          python -m venv venv
          source venv/bin/activate
          echo "PYTHONPATH=$PYTHONPATH:$GITHUB_WORKSPACE" >> $GITHUB_ENV
        working-directory: ${{ github.workspace }}

      - name: Install dependencies
        run: |
          source venv/bin/activate
          pip install yfinance pandas numpy python-telegram-bot==20.7
          pip install -r requirements.txt
        working-directory: ${{ github.workspace }}

      - name: Fetch Real-Time Stock Data
        run: |
          source venv/bin/activate
          python modules/stock_data_fetcher.py
        working-directory: ${{ github.workspace }}

      - name: Compute Stock Indicators
        run: |
          source venv/bin/activate
          python modules/feature_engineering.py
        working-directory: ${{ github.workspace }}

      - name: Generate Stock Recommendations
        run: |
          source venv/bin/activate
          python modules/recommendation.py
        working-directory: ${{ github.workspace }}

      - name: Send Recommendations to Telegram
        run: |
          source venv/bin/activate
          python modules/send_telegram.py
        working-directory: ${{ github.workspace }}

      - name: Optimize Portfolio Allocation
        run: |
          source venv/bin/activate
          python models/portfolio_optimizer.py
        working-directory: ${{ github.workspace }}

      - name: Run Full Stock Allocation System
        run: |
          source venv/bin/activate
          python app.py
        working-directory: ${{ github.workspace }}
