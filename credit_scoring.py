import json
import argparse
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def calculate_credit_score(wallet_address, transactions):
    total_deposits_usd = 0
    total_borrows_usd = 0
    total_repays_usd = 0
    total_redeems_usd = 0
    liquidation_count = 0
    transaction_count = len(transactions)
    timestamps = [tx['timestamp'] for tx in transactions]
    wallet_age_days = (datetime.now().timestamp() - min(timestamps)) / (60 * 60 * 24) if timestamps else 0

    for tx in transactions:
        action = tx.get('action')
        action_data = tx.get('actionData', {})
        amount_str = action_data.get('amount', '0')
        price_str = action_data.get('assetPriceUSD', '0')
        
        try:
            amount_usd = float(amount_str) * float(price_str)
        except (ValueError, TypeError):
            amount_usd = 0

        if action == 'deposit':
            total_deposits_usd += amount_usd
        elif action == 'borrow':
            total_borrows_usd += amount_usd
        elif action == 'repay':
            total_repays_usd += amount_usd
        elif action == 'redeemunderlying':
            total_redeems_usd += amount_usd
        elif action == 'liquidationcall':
            liquidation_count += 1

    # --- Scoring Logic ---
    score = 500  # Base score

    # Transaction Volume Score
    if total_deposits_usd > 100000:
        score += 150
    elif total_deposits_usd > 10000:
        score += 100
    elif total_deposits_usd > 1000:
        score += 50

    # Wallet History Score
    if wallet_age_days > 365:
        score += 100
    elif wallet_age_days > 180:
        score += 50

    # LTV Score
    ltv = total_borrows_usd / total_deposits_usd if total_deposits_usd > 0 else 0
    if ltv < 0.25:
        score += 200
    elif ltv < 0.5:
        score += 100
    elif ltv >= 0.75:
        score -= 100

    # Repayment Score
    repayment_ratio = total_repays_usd / total_borrows_usd if total_borrows_usd > 0 else 0
    if repayment_ratio >= 1:
        score += 200
    elif repayment_ratio >= 0.8:
        score += 100
    else:
        score -= 50

    # Liquidation Penalty
    score -= liquidation_count * 250

    # Transaction Count Score
    if transaction_count > 100:
        score += 100
    elif transaction_count > 50:
        score += 50

    # Bot-like Activity Penalty
    if len(timestamps) > 1:
        time_diffs = np.diff(sorted(timestamps))
        if np.mean(time_diffs) < 60:
            score -= 100

    # Clamp score between 0 and 1000
    score = max(0, min(1000, score))

    return {"wallet": wallet_address, "score": int(score)}


def analyze_and_plot(scores, output_path):
    # Plot histogram
    wallet_scores = [item['score'] for item in scores]
    plt.figure(figsize=(10, 6))
    plt.hist(wallet_scores, bins=10, range=(0, 1000), edgecolor='black')
    plt.title('Wallet Score Distribution')
    plt.xlabel('Credit Score')
    plt.ylabel('Number of Wallets')
    plt.xticks(range(0, 1001, 100))
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.savefig(f"{output_path}/score_distribution.png")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="DeFi Wallet Credit Scoring System")
    parser.add_argument("input_file", help="Path to user-wallet-transactions.json")
    parser.add_argument("--output_dir", default=".", help="Directory to save results")
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        data = json.load(f)

    # Group transactions by wallet
    wallets = defaultdict(list)
    for tx in data:
        wallets[tx['userWallet']].append(tx)

    # Calculate scores
    scores = [calculate_credit_score(wallet, txs) for wallet, txs in wallets.items()]

    # Save to CSV
    output_csv = f"{args.output_dir}/wallet_scores.csv"
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["wallet", "score"])
        writer.writeheader()
        writer.writerows(scores)

    print(f"Saved scores to {output_csv}")

    # Plot and save distribution graph
    analyze_and_plot(scores, args.output_dir)


if __name__ == "__main__":
    main()
