import argparse
import os

def main(args: argparse.Namespace) -> None:
    """
    Main function to run the Ranked Voting System using CSV or YAML files.

    Args:
        args (argparse.Namespace): Command-line arguments.

    Returns:
        None
    """
    main_folder = args.input_folder

    if args.file_format == "csv":
        from ranked_voting_from_csv import RankedVotingFromCSV

        voting_system = RankedVotingFromCSV(os.path.join(main_folder, args.file_name), show_intermediate=args.intermediate)
    elif args.file_format == "yaml":
        from ranked_voting_from_yaml import RankedVotingFromYAML

        voting_system = RankedVotingFromYAML(main_folder, show_intermediate=args.intermediate)
    else:
        raise ValueError("Invalid file format. Please choose 'csv' or 'yaml'.")

    voting_system.run_ranked_voting()
    voting_system.display_final_results(voting_system.vote_percentages)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ranked Voting System")
    parser.add_argument("input_folder", type=str, help="Path to the main folder containing the input file.")
    parser.add_argument("file_name", type=str, help="Name of the input file (without the extension).")
    parser.add_argument("file_format", choices=["csv", "yaml"], help="File format ('csv' or 'yaml').")
    parser.add_argument("--intermediate", action="store_true", help="Display intermediate results.")
    args = parser.parse_args()
    main(args)
