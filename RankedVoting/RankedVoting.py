from typing import Dict, List
import tabulate


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
        """
        Get the percentage of votes for a specific candidate.
        """
        total_votes = sum(self.candidates.values())
        if total_votes == 0:
            return 0.0
        return self.candidates[candidate_name] / total_votes * 100

    def calculate_vote_counts(self) -> Dict[str, int]:
        # Initialize a dictionary to count the votes for each candidate
        vote_counts = {candidate: 0 for candidate in self.candidates}

        # For each voter, find their top preference and increment the vote count for that candidate
        for voter_preferences in self.voters.values():
            # Filter out candidates with a preference of 0 or non-unique preference
            non_zero_unique_preferences = {candidate: preference for candidate, preference in voter_preferences.items()
                                        if preference != 0 and list(voter_preferences.values()).count(preference) == 1}

            if non_zero_unique_preferences:  # Check that there are non-zero unique preferences
                top_preference = min(non_zero_unique_preferences, key=non_zero_unique_preferences.get)
                vote_counts[top_preference] += 1

        return vote_counts

    def calculate_vote_percentages(self, local_candidates):
        total_votes = sum(local_candidates.values())
        vote_percentages = {candidate: (votes/total_votes) * 100 for candidate, votes in local_candidates.items()}
        return vote_percentages


    def _get_winner(self) -> str:
        vote_counts = self.calculate_vote_counts()
        total_votes = sum(vote_counts.values())
        for candidate, votes in vote_counts.items():
            if votes / total_votes > 0.5:
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
        """Redistribute votes from the least voted candidates until a winner is found or all candidates are removed."""

        while candidates_to_remove:
            candidate_to_remove = candidates_to_remove.pop(0)
            if candidate_to_remove in self.candidates:
                del self.candidates[candidate_to_remove]
                self.remove_candidate(candidate_to_remove)

            # Recalculate the vote counts
            self.candidates = self.calculate_vote_counts()

            # Check if a winner is found
            winner = self._get_winner()
            if winner:
                print(f"\n\nThe winner is {winner} with {self.candidates[winner]} votes!")
                break

            # If no winner, remove the next least voted candidates
            candidates_to_remove = self.find_candidates_with_least_votes()
            if not candidates_to_remove:
                print("\n\nNo candidate reached 50% of the votes. A runoff election may be needed.")

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
        headers = ['Candidate', 'Initial Percentage']
        total_votes = len(self.voters)  # each voter has one vote

        vote_counts = self.calculate_vote_counts()

        for candidate, votes in vote_counts.items():
            percentage = votes / total_votes * 100 if total_votes > 0 else 0
            row = [candidate, f"{percentage:.2f}%"]
            table_data.append(row)

        return tabulate.tabulate(table_data, headers=headers)



    def show_percentage_movement(self):
        headers = ['Round'] + list(self.candidates.keys())
        table_data = []

        for i, percentages in enumerate(self.percentage_movement):
            row = [f"Round {i + 1}"]
            for candidate in self.candidates.keys():
                row.append(f"{percentages[candidate]:.2f}%")
            table_data.append(row)

        print("Percentage Movement:")
        print(tabulate.tabulate(table_data, headers=headers))

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
                print(f"The winner is {winner}!")
                break

            # Find least voted candidate(s) and remove them
            least_voted_candidates = self.find_candidates_with_least_votes(self.candidates)
            if least_voted_candidates:
                self.redistribute_votes(least_voted_candidates)  # Pass a list of candidates

            # Check if we have a winner after redistribution
            winner = self._get_winner()
            if winner:
                print(f"The winner is {winner}!")
                break

        # Show percentage movement
        self.show_percentage_movement()

