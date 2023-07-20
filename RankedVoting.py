import csv
import argparse
from tabulate import tabulate
from typing import Dict, Tuple

class RankedVoting:
    def __init__(self, filename: str):
        self.filename = filename
        self.candidates = []
        self.votes = []

    def read_csv(self) -> None:
        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip the header row
            self.candidates = header[1:]  # Extract candidate names from the first row (excluding the first cell)
            voters = set()
            for row in reader:
                voter = row[0]
                if voter in voters:
                    raise ValueError(f"Duplicate voter found: {voter}")
                voters.add(voter)

                vote_row = [voter]
                for vote in row[1:]:
                    try:
                        vote = int(vote)
                        if vote < 0 or vote > len(self.candidates):
                            vote = 0  # Invalid preference, set to 0 (don't care)
                    except ValueError:
                        vote = 0  # Invalid preference, set to 0 (don't care)
                    vote_row.append(vote)

                self.votes.append(vote_row)

    def count_votes(self) -> Dict[str, int]:
        vote_counts = {candidate: 0 for candidate in self.candidates}
        for vote_row in self.votes:
            for candidate, vote in zip(self.candidates, vote_row[1:]):
                vote_counts[candidate] += vote
        return vote_counts

    def calculate_percentages(self, vote_counts: Dict[str, int]) -> Dict[str, float]:
        total_votes = sum(vote_counts.values())
        percentages = {candidate: (votes / total_votes) * 100 for candidate, votes in vote_counts.items()}
        return percentages

    def redistribute_votes(self, winner: str, vote_counts: Dict[str, int]) -> None:
        for vote_row in self.votes:
            if vote_row[1] != winner:
                for j, vote in enumerate(vote_row[2:], start=2):
                    if vote == winner:
                        vote_row[1] = winner
                        vote_counts[winner] += 1
                        break

    def find_winner(self, percentages: Dict[str, float]) -> str:
        return max(percentages, key=percentages.get)

    def run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
        self.read_csv()
        vote_counts = self.count_votes()
        percentages = self.calculate_percentages(vote_counts)
        winner = self.find_winner(percentages)

        while percentages[winner] < 50:
            self.redistribute_votes(winner, vote_counts)
            percentages = self.calculate_percentages(vote_counts)
            winner = self.find_winner(percentages)

        return percentages, winner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ranked Voting')
    parser.add_argument('csv_file', help='Path to the CSV file (without the .csv extension) containing the ranked voting data')
    args = parser.parse_args()

    filename = args.csv_file
    if not filename.endswith('.csv'):  # Check if the user provided .csv extension; if not, add it
        filename += '.csv'

    ranked_voting = RankedVoting(filename)
    percentages, winner = ranked_voting.run_ranked_voting()

    table_data = []
    for candidate, percentage in percentages.items():
        if candidate == winner:
            table_data.append([candidate, f"{percentage:.2f}%", "*"])
        else:
            table_data.append([candidate, f"{percentage:.2f}%", ""])

    headers = ["Candidate", "Percentage", "Winner"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
