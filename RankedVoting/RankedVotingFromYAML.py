from RankedVoting import RankedVoting
import os
import yaml
from typing import Tuple, List, Dict


class RankedVotingFromYAML(RankedVoting):
    """
    A class for conducting ranked voting calculations based on voter preferences provided in YAML files.

    Attributes:
        main_folder (str): Path to the main folder containing candidate.yaml and voter YAML files.
        candidates (List[str]): List of candidate names.
        voters (Dict[str, Dict[str, int]]): Dictionary of voters and their preferences in the format {voter_name: {candidate_name: rank}}.
        show_intermediate (bool): Flag to determine whether to display intermediate results during the ranked voting process.
    
    Methods:
        __init__(self, main_folder: str, show_intermediate: bool = False):
            Constructs a RankedVotingFromYAML instance.

        load_candidates(self) -> None:
            Loads the candidate names from the candidates.yaml file.

        load_voters(self) -> None:
            Loads the voter preferences from the voter YAML files.

        run_ranked_voting(self) -> None:
            Executes the ranked voting process using voter preferences and determines the winner.

    """

    def __init__(self, main_folder: str, show_intermediate: bool = False):
        """
        Constructs a RankedVotingFromYAML instance.

        Args:
            main_folder (str): Path to the main folder containing candidate.yaml and voter YAML files.
            show_intermediate (bool, optional): Flag to determine whether to display intermediate results during the ranked voting process. Default is False.

        Returns:
            None
        """
        super().__init__(show_intermediate)
        self.main_folder = main_folder

    def load_candidates(self) -> None:
        """
        Loads the candidate names from the candidates.yaml file.

        Args:
            None

        Returns:
            None
        """
        candidates_file = os.path.join(self.main_folder, "candidates.yaml")
        with open(candidates_file, "r") as file:
            self.candidates = yaml.safe_load(file)

    def load_voters(self) -> None:
        """
        Loads the voter preferences from the voter YAML files.

        Args:
            None

        Returns:
            None
        """
        voter_files = [file for file in os.listdir(self.main_folder) if
                       file.startswith("voter") and file.endswith(".yaml")]
        for voter_file in voter_files:
            voter_path = os.path.join(self.main_folder, voter_file)
            with open(voter_path, "r") as file:
                voter_data = yaml.safe_load(file)
                voter_name = voter_data[0]["Voter"]
                self.voters[voter_name] = voter_data[0]

    def run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
        """
        Run the ranked voting calculations using preferences from the YAML file.

        Returns:
            Tuple[Dict[str, float], str]: A tuple containing a dictionary mapping each candidate name to the percentage
            of votes received, and the winning candidate.
        """
        self.load_candidates()
        self.load_voters()
        return self._run_ranked_voting()
