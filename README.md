# Ranked Voting System

The Ranked Voting System is a method for conducting elections where voters rank candidates in order of preference. This system allows voters to express their preferences more accurately, and it helps in electing candidates who have broader support.

## Usage

To run the Ranked Voting System, execute the main Python script, providing the path to the main folder containing the input files (CSV or YAML) as a command-line argument. The script will conduct the ranked voting process and display the final results.

The script provides the following options:

- `input_folder`: Path to the main folder containing the input files (candidates.yaml for YAML option or the CSV file for CSV option).
- `file_name`: Name of the input file (without the extension).
- `file_format`: File format ('csv' or 'yaml').
- `--intermediate`: (Optional) Display intermediate results during the ranked voting process.

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
## Examples

### Example 1: Using CSV Format

To run the Ranked Voting System using a CSV file, execute the following command:

```bash
python main.py path/to/main_folder example_csv csv
```
- `path/to/main_folder`: Replace this with the path to the main folder containing the CSV file.
- `example_csv`: Replace this with the name of the CSV file (without the extension).
- `csv`: Indicates that the input file format is CSV.


### Example 2: Using YAML Format

To run the Ranked Voting System using YAML files, execute the following command:

```bash
python main.py path/to/main_folder example_yml yaml
```

- `path/to/main_folder`: Replace this with the path to the main folder containing the candidates.yaml and voter YAML files.
- `example_yml: Replace` this with the name of the main folder.
- `yaml`: Indicates that the input file format is YAML.