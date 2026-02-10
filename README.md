# Generative-AI

A Python script to generate a historical contribution graph on GitHub.

## Features

- Custom contribution frequency.
- Option to exclude weekends.
- Specify historical start and end dates.
- Automatic repository synchronization.
- 100% Emoji Free.

## Usage

1. Clone this repository.
2. Run the script:

   ```bash
   python contribute.py --repository <REMOTE_URL>
   ```

## Options

- `-nw`, `--no_weekends`: Do not commit on weekends.
- `-mc`, `--max_commits`: Maximum commits per day (1-20).
- `-fr`, `--frequency`: Percentage of days to commit.
- `-db`, `--days_before`: Number of days before today to start.
- `-da`, `--days_after`: Number of days after today to end.
