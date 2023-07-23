from typing import List, Dict
import pandas as pd
import json
from colorama import Fore, Style

class RankedVoting:
    def __init__(self, candidates: List[str], voters_data: Dict[str, Dict[str, int]]):
        self.candidates = {candidate: 0 for candidate in candidates}
        self.voters = voters_data
        self.vote_history = pd.DataFrame(columns=['round', 'removed', 'vote_counts'])

    def _sanitize_preferences(self, preferences: Dict[str, int]) -> Dict[str, int]:
        sanitized_preferences = {}
        max_preference = len(self.candidates)
        for candidate, preference in preferences.items():
            # Round float preferences to nearest integer
            if isinstance(preference, float):
                preference = round(preference)
            # Replace preferences that are higher than the number of candidates.yaml with 0
            if isinstance(preference, int) and preference > max_preference:
                preference = 0
            sanitized_preferences[candidate] = preference

        # Remove preferences with 0
        sanitized_preferences = {candidate: preference for candidate, preference in sanitized_preferences.items() if
                                 preference != 0}

        return sanitized_preferences

    def redistribute_votes(self, removed_candidate):
        voters_to_remove = []
        for voter, voter_preferences in self.voters.items():
            if removed_candidate in voter_preferences:
                del voter_preferences[removed_candidate]
            # Check if voter has no more preferences
            if not voter_preferences:
                voters_to_remove.append(voter)
            else:
                # Find the candidate with the next preference
                next_preference = min(voter_preferences.values())
                next_candidates = [candidate for candidate, preference in voter_preferences.items() if preference == next_preference]

                # If there is only one candidate with the next preference, assign the vote to that candidate
                if len(next_candidates) == 1:
                    candidate_to_assign = next_candidates[0]
                    self.candidates[candidate_to_assign] += 1
                else:
                    # If there are multiple candidates with the same next preference, distribute the vote equally
                    num_candidates = len(next_candidates)
                    vote_share = 1 / num_candidates
                    for candidate in next_candidates:
                        self.candidates[candidate] += vote_share

        # Remove voters with no more preferences
        for voter in voters_to_remove:
            del self.voters[voter]

    def calculate_vote_counts(self):
        vote_counts = {candidate: 0 for candidate in self.candidates}

        for voter_preferences in self.voters.values():
            sanitized_preferences = self._sanitize_preferences(voter_preferences)

            if sanitized_preferences:
                top_preference = min(sanitized_preferences, key=sanitized_preferences.get)
                vote_counts[top_preference] += 1

        return vote_counts

    def run_vote(self):
        round_number = 1
        while len(self.candidates) > 1:
            vote_counts = self.calculate_vote_counts()
            new_row = pd.DataFrame([{
                "round": round_number,
                "removed": [],
                "vote_counts": vote_counts.copy()
            }])
            self.vote_history = pd.concat([self.vote_history, new_row], ignore_index=True)

            min_votes = min(vote_counts.values())
            max_votes = max(vote_counts.values())

            # If all remaining candidates.yaml have equal votes, all of them are considered winners.
            if min_votes == max_votes:
                print("All remaining candidates.yaml have equal votes. They are all considered winners.")
                break

            min_vote_candidates = [candidate for candidate, votes in vote_counts.items() if votes == min_votes]

            for min_vote_candidate in min_vote_candidates:
                del self.candidates[min_vote_candidate]
                self.redistribute_votes(min_vote_candidate)

            self.vote_history.at[round_number - 1, "removed"] = min_vote_candidates
            round_number += 1

        # Last round where only one candidate remains
        vote_counts = self.calculate_vote_counts()
        new_row = pd.DataFrame([{
            "round": round_number,
            "removed": [],
            "vote_counts": vote_counts.copy()
        }])
        self.vote_history = pd.concat([self.vote_history, new_row], ignore_index=True)

         # Get the final winner and their total votes
        final_winner = max(vote_counts, key=vote_counts.get)
        final_winner_votes = vote_counts[final_winner]

        print("Final Results:")
        print(Fore.GREEN + '\033[1m' + f"The winner is {final_winner} with {final_winner_votes} votes!" + '\033[0m' + Style.RESET_ALL)
        print("-------------------------------")

    def display_interim_results(self):
        for idx, row in self.vote_history.iterrows():
            print(f"Round {row['round']} Results:")
            print("Vote counts:")
            print(row["vote_counts"])
            total_votes = sum(row["vote_counts"].values())
            if total_votes == 0:
                print("No votes cast.")
                continue
            print("Vote percentages:")
            vote_percentages = {candidate: (votes / total_votes) * 100 for candidate, votes in
                                row["vote_counts"].items()}
            print(vote_percentages)
            print("Removed: ", row["removed"])
            print("---------------------------")

    def save_results_to_csv(self, output_path):
        try:
            self.vote_history.to_csv(output_path)
        except Exception as e:
            print("Error saving to CSV:", str(e))

    def save_input_and_final_results(self, output_path):
        # Get the final result
        final_result = self.vote_history.loc[self.vote_history.index[-1], 'vote_counts']
        total_votes = sum(final_result.values())
        final_result_percent = {k: (v / total_votes * 100) for k, v in final_result.items()}

        # Prepare data to save
        data_to_save = {
            "candidates.yaml": self.candidates,
            "voters": self.voters,
            "final_result": final_result,
            "final_result_percent": final_result_percent
        }

        # Write to a JSON file
        with open(output_path, 'w') as f:
            for key, value in data_to_save.items():
                json.dump({key: value}, f)
                f.write('\n')
