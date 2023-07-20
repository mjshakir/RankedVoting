import argparse
from ranked_voting import RankedVoting
from typing import Dict, Tuple, Optional

def main() -> None:
    parser = argparse.ArgumentParser(description='Ranked Voting')
    parser.add_argument('csv_file', help='Path to the CSV file (without the .csv extension) containing the ranked voting data')
    parser.add_argument('--show-intermediate', action='store_true', help='Show intermediate results after each round of vote redistribution')
    args = parser.parse_args()

    filename: str = args.csv_file
    if not filename.endswith('.csv'):  # Check if the user provided .csv extension; if not, raise an error
        print("Error: The file must be in .csv format.")
        exit(1)

    show_intermediate: bool = args.show_intermediate

    ranked_voting = RankedVoting(filename, show_intermediate)
    percentages, _ = ranked_voting.run_ranked_voting()

    if show_intermediate:
        ranked_voting.display_intermediate_results(percentages)

    ranked_voting.display_final_results(percentages)

    # If you don't need the percentages and winner in the main script,
    # you can ignore the return values as follows:
    # ranked_voting.run_ranked_voting()

if __name__ == "__main__":
    main()
