import argparse
from RankedVoting.RankedVotingFromCSV import RankedVotingFromCSV
from RankedVoting.RankedVotingFromYAML import RankedVotingFromYAML

def main():
    parser = argparse.ArgumentParser(description="Ranked Voting System")
    parser.add_argument("file_path", type=str, help="Path to the CSV or main folder containing YAML files.")
    parser.add_argument("--show_intermediate", action="store_true", help="Display intermediate results.")
    args = parser.parse_args()

    if args.file_path.lower().endswith(".csv"):
        # CSV file
        try:
            ranked_voting = RankedVotingFromCSV(args.file_path, show_intermediate=args.show_intermediate)
            results, winner = ranked_voting.run_ranked_voting()
            ranked_voting.display_final_results(results)
        except Exception as e:
            print(f"Error: {e}")
    else:
        # YAML files in a folder
        try:
            ranked_voting = RankedVotingFromYAML(args.file_path, show_intermediate=args.show_intermediate)
            results, winner = ranked_voting.run_ranked_voting()
            ranked_voting.display_final_results(results)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
