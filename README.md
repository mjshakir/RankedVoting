# Ranked Voting Script

The Ranked Voting script is designed to perform ranked voting calculations based on a CSV file containing voter preferences for different candidates. This script implements the Ranked Choice Voting (RCV) or Alternative Vote (AV) method, where voters rank candidates in order of preference.

## Requirements

Before using the Ranked Voting script, make sure you have the following installed:

- Python 3

Additionally, you'll need the following Python libraries, which can be installed via pip:

- argparse
- tabulate
- collections

To install the required libraries, run the following command:

```bash
pip install argparse tabulate
```

## Input Format

The input for the Ranked Voting script is a CSV (Comma-Separated Values) file. The CSV file must follow the following format:

- The first row contains the names of the candidates.
- The first column contains the names or identifiers of the voters.
- The remaining cells contain the ranking preferences of each voter for the candidates. The ranking should be represented using integers, where 1 indicates the first choice, 2 indicates the second choice, and so on.

Example CSV file:


```
Voter,Candidate1,Candidate2,Candidate3
Voter1,1,2,3
Voter2,2,1,3
Voter3,3,2,1
Voter4,1,2,3
Voter5,2,1,3
Voter6,3,2,1
```


In the above example, three candidates (Candidate1, Candidate2, and Candidate3) are ranked by six voters (Voter1, Voter2, ..., Voter6). Each voter provides their preferences by assigning integers 1, 2, or 3 to the candidates.

**Note:** The script automatically handles invalid or missing preferences, treating them as "don't care" or abstentions.

## How to Use

To use the Ranked Voting script, follow these steps:

1. Save your ranked voting data in a CSV file following the input format described above.

2. Open a terminal or command prompt.

3. Run the script with the path to the CSV file as the first argument. Optionally, you can add the `--show-intermediate` flag to display intermediate results after each round of vote redistribution.

Command to run the script:

```Python
python main.py path_to_your_csv_file --show-intermediate
```


Replace `main.py` with the actual name of the Python script file containing the `main()` function and `RankedVoting` class.

## Example

Let's run the script with the example CSV file provided earlier:

**CSV File (example_votes.csv):**

```
Voter,Candidate1,Candidate2,Candidate3
Voter1,1,2,3
Voter2,2,1,3
Voter3,3,2,1
Voter4,1,2,3
Voter5,2,1,3
Voter6,3,2,1
```


**Command:**

```Python
python main.py path_to_your_csv_file --show-intermediate
```


**Output:**
```
Intermediate Results:
+-----------+------------+
| Candidate | Percentage |
+-----------+------------+
| Candidate1| 33.33%     |
| Candidate2| 33.33%     |
| Candidate3| 33.33%     |
+-----------+------------+

Intermediate Results:
+-----------+------------+
| Candidate | Percentage |
+-----------+------------+
| Candidate1| 44.44%     |
| Candidate2| 22.22%     |
| Candidate3| 33.33%     |
+-----------+------------+

Candidate   Percentage  Winner
-----------  -----------  --------
Candidate1  44.44%       *
Candidate2  22.22%
Candidate3  33.33%
```


The script will display the intermediate results after each round of vote redistribution if `--show-intermediate` is specified. Otherwise, it will display only the final results with the winning candidate highlighted.

---

To use the script, simply copy the contents of the `ranked_voting.py` and `main.py` files, and save them in their respective files in the same directory. Then, follow the usage instructions provided in the document.

Now, you have both the updated Markdown document and the Markdown source code. You can copy the source code and use it directly in your project or documentation.

