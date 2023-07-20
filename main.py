import argparse
from pathlib import Path
import RankedVotingFromCSV, RankedVotingFromYAML

def main(args: argparse.Namespace) -> None:
    candidates_file = args.candidates
    voter_files = args.voters

    if candidates_file.suffix == ".csv" and all(file.suffix == ".csv" for file in voter_files):
        voting_system = RankedVotingFromCSV(candidates_file, voter_files, show_intermediate=args.intermediate)
    elif candidates_file.suffix == ".yaml" and all(file.suffix == ".yaml" for file in voter_files):
        voting_system = RankedVotingFromYAML(candidates_file, voter_files, show_intermediate=args.intermediate)
    else:
        print("Invalid file format. Candidates and voter files must be either all CSV or all YAML.")
        return

    voting_system.run_ranked_voting()
    voting_system.display_final_results(voting_system.vote_percentages)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ranked Voting System")
    parser.add_argument("candidates", type=Path, help="Path to the candidates file (CSV or YAML)")
    parser.add_argument("voters", type=Path, nargs="+", help="Paths to the voter files (CSV or YAML)")
    parser.add_argument("--intermediate", action="store_true", help="Display intermediate results")
    args = parser.parse_args()
    main(args)