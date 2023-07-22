# import numpy as np
# from typing import Tuple, List, Dict
# from tabulate import tabulate
#
# class RankedVoting:
#     """
#     A class representing a Ranked Voting system.
#
#     Attributes:
#         show_intermediate (bool): If True, display intermediate results. Defaults to False.
#         candidates (List[str]): List of candidate names.
#         voters (Dict[str, Dict[str, int]]): Dictionary of voters and their preferences in the format {voter_name: {candidate_name: rank}}.
#         vote_percentages (Dict[str, float]): Dictionary of candidates and their respective vote percentages.
#         vote_counts (Dict[str, int]): Dictionary of candidates and their total vote counts.
#
#     Methods:
#         _calculate_vote_percentages(self) -> None:
#             Calculate the percentages of votes received by each candidate using NumPy.
#
#         _is_winner_found(self) -> bool:
#             Check if a winner has been found (i.e., any candidate has more than 50% of the votes).
#
#         _redistribute_votes(self, least_voted_candidate: str) -> None:
#             Redistribute votes from the candidate with the least votes to all candidates with equal ranks.
#
#         _find_winner(self) -> str:
#             Find the winner of the ranked voting.
#
#         _run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
#             Run the ranked voting calculations and determine the winner.
#
#         display_intermediate_results(self, percentages: Dict[str, float]) -> None:
#             Displays intermediate voting results.
#
#         display_final_results(self, percentages: Dict[str, float]) -> None:
#             Displays final voting results and highlights the winning candidate.
#     """
#     def __init__(self, show_intermediate: bool = False):
#         """
#         Initialize the RankedVoting instance.
#
#         Args:
#             show_intermediate (bool, optional): If True, display intermediate results. Defaults to False.
#         """
#         self.show_intermediate = show_intermediate
#         self.candidates: List[str] = []
#         self.voters: Dict[str, Dict[str, int]] = {}
#         self.vote_percentages: Dict[str, float] = {}
#         self.vote_counts: Dict[str, int] = {}
#
#     def _calculate_vote_percentages(self) -> None:
#         """
#         Calculate the percentages of votes received by each candidate using NumPy.
#
#         Note: NumPy optimizations are relevant for large voter numbers.
#         """
#         total_votes = sum(self.vote_counts.values())
#         if total_votes == 0:
#             self.vote_percentages = {candidate: 0 for candidate in self.candidates}
#         else:
#             candidates_arr = np.array(self.candidates)
#             votes_arr = np.array(list(self.vote_counts.values()))
#             self.vote_percentages = dict(zip(candidates_arr, (votes_arr / total_votes) * 100))
#
#     def _is_winner_found(self) -> bool:
#         """
#         Check if a winner has been found (i.e., any candidate has more than 50% of the votes).
#
#         Returns:
#             bool: True if a winner is found, False otherwise.
#         """
#         return any(percentage > 50.0 for percentage in self.vote_percentages.values())
#
#     def _get_least_voted_candidate(self) -> str:
#         """
#         Get the candidate with the least votes.
#
#         Returns:
#             str: The name of the candidate with the least votes.
#         """
#         if not self.vote_counts:
#             return self.candidates[0]  # Return any candidate when there are no votes
#
#         return min(self.vote_counts, key=self.vote_counts.get)
#
#     def _redistribute_votes(self, least_voted_candidate: str) -> None:
#         """
#         Redistribute votes from the candidate with the least votes to all candidates with equal ranks.
#
#         Args:
#             least_voted_candidate (str): The name of the candidate with the least votes.
#         """
#         if not self.vote_counts:
#             return  # No votes, nothing to redistribute
#
#         least_votes = min(self.vote_counts.values())
#         least_voted_candidates = [candidate for candidate, votes in self.vote_counts.items() if votes == least_votes]
#
#         # Remove the candidate with the least votes from the vote_counts before redistribution
#         for candidate in least_voted_candidates:
#             del self.vote_counts[candidate]
#
#         for voter, preferences in self.voters.items():
#             least_voted_ranks = [rank for candidate, rank in preferences.items() if candidate in least_voted_candidates]
#             if least_voted_ranks:
#                 # Calculate the total number of votes to redistribute equally among candidates with equal ranks
#                 total_votes_to_redistribute = least_votes / len(least_voted_ranks)
#
#                 # Redistribute votes to all candidates with equal ranks
#                 for candidate, rank in preferences.items():
#                     if rank in least_voted_ranks:
#                         self.vote_counts[candidate] += total_votes_to_redistribute
#
#         # Reset the vote count of the least voted candidate to 0 after redistribution
#         for candidate in least_voted_candidates:
#             self.vote_counts[candidate] = 0
#
#     def _find_winner(self) -> str:
#         """
#         Find the winner of the ranked voting.
#
#         Returns:
#             str: The name of the winning candidate.
#         """
#         while not self._is_winner_found():
#             least_voted_candidate = self._get_least_voted_candidate()
#             self._redistribute_votes(least_voted_candidate)
#
#         return max(self.vote_percentages, key=self.vote_percentages.get)
#
#     def _find_winner_with_ties_handling(self) -> str:
#         """
#         Find the winner of the ranked voting with proper tie handling.
#
#         Returns:
#             str: The name of the winning candidate.
#         """
#         while not self._is_winner_found():
#             least_voted_candidate = self._get_least_voted_candidate()
#             self._redistribute_votes(least_voted_candidate)
#
#         return self._get_winner_with_ties()
#
#     def _get_winner_with_ties(self) -> str:
#         """
#         Get the winner with proper tie handling.
#
#         Returns:
#             str: The name of the winning candidate.
#         """
#         max_percentage = max(self.vote_percentages.values())
#         winners = [candidate for candidate, percentage in self.vote_percentages.items() if percentage == max_percentage]
#         if len(winners) == 1:
#             return winners[0]
#         else:
#             # Handle tie by choosing the candidate with the most first-choice votes
#             return max(winners, key=lambda candidate: self.vote_counts[candidate])
#
#     def _run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
#         """
#         Run the ranked voting calculations and determine the winner.
#
#         Returns:
#             Tuple[Dict[str, float], str]: A tuple containing a dictionary mapping each candidate name to the percentage
#             of votes received and the winning candidate.
#         """
#         self._calculate_vote_percentages()
#         winner = self._find_winner()
#         return self.vote_percentages, winner
#
#     # def _run_ranked_voting_with_ties_handling(self) -> Tuple[Dict[str, float], str]:
#     #     """
#     #     Run the ranked voting calculations and determine the winner, handling ties.
#     #
#     #     Returns:
#     #         Tuple[Dict[str, float], str]: A tuple containing a dictionary mapping each candidate name to the percentage
#     #         of votes received and the winning candidate, or None if there is a tie.
#     #     """
#     #     MAX_ITERATIONS = 1000  # Set a maximum number of iterations to prevent infinite loops
#     #     for _ in range(MAX_ITERATIONS):
#     #         self._calculate_vote_percentages()
#     #         if self._is_winner_found():
#     #             return self.vote_percentages, self._find_winner()
#     #
#     #         least_voted_candidate = self._get_least_voted_candidate()
#     #         prev_vote_counts = dict(self.vote_counts)  # Make a copy of current vote counts
#     #
#     #         self._redistribute_votes(least_voted_candidate)
#     #
#     #         # Check if vote counts have changed after redistribution
#     #         if self.vote_counts == prev_vote_counts:
#     #             # If vote counts remain the same, it means there is a tie
#     #             return self.vote_percentages, None
#     #
#     #     # If we reach this point, it means the loop exceeded the maximum number of iterations
#     #     raise Exception("Maximum number of iterations reached. Unable to determine a winner due to potential tie.")
#         self._calculate_vote_percentages()
#         winner = self._find_winner_with_ties_handling()
#         return self.vote_percentages, winner
#
#     def display_intermediate_results(self, percentages: Dict[str, float]) -> None:
#         """
#         Displays intermediate voting results.
#
#         Args:
#             percentages (Dict[str, float]): A dictionary mapping each candidate name to the percentage of votes received.
#         """
#         print("Intermediate Results:")
#         headers = ["Candidate", "Percentage"]
#         table_data = [[candidate, f"{percentage:.2f}%"] for candidate, percentage in percentages.items()]
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))
#         print()
#
#     def display_final_results(self, percentages: Dict[str, float]) -> None:
#         """
#         Displays final voting results and highlights the winning candidate.
#
#         Args:
#             percentages (Dict[str, float]): A dictionary mapping each candidate name to the percentage of votes received.
#         """
#         print("Final Results:")
#         headers = ["Candidate", "Percentage", "Winner"]
#         table_data = []
#         winner = max(percentages, key=percentages.get)
#         for candidate, percentage in percentages.items():
#             winner_mark = "*" if candidate == winner else ""
#             table_data.append([candidate, f"{percentage:.2f}%", winner_mark])
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))

# import numpy as np
# from typing import Tuple, List, Dict
# from tabulate import tabulate
#
#
# class RankedVoting:
#     def __init__(self, show_intermediate: bool = False):
#         self.show_intermediate = show_intermediate
#         self.candidates: List[str] = []
#         self.voters: Dict[str, Dict[str, int]] = {}
#         self.vote_percentages: Dict[str, float] = {}
#         self.vote_counts: Dict[str, int] = {}
#
#     def _calculate_vote_percentages(self) -> None:
#         total_votes = sum(self.vote_counts.values())
#         if total_votes == 0:
#             self.vote_percentages = {candidate: 0 for candidate in self.candidates}
#         else:
#             candidates_arr = np.array(self.candidates)
#             votes_arr = np.array(list(self.vote_counts.values()))
#             self.vote_percentages = dict(zip(candidates_arr, (votes_arr / total_votes) * 100))
#
#     def _is_winner_found(self) -> bool:
#         return any(percentage > 50.0 for percentage in self.vote_percentages.values())
#
#     def _get_least_voted_candidate(self) -> str:
#         if not self.vote_counts:
#             return self.candidates[0]  # Return any candidate when there are no votes
#
#         return min(self.vote_counts, key=self.vote_counts.get)
#
#     def _redistribute_votes(self, least_voted_candidate: str) -> None:
#         least_votes = min(self.vote_counts.values())
#         least_voted_candidates = [candidate for candidate, votes in self.vote_counts.items() if votes == least_votes]
#
#         # Remove the candidate with the least votes from the vote_counts before redistribution
#         for candidate in least_voted_candidates:
#             del self.vote_counts[candidate]
#
#         for voter, preferences in self.voters.items():
#             for least_voted_candidate in least_voted_candidates:
#                 least_voted_rank = preferences.get(least_voted_candidate)
#                 if least_voted_rank is not None and least_voted_rank in self.candidates:
#                     # Get all candidates with equal ranks
#                     equal_ranks_candidates = [candidate for candidate, rank in preferences.items() if
#                                               rank == least_voted_rank]
#
#                     # Calculate the total number of votes to redistribute equally among candidates with equal ranks
#                     total_votes_to_redistribute = self.vote_counts[least_voted_candidate] // len(equal_ranks_candidates)
#
#                     # Redistribute votes to all candidates with equal ranks
#                     for candidate in equal_ranks_candidates:
#                         self.vote_counts[candidate] += total_votes_to_redistribute
#
#         # Reset the vote count of the least voted candidate to 0 after redistribution
#         for candidate in least_voted_candidates:
#             self.vote_counts[candidate] = 0
#
#     def _find_winner(self) -> str:
#         while not self._is_winner_found():
#             least_voted_candidate = self._get_least_voted_candidate()
#             self._redistribute_votes(least_voted_candidate)
#
#         return max(self.vote_percentages, key=self.vote_percentages.get)
#
#     def run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
#         self._calculate_vote_percentages()
#         winner = self._find_winner()
#         return self.vote_percentages, winner
#
#     def run_ranked_voting_with_ties_handling(self) -> Tuple[Dict[str, float], str]:
#         if not self.candidates or not self.voters:
#             raise ValueError("No candidates or voters provided.")
#
#         # Initialize vote_counts dictionary with 0 votes for each candidate
#         self.vote_counts = {candidate: 0 for candidate in self.candidates}
#
#         # Count the votes for each candidate
#         for voter, preferences in self.voters.items():
#             first_choice = min(preferences.values())
#             candidate_with_first_choice = next(candidate for candidate, rank in preferences.items() if rank == first_choice)
#             self.vote_counts[candidate_with_first_choice] += 1
#
#         # Run ranked voting with proper tie handling
#         return self.run_ranked_voting()
#
#     def display_intermediate_results(self, percentages: Dict[str, float]) -> None:
#         print("Intermediate Results:")
#         headers = ["Candidate", "Percentage"]
#         table_data = [[candidate, f"{percentage:.2f}%"] for candidate, percentage in percentages.items()]
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))
#         print()
#
#     def display_final_results(self, percentages: Dict[str, float]) -> None:
#         print("Final Results:")
#         headers = ["Candidate", "Percentage", "Winner"]
#         table_data = []
#         winner = max(percentages, key=percentages.get)
#         for candidate, percentage in percentages.items():
#             winner_mark = "*" if candidate == winner else ""
#             table_data.append([candidate, f"{percentage:.2f}%", winner_mark])
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))


# import numpy as np
# from typing import Tuple, List, Dict
# from tabulate import tabulate
#
#
# class RankedVoting:
#     def __init__(self, show_intermediate: bool = False):
#         self.show_intermediate = show_intermediate
#         self.candidates: List[str] = []
#         self.voters: Dict[str, Dict[str, int]] = {}
#         self.vote_percentages: Dict[str, float] = {}
#         self.vote_counts: Dict[str, int] = {}
#
#     def _calculate_vote_percentages(self) -> None:
#         total_votes = sum(self.vote_counts.values())
#         if total_votes == 0:
#             self.vote_percentages = {candidate: 0 for candidate in self.candidates}
#         else:
#             candidates_arr = np.array(self.candidates)
#             votes_arr = np.array(list(self.vote_counts.values()))
#             self.vote_percentages = dict(zip(candidates_arr, (votes_arr / total_votes) * 100))
#
#     def _is_winner_found(self) -> bool:
#         return any(percentage > 50.0 for percentage in self.vote_percentages.values())
#
#     def _get_least_voted_candidate(self) -> str:
#         if not self.vote_counts:
#             return self.candidates[0]  # Return any candidate when there are no votes
#
#         return min(self.vote_counts, key=self.vote_counts.get)
#
#     # def redistribute_votes(self, candidate_to_remove: str) -> None:
#     #     total_votes = self.vote_counts.pop(candidate_to_remove, 0)
#     #     candidates_to_redistribute = []
#     #
#     #     # Identify the candidates to whom we can redistribute votes
#     #     removed_candidates = {candidate_to_remove}  # Track the removed candidates in a set
#     #     for voter, prefs in self.voters.items():
#     #         least_ranked_candidates = [c for c, rank in prefs.items() if rank == 1 and c not in removed_candidates]
#     #         if least_ranked_candidates:
#     #             least_ranked_candidate = least_ranked_candidates[0].strip()  # Strip leading and trailing spaces
#     #             candidates_to_redistribute.append((voter, least_ranked_candidate))
#     #
#     #     # Adjust vote counts and preferences
#     #     for voter, redistributed_candidate in candidates_to_redistribute:
#     #         if redistributed_candidate in self.vote_counts:
#     #             self.vote_counts[redistributed_candidate] += total_votes
#     #         else:
#     #             self.vote_counts[redistributed_candidate] = total_votes
#     #
#     #         # Update the voter's preferences to remove the removed candidate
#     #         del self.voters[voter][candidate_to_remove]
#     #         # Set the preference of the redistributed candidate to 1
#     #         self.voters[voter][redistributed_candidate] = 1
#     #
#     #     # Now remove the redistributed candidate from the set of removed candidates
#     #     for _, redistributed_candidate in candidates_to_redistribute:
#     #         removed_candidates.discard(redistributed_candidate)
#
#     def redistribute_votes(self, candidate_to_remove: str) -> None:
#         total_votes = self.vote_counts.pop(candidate_to_remove, 0)
#         removed_candidates = {candidate_to_remove}
#
#         while total_votes > 0:
#             votes_redistributed = False  # Track if we have redistributed any votes in this iteration
#             for voter, prefs in self.voters.items():
#                 least_ranked_candidates = [c for c, rank in prefs.items() if rank == 1 and c not in removed_candidates]
#                 if least_ranked_candidates:
#                     least_ranked_candidate = least_ranked_candidates[0]
#                     if least_ranked_candidate in self.vote_counts:
#                         self.vote_counts[least_ranked_candidate] += 1
#                     else:
#                         self.vote_counts[least_ranked_candidate] = 1
#                     self.voters[voter][least_ranked_candidate] = 0
#                     total_votes -= 1
#                     votes_redistributed = True  # Mark that votes have been redistributed in this iteration
#
#             if not votes_redistributed:
#                 break  # No valid votes left to redistribute, exit the loop
#
#         # Remove voters whose preferences are exhausted and contain only removed candidates
#         self.voters = {voter: prefs for voter, prefs in self.voters.items() if
#                        any(prefs.values()) and not all(c in removed_candidates for c in prefs)}
#
#         print("Vote counts after redistribution:", self.vote_counts)
#         print("Voters after redistribution:", self.voters)
#         print("Total votes after redistribution:", total_votes)
#
#     def find_winner(self) -> str:
#         while not self._is_winner_found():
#             least_voted_candidate = self._get_least_voted_candidate()
#             self.redistribute_votes(least_voted_candidate)
#
#         return max(self.vote_percentages, key=self.vote_percentages.get)
#
#     def _run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
#         self._calculate_vote_percentages()
#         winner = self.find_winner()
#         return self.vote_percentages, winner
#
#     def run_ranked_voting_with_ties_handling(self) -> Tuple[Dict[str, float], str]:
#         if not self.candidates or not self.voters:
#             raise ValueError("No candidates or voters provided.")
#
#         # Initialize vote_counts dictionary with 0 votes for each candidate
#         self.vote_counts = {candidate: 0 for candidate in self.candidates}
#
#         # Count the votes for each candidate
#         for voter, preferences in self.voters.items():
#             first_choice = min(preferences.values())
#             candidate_with_first_choice = next(candidate for candidate, rank in preferences.items() if rank == first_choice)
#             self.vote_counts[candidate_with_first_choice] += 1
#
#         # Run ranked voting with proper tie handling
#         return self._run_ranked_voting()
#
#     def display_intermediate_results(self, percentages: Dict[str, float]) -> None:
#         print("Intermediate Results:")
#         headers = ["Candidate", "Percentage"]
#         table_data = [[candidate, f"{percentage:.2f}%"] for candidate, percentage in percentages.items()]
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))
#         print()
#
#     def display_final_results(self, percentages: Dict[str, float]) -> None:
#         print("Final Results:")
#         headers = ["Candidate", "Percentage", "Winner"]
#         table_data = []
#         winner = max(percentages, key=percentages.get)
#         for candidate, percentage in percentages.items():
#             winner_mark = "*" if candidate == winner else ""
#             table_data.append([candidate, f"{percentage:.2f}%", winner_mark])
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))


# from typing import Tuple, List, Dict
# from tabulate import tabulate
#
#
# class RankedVoting:
#     def __init__(self, show_intermediate: bool = False):
#         self.show_intermediate = show_intermediate
#         self.candidates: List[str] = []
#         self.voters: Dict[str, Dict[str, int]] = {}
#         self.vote_percentages: Dict[str, float] = {}
#         self.vote_counts: Dict[str, int] = {}
#
#     def _calculate_vote_percentages(self) -> None:
#         total_votes = sum(self.vote_counts.values())
#         if total_votes == 0:
#             self.vote_percentages = {candidate: 0 for candidate in self.candidates}
#         else:
#             self.vote_percentages = {candidate: (votes / total_votes) * 100 for candidate, votes in self.vote_counts.items()}
#
#     def _is_winner_found(self) -> bool:
#         return any(percentage > 50.0 for percentage in self.vote_percentages.values())
#
#     def _get_least_voted_candidate(self) -> str:
#         if not self.vote_counts:
#             return self.candidates[0]  # Return any candidate when there are no votes
#
#         return min(self.vote_counts, key=self.vote_counts.get)
#
#     def _redistribute_votes(self, candidate_to_remove: str) -> None:
#         total_votes = self.vote_counts[candidate_to_remove]
#         preferences = {voter: prefs.copy() for voter, prefs in self.voters.items()}
#         for voter, prefs in preferences.items():
#             least_ranked_candidates = [c for c, rank in prefs.items() if rank == 1]
#             if candidate_to_remove in least_ranked_candidates:
#                 least_ranked_candidates.remove(candidate_to_remove)
#
#             if least_ranked_candidates:
#                 least_ranked_candidate = least_ranked_candidates[0]
#                 self.vote_counts[least_ranked_candidate] += 1
#                 del prefs[candidate_to_remove]
#
#         del self.vote_counts[candidate_to_remove]
#
#     def _find_winner(self) -> str:
#         while not self._is_winner_found():
#             least_voted_candidate = self._get_least_voted_candidate()
#             self._redistribute_votes(least_voted_candidate)
#
#         return max(self.vote_percentages, key=self.vote_percentages.get)
#
#     def _run_ranked_voting(self) -> Tuple[Dict[str, float], str]:
#         self._calculate_vote_percentages()
#         winner = self._find_winner()
#         return self.vote_percentages, winner
#
#     def run_ranked_voting_with_ties_handling(self) -> Tuple[Dict[str, float], str]:
#         if not self.candidates or not self.voters:
#             raise ValueError("No candidates or voters provided.")
#
#         # Initialize vote_counts dictionary with 0 votes for each candidate
#         self.vote_counts = {candidate: 0 for candidate in self.candidates}
#
#         # Count the votes for each candidate
#         for voter, preferences in self.voters.items():
#             first_choice = min(preferences.values())
#             candidate_with_first_choice = next(candidate for candidate, rank in preferences.items() if rank == first_choice)
#             self.vote_counts[candidate_with_first_choice] += 1
#
#         # Run ranked voting with proper tie handling
#         return self._run_ranked_voting()
#
#     def display_intermediate_results(self, percentages: Dict[str, float]) -> None:
#         print("Intermediate Results:")
#         headers = ["Candidate", "Percentage"]
#         table_data = [[candidate, f"{percentage:.2f}%"] for candidate, percentage in percentages.items()]
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))
#         print()
#
#     def display_final_results(self, percentages: Dict[str, float]) -> None:
#         print("Final Results:")
#         headers = ["Candidate", "Percentage", "Winner"]
#         table_data = []
#         winner = max(percentages, key=percentages.get)
#         for candidate, percentage in percentages.items():
#             winner_mark = "*" if candidate == winner else ""
#             table_data.append([candidate, f"{percentage:.2f}%", winner_mark])
#         print(tabulate(table_data, headers=headers, tablefmt="grid"))


# from typing import List, Dict
# from collections import Counter
# import numpy as np
#
# class RankedVoting:
#     def __init__(self):
#         self.candidates = {}  # Dictionary to store candidates and their vote counts
#         self.voters = {}  # Dictionary to store voters and their ranked preferences
#         self.vote_counts = {}  # Dictionary to store the vote counts for each candidate
#
#     def add_candidate(self, candidate_name: str) -> None:
#         """
#         Add a candidate to the ranked voting system.
#         """
#         if candidate_name not in self.candidates:
#             self.candidates[candidate_name] = 0
#
#     def add_candidates(self, candidates_data: set) -> None:
#         for candidate in candidates_data:
#             self.candidates[candidate] = 0
#
#     def get_candidate_percentage(self, candidate_name: str) -> float:
#         """
#         Get the percentage of votes for a specific candidate.
#         """
#         total_votes = sum(self.candidates.values())
#         if total_votes == 0:
#             return 0.0
#         return self.candidates[candidate_name] / total_votes * 100
#
#     def calculate_vote_counts(self):
#         """
#         Calculate the vote counts for each candidate from the voters' preferences.
#         """
#         vote_counts = {candidate: 0 for candidate in self.candidates}
#
#         for voter_prefs in self.voters.values():
#             for candidate, rank in voter_prefs.items():
#                 if rank == 1 and candidate in self.candidates:
#                     vote_counts[candidate] += 1
#
#         return vote_counts
#
#     def add_vote(self, ranked_preferences):
#         voter_id = f"Voter {len(self.voters) + 1}"
#         self.voters[voter_id] = ranked_preferences
#
#     def add_voters(self, voters_data: dict) -> None:
#         for voter, ranked_preferences in voters_data.items():
#             self.add_vote(ranked_preferences)
#             self.voters[voter] = ranked_preferences
#
#     def _is_winner_found(self) -> bool:
#         total_votes = sum(self.vote_counts.values())
#         if not total_votes:
#             return False
#
#         for candidate, votes in self.vote_counts.items():
#             if votes / total_votes > 0.5:
#                 print(f"{candidate} is the winner with {votes} votes!")
#                 return True
#
#         return False
#
#     def _get_winner(self):
#         total_votes = sum(self.candidates.values())
#         if not total_votes:
#             return None
#
#         for candidate, votes in self.candidates.items():
#             if votes / total_votes > 0.5:
#                 return candidate
#         return None
#
#     def find_winner(self) -> str:
#         total_votes = sum(self.candidates.values())
#
#         while not any(votes / total_votes > 0.5 for votes in self.candidates.values()):
#             least_voted_candidate = min(self.candidates, key=self.candidates.get, default=None)
#             if least_voted_candidate is None:
#                 break
#             self.redistribute_votes(least_voted_candidate)
#
#         if any(votes / total_votes > 0.5 for votes in self.candidates.values()):
#             winner = max(self.candidates, key=self.candidates.get)
#             print(f"The winner is {winner}!")
#             winner_percentage = self.candidates[winner] / total_votes * 100
#             print(f"Final percentage for the winner: {winner_percentage:.2f}%")
#         else:
#             print("No candidate reached 50% of the votes. A runoff election may be needed.")
#
#     def find_candidate_with_least_votes(self) -> str:
#         if not self.candidates:
#             return ""
#
#         min_votes = min(self.candidates.values())
#         candidates_with_min_votes = [candidate for candidate, votes in self.candidates.items() if votes == min_votes]
#         return candidates_with_min_votes[0]
#
#     # Updated implementation of redistribute_votes
#     def redistribute_votes(self, candidate_to_remove: str) -> None:
#         if candidate_to_remove not in self.candidates:
#             return
#
#         # Collect votes for the candidate to be removed
#         votes_to_redistribute = self.candidates[candidate_to_remove]
#         del self.candidates[candidate_to_remove]
#
#         # Collect the remaining candidates
#         remaining_candidates = list(self.candidates.keys())
#
#         # Get the votes for each candidate in a NumPy array
#         candidate_votes = np.array(list(self.candidates.values()))
#
#         # Redistribute votes using NumPy
#         redistributed_votes = np.zeros(len(remaining_candidates), dtype=int)
#         for voter_preferences in self.voters.values():
#             top_preference = next((pref for pref in voter_preferences if pref in remaining_candidates), None)
#             if top_preference is not None:
#                 candidate_index = remaining_candidates.index(top_preference)
#                 redistributed_votes[candidate_index] += 1
#
#         # Update the candidates with redistributed votes
#         candidate_votes += redistributed_votes
#
#         # Remove candidates with zero votes
#         self.candidates = {candidate: votes for candidate, votes in zip(remaining_candidates, candidate_votes) if votes > 0}
#
#         # Redistribute any remaining votes recursively
#         if votes_to_redistribute > 0:
#             self.redistribute_votes(self.find_candidate_with_least_votes())
#
#         print(f"Redistribution details:")
#         for candidate, votes in self.candidates.items():
#             print(f"Candidate {candidate}: {votes} votes")
#
#         print(f"Current percentage for each candidate:")
#         total_votes = len(self.voters)
#         for candidate, votes in self.candidates.items():
#             percentage = votes / total_votes * 100
#             print(f"Candidate {candidate}: {percentage:.2f}%")
#
#     def _get_least_voted_candidate(self) -> str:
#         """
#         Get the candidate with the least number of votes.
#         """
#         return min(self.candidates, key=self.candidates.get, default=None)
#
#     def run_ranked_voting(self):
#         print("Running ranked voting...")
#
#         # Calculate the total number of votes
#         total_votes = len(self.voters)
#
#         # Calculate and display the initial percentages for each candidate
#         print("Initial percentage for each candidate:")
#         self.vote_counts = self.calculate_vote_counts()  # Calculate vote counts
#         for candidate, votes in self.vote_counts.items():
#             percentage = votes / total_votes * 100 if total_votes > 0 else 0
#             print(f"Candidate {candidate}: {percentage:.2f}%")
#
#         winner = self._get_winner()
#
#         while not winner:
#             least_voted_candidate = self._get_least_voted_candidate()
#             if least_voted_candidate is None:
#                 break
#             print(f"Eliminating candidate {least_voted_candidate}...")
#             self.redistribute_votes(least_voted_candidate)
#
#             # Calculate the percentage for each candidate at each round
#             self.vote_counts = self.calculate_vote_counts()  # Calculate vote counts
#             total_votes = len(self.voters)  # Recalculate total votes after redistribution
#             print("Current percentage for each candidate:")
#             for candidate, votes in self.vote_counts.items():
#                 percentage = votes / total_votes * 100 if total_votes > 0 else 0
#                 print(f"Candidate {candidate}: {percentage:.2f}%")
#
#             winner = self._get_winner()
#
#         if winner:
#             print(f"The winner is {winner}!")
#             winner_percentage = self.vote_counts[winner] / total_votes * 100 if total_votes > 0 else 0
#             print(f"Final percentage for the winner: {winner_percentage:.2f}%")
#         else:
#             print("No candidate reached 50% of the votes. A runoff election may be needed.")

# from typing import List, Dict
# from collections import Counter
# import numpy as np
#
# class RankedVoting:
#     def __init__(self):
#         self.candidates = {}  # Dictionary to store candidates and their vote counts
#         self.voters = {}  # Dictionary to store voters and their ranked preferences
#         self.vote_counts = {}  # Dictionary to store the vote counts for each candidate
#
#     def add_candidate(self, candidate_name: str) -> None:
#         """
#         Add a candidate to the ranked voting system.
#         """
#         if candidate_name not in self.candidates:
#             self.candidates[candidate_name] = 0
#
#     def add_candidates(self, candidates_data: set) -> None:
#         for candidate in candidates_data:
#             self.candidates[candidate] = 0
#
#     def get_candidate_percentage(self, candidate_name: str) -> float:
#         """
#         Get the percentage of votes for a specific candidate.
#         """
#         total_votes = sum(self.candidates.values())
#         if total_votes == 0:
#             return 0.0
#         return self.candidates[candidate_name] / total_votes * 100
#
#     def calculate_vote_counts(self):
#         """
#         Calculate the vote counts for each candidate from the voters' preferences.
#         """
#         vote_counts = {candidate: 0 for candidate in self.candidates}
#
#         for voter_prefs in self.voters.values():
#             # Find the top preference among the remaining candidates
#             top_preference = min(voter_prefs, key=lambda x: voter_prefs.get(x, float('inf')))
#             if top_preference in self.candidates:
#                 vote_counts[top_preference] += 1
#
#         return vote_counts
#
#     def _get_winner(self):
#         total_votes = sum(self.candidates.values())
#         if not total_votes:
#             return None
#
#         for candidate, votes in self.candidates.items():
#             if votes / total_votes > 0.5:
#                 return candidate
#         return None
#
#     def add_vote(self, ranked_preferences):
#         voter_id = f"Voter {len(self.voters) + 1}"
#         self.voters[voter_id] = ranked_preferences
#
#     def add_voters(self, voters_data: dict) -> None:
#         for voter, ranked_preferences in voters_data.items():
#             self.add_vote(ranked_preferences)
#             self.voters[voter] = ranked_preferences
#
#     def redistribute_votes(self, candidate_to_remove: str) -> None:
#         if candidate_to_remove not in self.candidates:
#             return
#
#         # Collect votes for the candidate to be removed
#         votes_to_redistribute = self.candidates[candidate_to_remove]
#         del self.candidates[candidate_to_remove]
#
#         # Collect the remaining candidates
#         remaining_candidates = list(self.candidates.keys())
#
#         # Redistribute votes using NumPy
#         redistributed_votes = np.zeros(len(remaining_candidates), dtype=int)
#         for voter_id, voter_preferences in self.voters.items():
#             if candidate_to_remove in voter_preferences:
#                 # Find the highest-ranked remaining candidate in voter's preferences
#                 top_preference = min(remaining_candidates, key=lambda x: voter_preferences.get(x, float('inf')))
#                 candidate_index = remaining_candidates.index(top_preference)
#                 redistributed_votes[candidate_index] += 1
#
#         # Update the candidates with redistributed votes
#         for i, candidate in enumerate(remaining_candidates):
#             self.candidates[candidate] += redistributed_votes[i]
#
#         # Update voter preferences after redistribution
#         for voter_id, voter_preferences in self.voters.items():
#             if candidate_to_remove in voter_preferences:
#                 top_preference = min(remaining_candidates, key=lambda x: voter_preferences.get(x, float('inf')))
#                 voter_preferences[candidate_to_remove] = voter_preferences.get(top_preference, float('inf'))
#
#         # Redistribute any remaining votes recursively
#         if votes_to_redistribute > 0:
#             self.redistribute_votes(self.find_candidate_with_least_votes())
#
#         print(f"Redistribution details:")
#         for candidate, votes in self.candidates.items():
#             print(f"Candidate {candidate}: {votes} votes")
#
#         print(f"Current percentage for each candidate:")
#         total_votes = len(self.voters)
#         for candidate, votes in self.candidates.items():
#             percentage = votes / total_votes * 100
#             print(f"Candidate {candidate}: {percentage:.2f}%")
#
#     def find_candidate_with_least_votes(self) -> str:
#         if not self.candidates:
#             return ""
#
#         min_votes = min(self.candidates.values())
#         candidates_with_min_votes = [candidate for candidate, votes in self.candidates.items() if votes == min_votes]
#         return candidates_with_min_votes[0]
#
#     def _get_least_voted_candidate(self) -> str:
#         """
#         Get the candidate with the least number of votes.
#         """
#         return min(self.candidates, key=self.candidates.get, default=None)
#
#     def run_ranked_voting(self):
#         print("Running ranked voting...")
#
#         # Calculate the total number of votes
#         total_votes = len(self.voters)
#
#         # Calculate and display the initial percentages for each candidate
#         print("Initial percentage for each candidate:")
#         self.vote_counts = self.calculate_vote_counts()  # Calculate vote counts
#         for candidate, votes in self.vote_counts.items():
#             percentage = votes / total_votes * 100 if total_votes > 0 else 0
#             print(f"Candidate {candidate}: {percentage:.2f}%")
#
#         winner = self._get_winner()
#
#         while not winner:
#             least_voted_candidate = self._get_least_voted_candidate()
#             if least_voted_candidate is None:
#                 break
#             print(f"Eliminating candidate {least_voted_candidate}...")
#             self.redistribute_votes(least_voted_candidate)
#
#             # Calculate the percentage for each candidate at each round
#             self.vote_counts = self.calculate_vote_counts()  # Calculate vote counts
#             total_votes = len(self.voters)  # Recalculate total votes after redistribution
#             print("Current percentage for each candidate:")
#             for candidate, votes in self.vote_counts.items():
#                 percentage = votes / total_votes * 100 if total_votes > 0 else 0
#                 print(f"Candidate {candidate}: {percentage:.2f}%")
#
#             winner = self._get_winner()
#
#         if winner:
#             print(f"The winner is {winner}!")
#             winner_percentage = self.vote_counts[winner] / total_votes * 100 if total_votes > 0 else 0
#             print(f"Final percentage for the winner: {winner_percentage:.2f}%")
#         else:
#             print("No candidate reached 50% of the votes. A runoff election may be needed.")

# from typing import Dict
# import tabulate
# class RankedVoting:
#     def __init__(self):
#         self.candidates = {}  # Dictionary to store candidates and their vote counts
#         self.voters = {}  # Dictionary to store voters and their ranked preferences
#
#     def add_candidate(self, candidate_name: str) -> None:
#         """
#         Add a candidate to the ranked voting system.
#         """
#         if candidate_name not in self.candidates:
#             self.candidates[candidate_name] = 0
#
#     def add_candidates(self, candidates_data: set) -> None:
#         for candidate in candidates_data:
#             self.candidates[candidate] = 0
#
#     def get_candidate_percentage(self, candidate_name: str) -> float:
#         """
#         Get the percentage of votes for a specific candidate.
#         """
#         total_votes = sum(self.candidates.values())
#         if total_votes == 0:
#             return 0.0
#         return self.candidates[candidate_name] / total_votes * 100
#
#     def calculate_vote_counts(self) -> Dict[str, int]:
#         """
#         Calculate the vote counts for each candidate from the voters' preferences.
#         """
#         vote_counts = {candidate: 0 for candidate in self.candidates}
#
#         for voter_prefs in self.voters.values():
#             # Find the top preference among the remaining candidates
#             top_preference = min(voter_prefs, key=lambda x: voter_prefs.get(x, float('inf')))
#             if top_preference in self.candidates:
#                 vote_counts[top_preference] += 1
#
#         return vote_counts
#
#     def _get_winner(self) -> str:
#         total_votes = sum(self.candidates.values())
#         if not total_votes:
#             return ""
#
#         for candidate, votes in self.candidates.items():
#             if votes / total_votes > 0.5:
#                 return candidate
#         return ""
#
#     def add_vote(self, ranked_preferences: Dict[str, int]) -> None:
#         voter_id = f"Voter {len(self.voters) + 1}"
#         self.voters[voter_id] = ranked_preferences
#
#     def add_voters(self, voters_data: Dict[str, Dict[str, int]]) -> None:
#         for voter, ranked_preferences in voters_data.items():
#             self.add_vote(ranked_preferences)
#             self.voters[voter] = ranked_preferences
#
#     def redistribute_votes(self, candidate_to_remove: str) -> None:
#         if candidate_to_remove not in self.candidates:
#             return
#
#         # Collect votes for the candidate to be removed
#         votes_to_redistribute = self.candidates[candidate_to_remove]
#         del self.candidates[candidate_to_remove]
#
#         # Collect the remaining candidates and their vote counts
#         remaining_candidates, candidate_votes = zip(*self.candidates.items())
#
#         # Redistribute votes
#         for voter_preferences in self.voters.values():
#             if candidate_to_remove in voter_preferences:
#                 # Find the highest-ranked remaining candidate in voter's preferences
#                 top_preference = min(remaining_candidates, key=lambda x: voter_preferences.get(x, float('inf')))
#                 candidate_index = remaining_candidates.index(top_preference)
#                 candidate_votes[candidate_index] += 1
#
#         # Update the candidates with redistributed votes
#         self.candidates = {candidate: votes for candidate, votes in zip(remaining_candidates, candidate_votes) if votes > 0}
#
#         # Redistribute any remaining votes recursively
#         if votes_to_redistribute > 0:
#             self.redistribute_votes(self.find_candidate_with_least_votes())
#
#         total_votes = len(self.voters)
#         for candidate, votes in self.candidates.items():
#             percentage = votes / total_votes * 100
#
#     def find_candidate_with_least_votes(self) -> str:
#         if not self.candidates:
#             return ""
#
#         min_votes = min(self.candidates.values())
#         candidates_with_min_votes = [candidate for candidate, votes in self.candidates.items() if votes == min_votes]
#         return candidates_with_min_votes[0]
#
#     def _get_least_voted_candidate(self) -> str:
#         """
#         Get the candidate with the least number of votes.
#         """
#         return min(self.candidates, key=self.candidates.get, default="")
#
#     def show_initial_percentages(self):
#         table_data = []
#         headers = ['Candidate', 'Initial Percentage']
#         total_votes = len(self.voters)
#
#         # Count the number of first preferences for each candidate
#         candidate_votes = {candidate: 0 for candidate in self.candidates}
#         for voter_prefs in self.voters.values():
#             top_preference = min(voter_prefs, key=lambda x: voter_prefs.get(x, float('inf')))
#             if top_preference in self.candidates:
#                 candidate_votes[top_preference] += 1
#
#         # Calculate and display initial percentages
#         for candidate, votes in candidate_votes.items():
#             percentage = votes / total_votes * 100
#             row = [candidate, f"{percentage:.2f}%"]
#             table_data.append(row)
#
#         print("Initial Percentages:")
#         print(tabulate.tabulate(table_data, headers=headers))
#
#     def show_vote_movement(self):
#         table_data = []
#         headers = ['Candidate'] + list(self.voters.keys())
#         for candidate, votes in self.calculate_vote_counts().items():
#             row = [candidate] + [votes]
#             table_data.append(row)
#
#         print("Vote Movement:")
#         print(tabulate.tabulate(table_data, headers=headers))
#
#     def show_final_result(self):
#         table_data = []
#         headers = ['Candidate', 'Percentage']
#         total_votes = len(self.voters)
#
#         for candidate, votes in self.calculate_vote_counts().items():
#             percentage = votes / total_votes * 100 if total_votes > 0 else 0
#             row = [candidate, f"{percentage:.2f}%"]
#             table_data.append(row)
#
#         print("Final Result:")
#         print(tabulate.tabulate(table_data, headers=headers))
#
#         winner = self._get_winner()
#         if winner:
#             print(f"The winner is {winner}!")
#         else:
#             print("No candidate reached 50% of the votes. A runoff election may be needed.")
#
#
#     def run_ranked_voting(self):
#
#         # Calculate the total number of votes
#         total_votes = len(self.voters)
#
#         # Calculate and display the initial percentages for each candidate
#         self.candidates = self.calculate_vote_counts()  # Calculate vote counts
#         for candidate, votes in self.candidates.items():
#             percentage = votes / total_votes * 100 if total_votes > 0 else 0
#
#         winner = self._get_winner()
#
#         while not winner:
#             least_voted_candidate = self._get_least_voted_candidate()
#             if not least_voted_candidate:
#                 break
#             self.redistribute_votes(least_voted_candidate)
#
#             # Calculate the percentage for each candidate at each round
#             self.candidates = self.calculate_vote_counts()  # Calculate vote counts
#             total_votes = len(self.voters)  # Recalculate total votes after redistribution
#             print("Current percentage for each candidate:")
#             for candidate, votes in self.candidates.items():
#                 percentage = votes / total_votes * 100 if total_votes > 0 else 0
#                 print(f"Candidate {candidate}: {percentage:.2f}%")
#
#             winner = self._get_winner()

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
        """
        Get the percentage of votes for a specific candidate.
        """
        total_votes = sum(self.candidates.values())
        if total_votes == 0:
            return 0.0
        return self.candidates[candidate_name] / total_votes * 100

    def calculate_vote_counts(self, candidates=None) -> Dict[str, int]:
        candidates = candidates or self.candidates
        vote_counts = {candidate: 0 for candidate in candidates}

        for voter_preferences in self.voters.values():
            voted = False  # To check if the voter voted for any candidate in their preferences
            for candidate in candidates:
                if candidate in voter_preferences:
                    vote_counts[candidate] += 1
                    voted = True
                    break

            # If the voter did not vote for any candidate in their preferences, consider their vote for the least voted candidate
            if not voted:
                least_voted_candidate = self.find_candidate_with_least_votes()
                if least_voted_candidate:
                    vote_counts[least_voted_candidate] += 1

        return vote_counts

    def calculate_vote_percentages(self, candidates) -> dict:
        total_votes = sum(candidates.values())
        if total_votes == 0:
            return {candidate: 0 for candidate in candidates}

        vote_percentages = {candidate: count / total_votes * 100 for candidate, count in candidates.items()}
        return vote_percentages

    def _get_winner(self) -> str:
        total_votes = sum(self.candidates.values())
        if not total_votes:
            return ""

        for candidate, votes in self.candidates.items():
            if votes / total_votes > 0.5:
                return candidate
        return ""

    def add_vote(self, ranked_preferences: Dict[str, int]) -> None:
        if not ranked_preferences or not isinstance(ranked_preferences, dict):
            raise ValueError("Ranked preferences should be a non-empty dictionary.")

        if len(ranked_preferences) != len(self.candidates):
            raise ValueError("Ranked preferences should have preferences for all candidates.")

        voter_id = f"Voter {len(self.voters) + 1}"
        self.voters[voter_id] = ranked_preferences  # Remove this line; the same line appears in the add_voters method

    def add_voters(self, voters_data: Dict[str, Dict[str, int]]) -> None:
        if not voters_data or not isinstance(voters_data, dict):
            raise ValueError("Voters data should be a non-empty dictionary.")

        # Create a new list to store the elements
        new_voters_data = list(voters_data.items())

        # Add the new elements to the global voters dictionary
        for voter, ranked_preferences in new_voters_data:
            self.add_vote(ranked_preferences)
            self.voters[voter] = ranked_preferences

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

    def redistribute_votes(self, candidates_to_remove):
        if not candidates_to_remove:
            return

        local_candidates = self.candidates.copy()
        local_voters = self.voters.copy()

        while candidates_to_remove:
            candidate_to_remove = candidates_to_remove.pop(0)
            if candidate_to_remove not in local_candidates:
                continue

            # Collect votes for the candidate to be removed
            votes_to_redistribute = local_candidates[candidate_to_remove]
            del local_candidates[candidate_to_remove]

            # Collect the remaining candidates and their vote counts as NumPy arrays
            remaining_candidates = list(local_candidates.keys())
            candidate_votes = np.array(list(local_candidates.values()))

            # Redistribute votes
            for voter_preferences in local_voters.values():
                if candidate_to_remove in voter_preferences:
                    # Find the highest-ranked remaining candidate in voter's preferences
                    if remaining_candidates:
                        top_preference = min(remaining_candidates, key=lambda x: voter_preferences.get(x, float('inf')))
                    else:
                        break  # No need to continue redistribution if there are no more remaining candidates
                    candidate_index = remaining_candidates.index(top_preference)
                    candidate_votes[candidate_index] += 1

            # Update the candidates with redistributed votes
            local_candidates = {candidate: votes for candidate, votes in zip(remaining_candidates, candidate_votes) if
                                votes > 0}

            # Find the new least voted candidates and continue redistribution
            candidates_to_remove = self.find_candidates_with_least_votes(local_candidates)

            # Update the percentage movement
            vote_percentages = self.calculate_vote_percentages(local_candidates)
            self.percentage_movement.append(vote_percentages)

        self.candidates = local_candidates
        self.voters = local_voters

    def _get_least_voted_candidate(self) -> str:
        """
        Get the candidate with the least number of votes.
        """
        return min(self.candidates, key=self.candidates.get, default="")

    def show_initial_percentages(self) -> str:
        table_data = []
        headers = ['Candidate', 'Initial Percentage']
        total_votes = sum(sum(votes.values()) for votes in self.voters.values())

        for candidate, votes in self.calculate_vote_counts().items():
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
        # Add voters
        self.add_voters(self.voters)

        print("Initial Percentages:")
        print(self.show_initial_percentages())
        total_votes = len(self.voters)

        # Check the total votes before and after counting
        votes_before = sum(self.candidates.values())
        counted_votes = sum(self.calculate_vote_counts().values())
        assert votes_before == counted_votes == total_votes, "Votes not counted correctly!"

        print("Current percentage for each candidate:")
        print(self.calculate_vote_percentages(self.candidates))
        print("Vote Movement:")
        self.redistribute_votes(self.find_candidates_with_least_votes())
        print("Final Result:")
        self.show_final_result()
        self.show_percentage_movement()

