# Ranked Voting System

The Ranked Voting System is a method for conducting elections where voters rank candidates in order of preference. This system allows voters to express their preferences more accurately, and it helps in electing candidates who have broader support.

## Getting Started

### Requirements

- Python 3.8+
- pandas
- PyYAML

To install the requirements, use the provided `install.sh` (for Unix-based systems) or `install.bat` (for Windows) scripts, or manually install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the Ranked Voting System, execute the main Python script, providing the path to the main folder containing the input files (CSV or YAML) as a command-line argument. The script will conduct the ranked voting process and display the final results.

### Running the Code
To run the code, use the following command:

```bash
python main.py <input_file> --display_interim <True/False> --interim_filename <interim_filename> --final_filename <final_filename>
```
where:
- <input_file> is the path to the input file in either YAML or CSV format.
- <True/False> is a Boolean indicating whether to display interim step results. The default is False.
- <interim_filename> is the filename for saving interim step results. The default is "interim_results.json".
- <final_filename> is the filename for saving final results. The default is "final_results.json".

#### Example
```bash
python main.py Example/yaml/example.yaml --display_interim True --interim_filename interim.json --final_filename final.json
```

## Expected Formats

### CSV Format

- The CSV file should contain the candidates' names in the first row and the voters' names in the first column.
- The cells in the middle represent the rank given by each voter to each candidate.
- An empty cell represents that the voter did not rank that particular candidate.
- If a voter ranked multiple candidates with the same rank, the values can be repeated in the corresponding cells.

Example CSV file:

```cvs
| Voter    | Candidate A | Candidate B | Candidate C |
|----------|-------------|-------------|-------------|
| Voter 1  | 1           | 2           |  3          |
|----------|-------------|-------------|-------------|
| Voter 2  |             | 2           |  1          |
|----------|-------------|-------------|-------------|
| Voter 3  | 1           |             |             |
|----------|-------------|-------------|-------------|
| Voter 4  | 3           | 1           |  2          |
|----------|-------------|-------------|-------------|
```

### YAML Format

- The main folder should contain a `candidates.yaml` file and one YAML file for each voter, e.g., `voter1.yaml`, `voter2.yaml`, etc.
- The `candidates.yaml` file should contain a list of candidate names.
- Each voter YAML file should contain a list of dictionaries, where each dictionary represents the voter's preferences.
- Each dictionary should have a `"Voter"` key with the voter's name and other keys representing the candidate names with corresponding ranks.
- An empty value or absence of a rank for a candidate means that the voter did not rank that particular candidate.

Example candidates.yaml:

```yaml
- Candidate A
- Candidate B
- Candidate C
```
Example voter1.yaml:
```yaml
- Voter: Voter 1
  Candidate A: 1
  Candidate B: 3
  Candidate C: 2
```
Example voter2.yaml:
```yaml
- Voter: Voter 2
  Candidate B: 2
  Candidate C: 1
```
Example voter3.yaml:
```yaml
- Voter: Voter 3
  Candidate A: 1
```
Example voter4.yaml:
```yaml
- Voter: Voter 4
  Candidate A: 3
  Candidate B: 1
  Candidate C: 2
```