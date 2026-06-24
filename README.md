# M-Pesa Ledger CLI 2026

A lightweight command-line utility to parse exported M-Pesa transaction SMS messages and generate personal finance insights.

## Features
- Parses standard M-Pesa SMS confirmation formats.
- Calculates total income vs. total expenditure.
- Identifies top expense categories/recipients.
- Exports parsed data to CSV for further analysis in Excel or Google Sheets.

## Requirements
- Python 3.7+

## Usage
1. Save your M-Pesa SMS history into a plain text file (e.g., `history.txt`).
2. Run the tool:
   ```bash
   python main.py history.txt
   ```
3. To export to CSV:
   ```bash
   python main.py history.txt --csv report.csv
   ```

## Expected SMS Format Example
`ABC123DEF4 Confirmed. Ksh2,500.00 paid to KPLC. on 15/6/26 at 8:45 PM.`
`GHI567JKL8 Confirmed. You have received Ksh1,000.00 from Jane Doe 0712345678 on 16/6/26 at 9:00 AM.`