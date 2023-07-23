import pytest
from RankedVoting import RankedVoting


@pytest.fixture
def ranked_voting():
    candidates = ["Candidate 1", "Candidate 2", "Candidate 3", "Candidate 4"]
    voters = {
        "Voter 1": {"Candidate 1": 1, "Candidate 2": 2, "Candidate 3": 3, "Candidate 4": 4},
        "Voter 2": {"Candidate 1": 2, "Candidate 2": 1, "Candidate 3": 4, "Candidate 4": 3},
        "Voter 3": {"Candidate 1": 4, "Candidate 2": 3, "Candidate 3": 2, "Candidate 4": 1},
        "Voter 4": {"Candidate 1": 3, "Candidate 2": 4, "Candidate 3": 1, "Candidate 4": 2}
    }
    return RankedVoting(candidates, voters)


def test_calculate_vote_counts(ranked_voting):
    # Setup
    ranked_voting.candidates = {
        "Candidate 1": 0,
        "Candidate 2": 0,
        "Candidate 3": 0,
        "Candidate 4": 0
    }
    ranked_voting.voters = {
        "Voter 1": {"Candidate 1": 1, "Candidate 3": 2, "Candidate 4": 3},
        "Voter 2": {"Candidate 1": 0, "Candidate 2": 1, "Candidate 3": 2},
        "Voter 3": {"Candidate 3": 1, "Candidate 2": 0, "Candidate 4": 2},
        "Voter 4": {"Candidate 4": 1, "Candidate 2": 2, "Candidate 3": 3}
    }

    # Call the method to be tested
    vote_counts = ranked_voting.calculate_vote_counts()

    # Check the vote count for each candidate
    assert vote_counts == {
        "Candidate 1": 1,
        "Candidate 2": 1,
        "Candidate 3": 1,
        "Candidate 4": 1
    }
