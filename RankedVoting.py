
import numpy as np
from typing import Dict
from collections import defaultdict
from tabulate import tabulate

class RankedVoting:
    def __init__(self, show_intermediate: bool = False):
        """
        Initialize the RankedVoting instance.

        Args:
            show_intermediate (bool, optional): If True, display intermediate results. Defaults to False.
        """
        self.show_intermediate = show_intermediate
        self.candidates = []
        self.voters = {}
        self.vote_percentages = {}
        self.vote_counts = defaultdict(int)

    def initialize_votes(self) -> None:
        """
        Initialize the votes for each candidate.
        """
        self.vote_counts = defaultdict(int)

    def calculate_vote_percentages(self) -> None:
        """
        Calculate the percentages of votes received by each candidate using NumPy.

        Note: NumPy optimizations are relevant for large voter numbers.
        """
        total_votes = sum(self.vote_counts.values())
        candidates_arr = np.array(self.candidates)
        votes_arr = np.array(list(self.vote_counts.values()))
        self.vote_percentages = dict(zip(candidates_arr, (votes_arr / total_votes) * 100 if total_votes > 0 else 0))

    def is_winner_found(self) -> bool:
        """
        Check if a winner has been found (i.e., any candidate has more than 50% of the votes).

        Returns:
            bool: True if a winner is found, False otherwise.
        """
        return any(percentage > 50.0 for percentage in self.vote_percentages.values())

    def get_least_voted_candidate(self) -> str:
        """
        Get the candidate with the least votes.

        Returns:
            str: The name of the candidate with the least votes.
        """
        return min(self.vote_counts, key=self.vote_counts.get)

    def redistribute_votes(self, least_voted_candidate: str) -> None:
        """
        Redistribute votes from the candidate with the least votes to the other candidates based on preferences.

        Args:
            least_voted_candidate (str): The name of the candidate with the least votes.
        """
        for voter, preferences in self.voters.items():
            least_voted_rank = preferences.get(least_voted_candidate)
            if least_voted_rank is not None and least_voted_rank in self.candidates:
                least_voted_candidate = least_voted_rank
            else:
                least_voted_candidate = next(iter(preferences))
            self.vote_counts[least_voted_candidate] += 1

    def display_intermediate_results(self, percentages: Dict[str, float]) -> None:
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

    def display_final_results(self, percentages: Dict[str, float]) -> None:
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