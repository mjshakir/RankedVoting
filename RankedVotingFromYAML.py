import RankedVoting
import yaml
from typing import Dict, Tuple, List

class RankedVotingFromYAML(RankedVoting):
    def __init__(self, candidates_file: str, voter_files: List[str], show_intermediate: bool = False):
        """
        Initialize the RankedVotingFromYAML instance.

        Args:
            candidates_file (str): Path to the YAML file containing the names of the candidates.
            voter_files (List[str]): List of paths to the YAML files containing the voters' preferences.
            show_intermediate (bool, optional): If True, display intermediate results. Defaults to False.
        """
        super().__init__(show_intermediate)
        self.candidates_file = candidates_file
        self.voter_files = voter_files

    def load_candidates(self) -> None:
        """
        Load the candidates' names from the YAML file.
        """
        with open(self.candidates_file, 'r') as file:
            self.candidates = yaml.safe_load(file)
            
    def load_voters(self, remove_candidate_is_dont_care: bool = True) -> None:
        """
        Load voters' preferences from the YAML files.

        Args:
            remove_candidate_is_dont_care (bool, optional): If True, treat the removal of a candidate as a "don't care" value.
                If False, treat the removal as a strict preference against the candidate. Defaults to True.
        """
        candidate_set = set(self.candidates)
        for file in self.voter_files:
            with open(file, 'r') as voter_file:
                voter_data = yaml.safe_load(voter_file)
                voter_name = voter_data.pop('Voter')
                preferences = {}
                for candidate, rank in voter_data.items():
                    if candidate in candidate_set:
                        preferences[candidate] = rank
                    elif not remove_candidate_is_dont_care:
                        # If the candidate is removed and remove_candidate_is_dont_care is False,
                        # treat it as a strict preference against the candidate (do not include in preferences).
                        self.vote_counts[candidate] += 1
                self.voters[voter_name] = preferences

    def run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
        """
        Run the ranked voting calculations using preferences from YAML files.

        Returns:
            Tuple[Dict[str, float], str]: A tuple containing a dictionary mapping each candidate name to the percentage
            of votes received, and the winning candidate.
        """
        self.load_candidates()
        self.load_voters()
        super().run_ranked_voting()