import pytest
from RankedVoting import RankedVoting



@pytest.fixture
def ranked_voting():
    candidates = ["Candidate 1", "Candidate 2", "Candidate 3", "Candidate 4"]
    voters_data = {}
    return RankedVoting(candidates, voters_data)


def test_redistribute_votes(ranked_voting):
    # Setup
    candidate_to_remove = "Candidate 3"
    ranked_voting.candidates = {
        "Candidate 1": 0, 
        "Candidate 2": 0, 
        "Candidate 3": 0, 
        "Candidate 4": 0
    }
    ranked_voting.voters = {
        "Voter 1": {"Candidate 1": 1, "Candidate 3": 2, "Candidate 4": 3},
        "Voter 2": {"Candidate 1": 1, "Candidate 2": 2},
        "Voter 3": {"Candidate 3": 1, "Candidate 2": 2, "Candidate 4": 3},
        "Voter 4": {"Candidate 3": 1}
    }
    # Call the method to be tested
    ranked_voting.redistribute_votes(candidate_to_remove)
    # Check the voters' preferences after redistribution
    assert ranked_voting.voters == {
        "Voter 1": {"Candidate 1": 1, "Candidate 4": 3},
        "Voter 2": {"Candidate 1": 1, "Candidate 2": 2},
        "Voter 3": {"Candidate 2": 2, "Candidate 4": 3}
    }

