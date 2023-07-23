import os
import pandas as pd
from typing import Dict, List, Tuple
from RankedVoting import RankedVoting


class RankedVotingFromCSV(RankedVoting):
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.candidates, self.voters_data = self._load_from_csv()
        super().__init__(self.candidates, self.voters_data)

    def _sanitize_rank(self, rank: str, max_rank: int) -> int:
        if pd.isnull(rank) or not str(rank).strip().replace(".", "").isdigit():
            return 0
        if "." in str(rank):
            rank_value = round(float(rank))  # Round float rank to the nearest integer
        else:
            rank_value = int(rank)
        return 0 if rank_value > max_rank else rank_value  # If rank is higher than the number of candidates, assign 0

    def _load_from_csv(self) -> Tuple[List[str], Dict[str, Dict[str, int]]]:
        if not os.path.isfile(self.csv_file):
            raise ValueError(f"File {self.csv_file} does not exist. Please ensure that your CSV file path is correct.")

        df = pd.read_csv(self.csv_file)
        candidates = df.columns.tolist()[1:]  # Get the candidate names
        max_rank = len(candidates)  # Maximum rank allowed

        voters_data = {}
        for _, row in df.iterrows():
            voter_name = row[0]
            preferences = {candidates[i]: self._sanitize_rank(rank, max_rank) for i, rank in enumerate(row[1:])}

            if voter_name in voters_data:
                if voters_data[voter_name] == preferences:
                    print(f"Warning: Duplicate voter found: {voter_name}. Only counting once.")
                else:
                    print(f"Warning: Conflict detected! Different preferences found for the same voter ({voter_name}). Ignoring the latter entry.")
                    continue
            voters_data[voter_name] = preferences
        return candidates, voters_data

