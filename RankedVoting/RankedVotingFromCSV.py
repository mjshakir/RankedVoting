import RankedVoting
import csv
from typing import Dict, Tuple

class RankedVotingFromCSV(RankedVoting):
    def __init__(self, csv_file: str, show_intermediate: bool = False):
        """
        Initialize the RankedVotingFromCSV instance.

        Args:
            csv_file (str): Path to the CSV file containing the candidates and voters' preferences.
            show_intermediate (bool, optional): If True, display intermediate results. Defaults to False.
        """
        super().__init__(show_intermediate)
        self.csv_file = csv_file

    def load_candidates(self) -> None:
        """
        Load the candidates' names from the first row of the CSV file.
        """
        with open(self.csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            self.candidates = next(csv_reader)[1:]

    def load_voters(self) -> None:
        """
        Load voters' preferences from the CSV file.

        Ensure that voters are unique based on their names.
        """
        voter_names_set = set()
        with open(self.csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the first row (candidates' names)
            for row in csv_reader:
                voter_name = row[0]
                if voter_name not in voter_names_set:
                    voter_names_set.add(voter_name)
                    preferences = {self.candidates[i]: int(rank) for i, rank in enumerate(row[1:])}
                    self.voters[voter_name] = preferences

    def run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
        """
        Run the ranked voting calculations using preferences from the CSV file.

        Returns:
            Tuple[Dict[str, float], str]: A tuple containing a dictionary mapping each candidate name to the percentage
            of votes received, and the winning candidate.
        """
        self.load_candidates()
        self.load_voters()
        self._calculate_vote_percentages()
        self._find_winner()

