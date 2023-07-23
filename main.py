import os
import argparse
from RankedVoting import RankedVotingFromYAML, RankedVotingFromCSV


def main():
    parser = argparse.ArgumentParser(description='Run a ranked voting system.')
    parser.add_argument('input_file', help='Path to the input file in either YAML or CSV format')
    parser.add_argument('--display_interim', default=False, action=argparse.BooleanOptionalAction,
                        help='Whether to display interim step results. Default is False.')
    parser.add_argument('--interim_filename', default='interim_results.csv',
                        help='The filename for saving interim step results. Default is "interim_results.json".')
    parser.add_argument('--final_filename', default='final_results.json',
                        help='The filename for saving final results. Default is "final_results.json".')

    args = parser.parse_args()

    if args.input_file.endswith('.yaml') or os.path.isdir(args.input_file):
        ranked_voting = RankedVotingFromYAML(args.input_file)
    elif args.input_file.endswith('.csv'):
        ranked_voting = RankedVotingFromCSV(args.input_file)
    else:
        raise ValueError('Unsupported file format. Please provide a YAML or CSV file.')

    ranked_voting.run_vote()

    # Display interim results if the argument is provided
    if args.display_interim:
        ranked_voting.display_interim_results()

    # Save interim results
    ranked_voting.save_results_to_csv(args.interim_filename)

    # Save final results
    ranked_voting.save_input_and_final_results(args.final_filename)



if __name__ == '__main__':
    main()
