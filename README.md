# Generative-AI

A Python script to generate a historical contribution graph on GitHub.

## Features

- Custom contribution frequency.
- Option to exclude weekends.
- Explicit start and end date support.
- Support for high-frequency contributions (up to 120/day).
- Automatic repository synchronization.
- 100% Emoji Free.

## Usage

1. Clone this repository.
2. Run the script:

   ```bash
   python contribute.py --repository <REMOTE_URL>
   ```

### Examples

#### Target 2024-2026 with 40 average commits/day (no weekends)

```bash
python contribute.py --start_date 2024-01-01 --end_date 2026-12-31 --no_weekends --max_commits 80 --frequency 100
```

## Options

- `-nw`, `--no_weekends`: Do not commit on weekends.
- `-mc`, `--max_commits`: Maximum commits per day (1-120).
- `-fr`, `--frequency`: Percentage of days to commit.
- `-r`, `--repository`: A link on an empty remote git repository.
- `-sd`, `--start_date`: Explicit start date (YYYY-MM-DD).
- `-ed`, `--end_date`: Explicit end date (YYYY-MM-DD).
- `-un`, `--user_name`: Overrides user.name git config.
- `-ue`, `--user_email`: Overrides user.email git config.
