import argparse
# from RankedVoting.RankedVotingFromCSV import RankedVotingFromCSV
# from RankedVoting.RankedVotingFromYAML import RankedVotingFromYAML
from RankedVoting import RankedVotingFromCSV
from RankedVoting import RankedVoting
def main():
    # parser = argparse.ArgumentParser(description="Ranked Voting System")
    # parser.add_argument("file_path", type=str, help="Path to the CSV or main folder containing YAML files.")
    # parser.add_argument("--show_intermediate", action="store_true", help="Display intermediate results.")
    # args = parser.parse_args()

    # if args.file_path.lower().endswith(".csv"):
    #     # CSV file
    #     try:
    #         ranked_voting = RankedVotingFromCSV(args.file_path, show_intermediate=args.show_intermediate)
    #         results, winner = ranked_voting.run_ranked_voting()
    #         ranked_voting.display_final_results(results)
    #     except Exception as e:
    #         print(f"Error: {e}")
    # else:
    #     # YAML files in a folder
    #     try:
    #         ranked_voting = RankedVotingFromYAML(args.file_path, show_intermediate=args.show_intermediate)
    #         results, winner = ranked_voting.run_ranked_voting()
    #         ranked_voting.display_final_results(results)
    #     except Exception as e:
    #         print(f"Error: {e}")
    #---------
    # ranked_voting = RankedVotingFromCSV("Example/csv/example.csv", True)
    # results, winner = ranked_voting.run_ranked_voting()
    # ranked_voting.display_final_results(results)
    # ---------
    # data = {
    #     ' Candidate A': 1,
    #     ' Candidate B': 2,
    #     ' Candidate C': 3
    # }
    # voters_data = {
    #     'Voter 1': {' Candidate A': 1, ' Candidate B': 2, ' Candidate C': 3},
    #     'Voter 2': {' Candidate A': 0, ' Candidate B': 2, ' Candidate C': 1},
    #     'Voter 3': {' Candidate A': 1, ' Candidate B': 0, ' Candidate C': 0},
    #     'Voter 4': {' Candidate A': 3, ' Candidate B': 1, ' Candidate C': 2}
    # }
    #
    # candidates = list(data.keys())
    # voters = voters_data
    #
    # ranked_voting = RankedVoting()
    # ranked_voting.candidates = candidates
    # ranked_voting.voters = voters
    #
    # ranked_voting.run_ranked_voting()

    # Run the ranked voting
    # percentages, winner = ranked_voting.run_ranked_voting()

    # Display results
    # ranked_voting.display_final_results(percentages)
    # ---------
    # data = {
    #     'Candidate A',
    #     'Candidate B',
    #     'Candidate C'
    # }

    # voters_data = {
    #     'Voter 1': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
    #     'Voter 2': {'Candidate A': 0, 'Candidate B': 2, 'Candidate C': 1},
    #     'Voter 3': {'Candidate A': 1, 'Candidate B': 0, 'Candidate C': 0},
    #     'Voter 4': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
    #     'Voter 5': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 2}
    # }
    #
    # voters_data = {
    #     'Voter 1': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
    #     'Voter 2': {'Candidate A': 0, 'Candidate B': 2, 'Candidate C': 1},
    #     'Voter 3': {'Candidate A': 1, 'Candidate B': 0, 'Candidate C': 0},
    #     'Voter 4': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
    #     'Voter 5': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 2},
    # }

    # voters_data = {
    #     'Voter 1': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
    #     'Voter 2': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3},
    #     'Voter 3': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
    #     'Voter 4': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
    #     'Voter 5': {'Candidate A': 1, 'Candidate B': 3, 'Candidate C': 2},
    #     'Voter 6': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
    #     'Voter 7': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
    #     'Voter 8': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
    #     'Voter 9': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
    #     'Voter 10': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3}
    # }


    # # Create a new instance of RankedVoting
    # ranked_voting = RankedVoting()
    #
    # # Add candidates to the RankedVoting object
    # ranked_voting.add_candidates(data)
    #
    # # Add voters to the RankedVoting object
    # for voter, ranked_preferences in voters_data.items():
    #     ranked_voting.add_vote(ranked_preferences)
    #
    # ranked_voting.show_initial_percentages()
    #
    # # Run the ranked voting process with the provided data
    # ranked_voting.run_ranked_voting()
    #
    # # Show the vote movement
    # ranked_voting.show_vote_movement()
    #
    # # Show the final result
    # ranked_voting.show_final_result()
    # ---------
    # ranked_voting = RankedVoting()
    # candidates_data = {"A", "B", "C", "D"}
    # ranked_voting.add_candidates(candidates_data)
    #
    # voters_data = {
    #     "Voter 1": {"A": 1, "B": 2, "C": 3, "D": 4},
    #     "Voter 2": {"A": 1, "B": 2, "C": 3, "D": 4},
    #     "Voter 3": {"A": 1, "B": 2, "C": 3, "D": 4},
    # }
    # ranked_voting.add_voters(voters_data)
    #
    # ranked_voting.show_initial_percentages()
    # ranked_voting.run_ranked_voting()
    # ranked_voting.show_final_result()
    # ---------
    candidates_list = ['Candidate A', 'Candidate B', 'Candidate C']

    voters_data = {
        'Voter 1': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
        'Voter 2': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3},
        'Voter 3': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
        'Voter 4': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
        'Voter 5': {'Candidate A': 1, 'Candidate B': 3, 'Candidate C': 2},
        'Voter 6': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
        'Voter 7': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
        'Voter 8': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
        'Voter 9': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
        'Voter 10': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3}
    }

    # voters_data = {
    #     'Voter 1': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
    #     'Voter 2': {'Candidate A': 0, 'Candidate B': 2, 'Candidate C': 1},
    #     'Voter 3': {'Candidate A': 1, 'Candidate B': 0, 'Candidate C': 0},
    #     'Voter 4': {'Candidate A': 3, 'Candidate B': 1, 'Candidate C': 2},
    #     'Voter 5': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 2},
    # }

    ranked_voting = RankedVoting(candidates_list, voters_data)
    ranked_voting.run_ranked_voting()


if __name__ == "__main__":
    main()
