from pathlib import Path
import yaml
from RankedVoting import RankedVoting


class RankedVotingFromYAML(RankedVoting):
    def __init__(self, main_folder, candidates_file="candidates.yaml"):
        self.main_folder = Path(main_folder)
        self.candidates_file = self.main_folder / candidates_file
        self.voters_folder = self.main_folder / "voters"
        if not self.candidates_file.is_file() or not self.voters_folder.is_dir():
            raise FileNotFoundError(
                "Cannot find candidates file or voters folder. "
                "Please make sure your folder structure is as follows: \n"
                "main_folder\n"
                "├── candidates_file.yaml\n"
                "└── voters\n"
                "    ├── voter1.yaml\n"
                "    ├── voter2.yaml\n"
                "    └── ..."
            )
        self.candidates = self.load_candidates()
        self.voters = self.load_voters()
        super().__init__(self.candidates, self.voters)

    def load_candidates(self):
        with open(self.candidates_file, 'r') as file:
            candidates = yaml.safe_load(file)
        return {candidate: 0 for candidate in candidates}

    def _sanitize_rank(self, preferences):
        number_of_candidates = len(self.candidates)
        sanitized = {}
        for candidate, rank in preferences.items():
            if not isinstance(rank, (int, float)) or rank < 1 or rank > number_of_candidates:
                sanitized[candidate] = 0
            else:
                sanitized[candidate] = round(rank)
        return sanitized

    def load_voters(self):
        voters = {}
        for voter_file in self.voters_folder.iterdir():
            with open(voter_file, 'r') as file:
                voter_data = yaml.safe_load(file)
                for voter_name, raw_preferences in voter_data.items():
                    preferences = self._sanitize_rank(raw_preferences)
                    if voter_name in voters:
                        if voters[voter_name] == preferences:
                            print(f"Duplicate voter found: {voter_name}. Counting once.")
                        else:
                            print(f"Conflict! Different preferences for same voter ({voter_name}). Ignoring.")
                            continue
                    voters[voter_name] = preferences
        return voters