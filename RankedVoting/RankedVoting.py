import numpy as np
from typing import List, Dict
from tabulate import tabulate

class RankedVoting:
    """
    A class representing a Ranked Voting system.

    Attributes:
        show_intermediate (bool): If True, display intermediate results. Defaults to False.
        candidates (List[str]): List of candidate names.
        voters (Dict[str, Dict[str, int]]): Dictionary of voters and their preferences in the format {voter_name: {candidate_name: rank}}.
        vote_percentages (Dict[str, float]): Dictionary of candidates and their respective vote percentages.
        vote_counts (Dict[str, int]): Dictionary of candidates and their total vote counts.

    Methods:
        _calculate_vote_percentages(self) -> None:
            Calculate the percentages of votes received by each candidate using NumPy.

        _is_winner_found(self) -> bool:
            Check if a winner has been found (i.e., any candidate has more than 50% of the votes).

        _redistribute_votes(self, least_voted_candidate: str) -> None:
            Redistribute votes from the candidate with the least votes to all candidates with equal ranks.

        _find_winner(self) -> str:
            Find the winner of the ranked voting.

        display_intermediate_results(self, percentages: Dict[str, float]) -> None:
            Displays intermediate voting results.

        display_final_results(self, percentages: Dict[str, float]) -> None:
            Displays final voting results and highlights the winning candidate.
    """
    def __init__(self, show_intermediate: bool = False):
        """
        Initialize the RankedVoting instance.

        Args:
            show_intermediate (bool, optional): If True, display intermediate results. Defaults to False.
        """
        self.show_intermediate = show_intermediate
        self.candidates: List[str] = []
        self.voters: Dict[str, Dict[str, int]] = {}
        self.vote_percentages: Dict[str, float] = {}
        self.vote_counts: Dict[str, int] = {}

    def _calculate_vote_percentages(self) -> None:
        """
        Calculate the percentages of votes received by each candidate using NumPy.

        Note: NumPy optimizations are relevant for large voter numbers.
        """
        total_votes = sum(self.vote_counts.values())
        candidates_arr = np.array(self.candidates)
        votes_arr = np.array(list(self.vote_counts.values()))
        self.vote_percentages = dict(zip(candidates_arr, (votes_arr / total_votes) * 100 if total_votes > 0 else 0))

    def _is_winner_found(self) -> bool:
        """
        Check if a winner has been found (i.e., any candidate has more than 50% of the votes).

        Returns:
            bool: True if a winner is found, False otherwise.
        """
        return any(percentage > 50.0 for percentage in self.vote_percentages.values())

    def _redistribute_votes(self, least_voted_candidate: str) -> None:
        """
        Redistribute votes from the candidate with the least votes to all candidates with equal ranks.

        Args:
            least_voted_candidate (str): The name of the candidate with the least votes.
        """
        for voter, preferences in self.voters.items():
            least_voted_rank = preferences.get(least_voted_candidate)
            if least_voted_rank is not None and least_voted_rank in self.candidates:
                # Get all candidates with equal ranks
                equal_ranks_candidates = [candidate for candidate, rank in preferences.items() if rank == least_voted_rank]

                # Calculate the number of votes to redistribute equally among candidates with equal ranks
                votes_to_redistribute = 1 / len(equal_ranks_candidates)

                # Redistribute votes to all candidates with equal ranks
                for candidate in equal_ranks_candidates:
                    self.vote_counts[candidate] += votes_to_redistribute

    def _find_winner(self) -> str:
        """
        Find the winner of the ranked voting.

        Returns:
            str: The name of the winning candidate.
        """
        while not self._is_winner_found():
            least_voted_candidate = self._get_least_voted_candidate()
            self._redistribute_votes(least_voted_candidate)

        return max(self.vote_percentages, key=self.vote_percentages.get)

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
