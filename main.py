import re
import csv
import argparse
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Transaction:
    tx_id: str
    amount: float
    action: str
    recipient: str
    date: str
    time: str

class MpesaLedger:
    def __init__(self):
        # Regex to capture Transaction ID, Amount, Action, Entity, Date, and Time
        self.pattern = re.compile(
            r"([A-Z0-9]{10}) Confirmed\. (?:Ksh)?([\d,]+\.\d{2}) (sent to|paid to|received from|withdrawn from) (.+?) on (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]+)"
        )

    def parse_text(self, text: str) -> List[Transaction]:
        transactions = []
        for line in text.splitlines():
            match = self.pattern.search(line)
            if match:
                tx_id, amount_str, action, entity, date, time = match.groups()
                amount = float(amount_str.replace(",", ""))
                transactions.append(Transaction(tx_id, amount, action, entity.strip(), date, time))
        return transactions

    def generate_report(self, transactions: List[Transaction]):
        summary = defaultdict(float)
        categories = defaultdict(float)
        
        total_in = 0.0
        total_out = 0.0

        for tx in transactions:
            if tx.action in ['sent to', 'paid to', 'withdrawn from']:
                total_out += tx.amount
                categories[tx.recipient] += tx.amount
            else:
                total_in += tx.amount

        print("\n" + "="*40)
        print(" M-PESA FINANCIAL SUMMARY REPORT ")
        print("="*40)
        print(f"Total Transactions: {len(transactions)}")
        print(f"Total Received:     Ksh {total_in:,.2f}")
        print(f"Total Spent/Out:    Ksh {total_out:,.2f}")
        print(f"Net Cash Flow:      Ksh {(total_in - total_out):,.2f}")
        print("-"*40)
        
        print("Top 5 Expenses by Recipient:")
        sorted_exp = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for name, amt in sorted_exp[:5]:
            print(f" - {name[:20]:<20}: Ksh {amt:,.2f}")
        print("="*40 + "\n")

    def export_csv(self, transactions: List[Transaction], output_file: str):
        keys = ['tx_id', 'amount', 'action', 'recipient', 'date', 'time']
        with open(output_file, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            for tx in transactions:
                dict_writer.writerow(tx.__dict__)
        print(f"[+] Exported {len(transactions)} records to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="M-Pesa Ledger CLI 2026")
    parser.add_argument("input", help="Path to the text file containing M-Pesa SMS history")
    parser.add_argument("--csv", help="Optional: Export data to a CSV file", meta_var="FILE")
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {args.input} not found.")
        return

    ledger = MpesaLedger()
    tx_list = ledger.parse_text(content)

    if not tx_list:
        print("No valid M-Pesa transactions found in the input file.")
        return

    ledger.generate_report(tx_list)

    if args.csv:
        ledger.export_csv(tx_list, args.csv)

if __name__ == "__main__":
    main()