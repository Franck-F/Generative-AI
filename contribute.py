#!/usr/bin/env python
import argparse
import os
from datetime import datetime
from datetime import timedelta
from random import randint
import subprocess
import sys


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        sys.exit(f"Error: Invalid date format for '{date_str}'. Use YYYY-MM-DD.")


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        if end == -1 or end <= start:
            directory = repository[start:]
        else:
            directory = repository[start:end]
    no_weekends = args.no_weekends
    frequency = args.frequency

    if args.start_date:
        start_date = parse_date(args.start_date).replace(hour=20, minute=0)
    else:
        start_date = curr_date.replace(hour=20, minute=0) - timedelta(args.days_before)

    if args.end_date:
        end_date = parse_date(args.end_date).replace(hour=20, minute=0)
    else:
        end_date = curr_date.replace(hour=20, minute=0) + timedelta(args.days_after)

    if start_date > end_date:
        sys.exit('Error: start_date must be before end_date')

    if not os.path.exists(directory):
        os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    delta = end_date - start_date
    for n in range(delta.days + 1):
        day = start_date + timedelta(days=n)
        if (not no_weekends or day.weekday() < 5) \
                and randint(0, 100) < frequency:
            for commit_time in (day + timedelta(minutes=m)
                                for m in range(contributions_per_day(args))):
                contribute(commit_time)

    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    # Return to original directory to avoid test issues
    os.chdir('..')
    print('\nRepository generation completed successfully!')


def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    subprocess.run(commands, check=True, capture_output=True)


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    max_c = args.max_commits
    if max_c > 120:
        max_c = 120
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends',
                        required=False, action='store_true', default=False,
                        help="""do not commit on weekends""")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        required=False, help="""Defines the maximum amount of
                        commits a day the script can make. Accepts a number
                        from 1 to 120. If N is specified the script commits
                        from 1 to N times a day. The exact number of commits
                        is defined randomly for each day. The default value
                        is 10.""")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        required=False, help="""Percentage of days when the
                        script performs commits. If N is specified, the script
                        will commit N%% of days in a year. The default value
                        is 80.""")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link on an empty remote git repository.""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.""")
    parser.add_argument('-db', '--days_before', type=int, default=365,
                        required=False, help="""Specifies the number of days
                        before the current date when the script will start
                        adding commits.""")
    parser.add_argument('-da', '--days_after', type=int, default=0,
                        required=False, help="""Specifies the number of days
                        after the current date until which the script will be
                        adding commits.""")
    parser.add_argument('-sd', '--start_date', type=str, required=False,
                        help="""Explicit start date in YYYY-MM-DD format.
                        Overrides --days_before.""")
    parser.add_argument('-ed', '--end_date', type=str, required=False,
                        help="""Explicit end date in YYYY-MM-DD format.
                        Overrides --days_after.""")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
