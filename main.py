import re
import csv
import argparse
import sys
from collections import defaultdict
from datetime import datetime

# Standard M-Pesa Message Regex Patterns
PATTERNS = {
    'sent': re.compile(r"(?P<id>\w+) Confirmed\. Ksh(?P<amount>[\d,.]+).+sent to (?P<recipient>.+?) (?P<phone>\d+) on (?P<date>\d{1,2}/\d{1,2}/\d{2}) at (?P<time>\d{1,2}:\d{2} [APM]+)"),
    'received': re.compile(r"(?P<id>\w+) Confirmed\. You have received Ksh(?P<amount>[\d,.]+) from (?P<sender>.+?) (?P<phone>\d+) on (?P<date>\d{1,2}/\d{1,2}/\d{2}) at (?P<time>\d{1,2}:\d{2} [APM]+)"),
    'paybill': re.compile(r"(?P<id>\w+) Confirmed\. Ksh(?P<amount>[\d,.]+) paid to (?P<recipient>.+?) for account (?P<account>.+?) on (?P<date>\d{1,2}/\d{1,2}/\d{2}) at (?P<time>\d{1,2}:\d{2} [APM]+)"),
    'withdraw': re.compile(r"(?P<id>\w+) Confirmed\. Ksh(?P<amount>[\d,.]+) withdrawn from (?P<agent>.+?) on (?P<date>\d{1,2}/\d{1,2}/\d{2}) at (?P<time>\d{1,2}:\d{2} [APM]+)")
}

class MPesaLedger:
    def __init__(self):
        self.transactions = []

    def parse_text(self, text_content):
        lines = text_content.splitlines()
        for line in lines:
            for category, pattern in PATTERNS.items():
                match = pattern.search(line)
                if match:
                    data = match.groupdict()
                    data['type'] = category
                    data['amount'] = float(data['amount'].replace(',', ''))
                    self.transactions.append(data)
                    break

    def generate_report(self):
        summary = defaultdict(float)
        monthly_spend = defaultdict(float)
        recipients = defaultdict(float)
        
        for tx in self.transactions:
            summary[tx['type']] += tx['amount']
            month = datetime.strptime(tx['date'], "%d/%m/%y").strftime("%Y-%m")
            monthly_spend[month] += tx['amount']
            if 'recipient' in tx:
                recipients[tx['recipient']] += tx['amount']

        print("\n=== M-PESA FINANCIAL REPORT ===")
        print(f"Total Transactions Processed: {len(self.transactions)}")
        print("\n--- Totals by Category ---")
        for cat, amt in summary.items():
            print(f"{cat.capitalize():<12}: Ksh {amt:,.2f}")

        print("\n--- Monthly Cash Flow (Volume) ---")
        for month, amt in sorted(monthly_spend.items()):
            print(f"{month}: Ksh {amt:,.2f}")

        print("\n--- Top Recipients ---")
        sorted_recipients = sorted(recipients.items(), key=lambda x: x[1], reverse=True)[:5]
        for name, amt in sorted_recipients:
            print(f"{name[:20]:<20}: Ksh {amt:,.2f}")

    def export_csv(self, filename):
        if not self.transactions: return
        keys = self.transactions[0].keys()
        with open(filename, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.transactions)
        print(f"\n[+] Exported to {filename}")

def main():
    parser = argparse.ArgumentParser(description="M-Pesa Ledger CLI Tool")
    parser.add_argument("input", help="Path to text file containing M-Pesa messages")
    parser.add_argument("--csv", help="Export data to a CSV file", metavar="OUTPUT_FILE")
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {args.input} not found.")
        sys.exit(1)

    ledger = MPesaLedger()
    ledger.parse_text(content)
    
    if not ledger.transactions:
        print("No valid M-Pesa transactions found in the input file.")
        return

    ledger.generate_report()
    if args.csv:
        ledger.export_csv(args.csv)

if __name__ == "__main__":
    main()