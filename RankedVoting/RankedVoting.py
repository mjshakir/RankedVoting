from typing import Dict, List
import tabulate
import numpy as np


class RankedVoting:
    def __init__(self, candidates: List[str], voters_data: dict):
        self.candidates = {candidate: 0 for candidate in candidates}
        self.voters = voters_data
        self.percentage_movement = []

    def add_candidate(self, candidate_name: str) -> None:
        """
        Add a candidate to the ranked voting system.
        """
        if not candidate_name or not isinstance(candidate_name, str):
            raise ValueError("Candidate name should be a non-empty string.")

        if candidate_name not in self.candidates:
            self.candidates[candidate_name] = 0

    def add_candidates(self, candidates_data: set) -> None:
        for candidate in candidates_data:
            self.candidates[candidate] = 0

    def get_candidate_percentage(self, candidate_name: str) -> float:
        total_votes = np.sum(list(self.candidates.values()))
        if total_votes == 0:
            return 0.0
        return self.candidates[candidate_name] / total_votes * 100

    def calculate_vote_counts(self) -> Dict[str, int]:
        vote_counts = {candidate: 0 for candidate in self.candidates}

        for voter_preferences in self.voters.values():
            # Sanitize preferences
            sanitized_preferences = {}
            for candidate, preference in voter_preferences.items():
                if isinstance(preference, int):
                    sanitized_preferences[candidate] = preference
                else:
                    sanitized_preferences[candidate] = 0  # Treat non-integer preferences as 0

            # Count number of occurrences for each preference
            preference_counts = {}
            for preference in sanitized_preferences.values():
                if preference in preference_counts:
                    preference_counts[preference] += 1
                else:
                    preference_counts[preference] = 1

            # Filter out candidates with a preference of 0 or non-unique preference
            unique_preferences = {candidate: preference for candidate, preference in sanitized_preferences.items()
                                if preference != 0 and preference_counts[preference] == 1}

            if unique_preferences:
                top_preference = min(unique_preferences, key=unique_preferences.get)
                vote_counts[top_preference] += 1

        return vote_counts


    def calculate_vote_percentages(self, local_candidates):
        total_votes = np.sum(list(local_candidates.values()))
        vote_percentages = {candidate: (votes/total_votes) * 100 for candidate, votes in local_candidates.items()}
        return vote_percentages


    def _get_winner(self) -> str:
        vote_counts = self.calculate_vote_counts()
        total_votes = np.sum(list(vote_counts.values()))
        for candidate, votes in vote_counts.items():
            if np.divide(votes, total_votes) > 0.5:
                return candidate
        return ""

    def add_vote(self, ranked_preferences: Dict[str, int]) -> None:
        if not ranked_preferences or not isinstance(ranked_preferences, dict):
            raise ValueError("Ranked preferences should be a non-empty dictionary.")

        if len(ranked_preferences) != len(self.candidates):
            raise ValueError("Ranked preferences should have preferences for all candidates.")

        # Check for invalid preferences
        for preference in ranked_preferences.values():
            if not preference or list(ranked_preferences.values()).count(preference) > 1:
                raise ValueError("Invalid voter preferences. No preference should be 0, blank, or duplicated.")

        voter_id = f"Voter {len(self.voters) + 1}"
        self.voters[voter_id] = ranked_preferences


    def add_voters(self, voters_data: Dict[str, Dict[str, int]]) -> None:
        if not voters_data or not isinstance(voters_data, dict):
            raise ValueError("Voters data should be a non-empty dictionary.")
        self.voters = {**self.voters, **voters_data}  # Merge dictionaries

    def find_candidate_with_least_votes(self) -> str:
        if not self.candidates:
            return ""

        min_votes = min(self.candidates.values())
        candidates_with_min_votes = [candidate for candidate, votes in self.candidates.items() if votes == min_votes]
        return candidates_with_min_votes[0] if candidates_with_min_votes else ""

    def find_candidates_with_least_votes(self, candidates=None) -> List[str]:
        if not candidates:
            candidates = self.candidates
        if not candidates:
            return []

        min_votes = min(candidates.values())
        candidates_with_min_votes = [candidate for candidate, votes in candidates.items() if votes == min_votes]
        return candidates_with_min_votes

    def remove_candidate(self, candidate: str) -> None:
        """Remove a candidate from all voter preferences."""
        for voter in self.voters:
            if candidate in self.voters[voter]:
                del self.voters[voter][candidate]

    def redistribute_votes(self, candidates_to_remove: List[str]) -> None:
        while candidates_to_remove:
            candidate_to_remove = candidates_to_remove.pop(0)
            if candidate_to_remove in self.candidates:
                del self.candidates[candidate_to_remove]
                # instead of simply removing the candidate, redistribute their votes
                for voter, preferences in self.voters.items():
                    if preferences.get(candidate_to_remove) is not None:
                        del preferences[candidate_to_remove]
                        # sort the preferences based on ranking after deleting
                        preferences = dict(sorted(preferences.items(), key=lambda item: item[1]))
                        # increment vote count for the new top preferred candidate
                        top_preference = next(iter(preferences))
                        self.candidates[top_preference] += 1

            # Recalculate the vote counts
            self.candidates = self.calculate_vote_counts()

            # Check if a winner is found
            winner = self._get_winner()
            if winner:
                break

            # If no winner, remove the next least voted candidates
            candidates_to_remove = self.find_candidates_with_least_votes()

            # Update the percentage movement
            vote_percentages = self.calculate_vote_percentages(self.candidates)
            self.percentage_movement.append(vote_percentages)




    def _get_least_voted_candidate(self) -> str:
        """
        Get the candidate with the least number of votes.
        """
        return min(self.candidates, key=self.candidates.get, default="")

    def show_initial_percentages(self) -> str:
        table_data = []
        headers = ['Candidate', 'Initial Votes', 'Initial Percentage']
        total_votes = len(self.voters)  # each voter has one vote

        vote_counts = self.calculate_vote_counts()

        for candidate, votes in vote_counts.items():
            percentage = votes / total_votes * 100 if total_votes > 0 else 0
            row = [candidate, votes, f"{percentage:.2f}%"]
            table_data.append(row)

        # Sort the table data by votes in descending order
        table_data.sort(key=lambda x: x[1], reverse=True)

        print("\nInitial vote counts and percentages for each candidate:")
        print("----------------------------------------------------------")
        return tabulate.tabulate(table_data, headers=headers, tablefmt="grid")

    def show_percentage_movement(self):
        headers = ['Round', 'Dropped Candidate', 'Remaining Candidates', 'Votes', 'Percentage']
        table_data = []

        dropped_candidates = []

        for i, percentages in enumerate(self.percentage_movement):
            vote_counts = self.calculate_vote_counts()

            # Find the candidates dropped in this round
            current_candidates = set(self.candidates.keys())
            dropped_in_this_round = [candidate for candidate in dropped_candidates if candidate not in current_candidates]
            dropped_candidates.extend(dropped_in_this_round)

            for candidate in self.candidates.keys():
                if candidate in dropped_in_this_round:
                    row = [f"Round {i + 1}", candidate, "Dropped", "-", "-"]
                else:
                    row = [f"Round {i + 1}", "", candidate, vote_counts[candidate], f"{percentages[candidate]:.2f}%"]
                table_data.append(row)

        # Sort the table data by round and votes in descending order
        table_data.sort(key=lambda x: (x[0], -x[3] if x[3] != "-" else 0))

        print("\nVote counts and percentages movement for each candidate by round:")
        print("----------------------------------------------------------------------")
        print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))



    def show_final_result(self, winner=None):
        table_data = []
        headers = ['Candidate', 'Percentage']
        total_votes = len(self.voters)
        for candidate, votes in self.calculate_vote_counts().items():
            percentage = votes / total_votes * 100 if total_votes > 0 else 0
            row = [candidate, f"{percentage:.2f}%"]
            table_data.append(row)
        print("Final Result:")
        print(tabulate.tabulate(table_data, headers=headers))

        if winner:
            print(f"The winner is {winner}!")
        else:
            print("No candidate reached 50% of the votes. A runoff election may be needed.")

    def run_ranked_voting(self):
        # Show initial percentages
        print("Initial Percentages:")
        print(self.show_initial_percentages())

        while True:
            vote_counts = self.calculate_vote_counts()
            vote_percentages = self.calculate_vote_percentages(vote_counts)
            self.percentage_movement.append(vote_percentages)

            # Check if we have a winner
            winner = self._get_winner()
            if winner:
                print(f"\n\nThe winner is {winner} with {self.candidates[winner]} votes!")
                break

            # Find least voted candidate(s) and remove them
            least_voted_candidates = self.find_candidates_with_least_votes(self.candidates)
            if least_voted_candidates:
                self.redistribute_votes(least_voted_candidates)  # Pass a list of candidates

            # Check if we have a winner after redistribution
            winner = self._get_winner()
            if winner:
                print(f"\n\nThe winner is {winner} with {self.candidates[winner]} votes!")
                break

        # Show percentage movement
        self.show_percentage_movement()