# M-Pesa Ledger CLI 2026

A command-line tool designed to parse M-Pesa transaction SMS history and generate structured financial reports. It helps users track spending, analyze monthly cash flows, and identify top transaction recipients.

## Features
- **Automated Parsing**: Uses regex to extract ID, Amount, Date, Time, and Counterparty from raw SMS text.
- **Transaction Categorization**: Automatically identifies Send Money, Receive Money, Paybill, and Agent Withdrawals.
- **Financial Insights**: Generates summaries of spending by category and monthly trends.
- **CSV Export**: Export parsed data for use in Excel or other accounting software.

## Installation
1. Ensure you have Python 3.8+ installed.
2. Clone this repository or download the files.

## Usage
1. Copy your M-Pesa SMS messages into a text file (e.g., `messages.txt`).
2. Run the tool:
   ```bash
   python main.py messages.txt
   ```
3. Export to CSV:
   ```bash
   python main.py messages.txt --csv report.csv
   ```

## Data Privacy
This tool processes data locally on your machine. No transaction information is uploaded to any external server.