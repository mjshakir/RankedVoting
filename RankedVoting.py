import csv
from typing import Dict, Tuple
from tabulate import tabulate
from collections import defaultdict

class RankedVoting:
    """
    A class to perform Ranked Voting calculations based on a CSV file.

    Attributes:
        filename (str): The path to the CSV file containing the ranked voting data.
        candidates (list[str]): The list of candidate names extracted from the CSV file.
        votes (list[list[int]]): The list of votes, where each vote is represented as a list of integers.
        show_intermediate (bool): A flag to determine whether to display intermediate results.
    """
    def __init__(self, filename: str, show_intermediate: bool = False):
        """
        Initializes the RankedVoting object.

        Args:
            filename (str): The path to the CSV file containing the ranked voting data.
            show_intermediate (bool, optional): Whether to display intermediate results after each round of vote redistribution.
                                                Defaults to False.
        """
        self.filename = filename
        self.candidates = []
        self.votes = []
        self.show_intermediate = show_intermediate

    def _read_csv(self) -> None:
        """
        Reads the CSV file and extracts candidate names and voter preferences.
        """
        if not self.filename.endswith('.csv'):
            raise ValueError("Invalid file format. The file must be in .csv format.")

        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.candidates = next(reader)[1:]  # Extract candidate names from the first row (excluding the first cell)

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
                        if 0 < vote <= len(self.candidates):
                            vote_row.append(vote)
                    except ValueError:
                        pass

                self.votes.append(vote_row)

    def _count_votes(self) -> Dict[str, int]:
        """
        Counts the votes received by each candidate.

        Returns:
            Dict[str, int]: A dictionary mapping each candidate name to the total number of votes received.
        """
        vote_counts = defaultdict(int)
        for vote_row in self.votes:
            for _, candidate in enumerate(vote_row[1:], start=1):
                vote_counts[self.candidates[candidate - 1]] += 1
        return vote_counts

    def _calculate_percentages(self, vote_counts: Dict[str, int], total_votes: int) -> Dict[str, float]:
        """
        Calculates the percentage of votes received by each candidate.

        Args:
            vote_counts (Dict[str, int]): A dictionary mapping each candidate name to the total number of votes received.
            total_votes (int): The total number of votes cast.

        Returns:
            Dict[str, float]: A dictionary mapping each candidate name to the percentage of votes received.
        """
        percentages = {candidate: (votes / total_votes) * 100 for candidate, votes in vote_counts.items()}
        return percentages

    def _redistribute_votes(self, winner: str, vote_counts: Dict[str, int]) -> None:
        """
        Redistributes votes from non-winning candidates to their next preferences.

        Args:
            winner (str): The name of the winning candidate.
            vote_counts (Dict[str, int]): A dictionary mapping each candidate name to the total number of votes received.
        """
        for vote_row in self.votes:
            if vote_row[1] != winner:
                for j, candidate in enumerate(vote_row[2:], start=2):
                    if candidate == winner:
                        vote_row[1] = winner
                        vote_counts[winner] += 1
                        break

    def _find_winner(self, percentages: Dict[str, float]) -> str:
        """
        Finds the candidate with the highest percentage of votes.

        Args:
            percentages (Dict[str, float]): A dictionary mapping each candidate name to the percentage of votes received.

        Returns:
            str: The name of the winning candidate.
        """
        return max(percentages, key=percentages.get)
    
    def _display_intermediate_results(self, percentages: Dict[str, float]) -> None:
        """
        Displays intermediate voting results.

        Args:
            percentages (Dict[str, float]): A dictionary mapping each candidate name to the percentage of votes received.
        """
        print("Intermediate Results:")
        headers = ["Candidate", "Percentage"]
        table_data = [[candidate, f"{percentage:.2f}%"] for candidate, percentage in percentages.items()]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()

    def _display_final_results(self, percentages: Dict[str, float]) -> None:
        """
        Displays final voting results and highlights the winning candidate.

        Args:
            percentages (Dict[str, float]): A dictionary mapping each candidate name to the percentage of votes received.
        """
        print("Final Results:")
        headers = ["Candidate", "Percentage", "Winner"]
        table_data = []
        winner = max(percentages, key=percentages.get)
        for candidate, percentage in percentages.items():
            winner_mark = "*" if candidate == winner else ""
            table_data.append([candidate, f"{percentage:.2f}%", winner_mark])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
        """
        Performs the ranked voting calculations and returns the percentages of votes received by each candidate
        and the winning candidate.

        Returns:
            Tuple[Dict[str, float], str]: A tuple containing a dictionary mapping each candidate name to the percentage
            of votes received, and the winning candidate.
        """
        self.initialize_votes()

        while not self.is_winner_found():
            self.calculate_vote_percentages()
            if self.show_intermediate:
                self.display_intermediate_results(self.vote_percentages)

            least_voted_candidate = self.get_least_voted_candidate()
            if not least_voted_candidate:
                break

            self.redistribute_votes(least_voted_candidate)

        self.calculate_vote_percentages()
        self.display_final_results(self.vote_percentages)

        winner = max(self.vote_percentages, key=self.vote_percentages.get)
        return self.vote_percentages, winner