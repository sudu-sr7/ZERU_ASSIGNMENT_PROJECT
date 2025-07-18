# Aave V2 Wallet Credit Scoring System

This project provides a robust command-line tool for assigning a credit score (from 0 to 1000) to DeFi wallets based on their historical transaction data from the Aave V2 protocol. The script analyzes wallet behavior to identify reliable users versus those who exhibit risky or exploitative patterns.

---

## Architecture and Processing Flow

The system is built as a single, flexible Python script (`credit_scoring.py`) that leverages standard data science libraries.

**Architecture:**
1.  **Command-Line Interface**: Utilizes Python's `argparse` module to accept file paths as arguments, making the tool flexible and easy to integrate into automated workflows.
2.  **Data Ingestion**: Loads transaction data from a user-specified JSON file.
3.  **Data Processing**: Efficiently groups all transactions by their wallet address using `collections.defaultdict`.
4.  **Feature Engineering**: For each wallet, the script calculates a set of key behavioral features, including transaction volumes, wallet age, Loan-to-Value (LTV) ratios, repayment history, and liquidation events.
5.  **Scoring Logic**: A rule-based engine applies a series of bonuses and penalties to a baseline score based on the engineered features. The logic includes robust error handling to manage incomplete or malformed data.
6.  **Output Generation**: The final scores are saved to a clean `wallet_scores.csv` file, and a score distribution histogram is generated and saved as `score_distribution.png`.

---

## How to Run

Follow these steps to set up and run the credit scoring system.

** 1. Create a Virtual Environment**

First, create and activate a virtual environment in the project directory.
# Create the environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate

**2. Install Dependencies**
## With the virtual environment active, install the necessary Python libraries.
pip install matplotlib numpy

**3. Execute the Script**
## Run the script from your terminal, providing the path to the transaction data file as an argument.
python credit_scoring.py user-wallet-transactions.json