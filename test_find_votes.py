import pytest
from RankedVoting import RankedVoting


@pytest.fixture
def ranked_voting():
    return RankedVoting()


def test_add_vote(ranked_voting):
    # Test adding a vote with valid candidate preferences
    ranked_voting.candidates = {'Candidate A': 0, 'Candidate B': 0}
    ranked_voting.voters = {}
    vote_preferences = {'Candidate B': 1, 'Candidate A': 2}

    # Add the vote
    ranked_voting.add_vote(vote_preferences)

    # Check that candidates have been added to the system
    assert 'Candidate A' in ranked_voting.candidates
    assert 'Candidate B' in ranked_voting.candidates

    # Check that the vote has been added to voters
    assert len(ranked_voting.voters) == 1
    voter_id = list(ranked_voting.voters.keys())[0]
    assert ranked_voting.voters[voter_id] == vote_preferences


def test_add_vote_invalid_candidate(ranked_voting):
    # Test adding a vote with an invalid candidate
    ranked_voting.candidates = {'Candidate A': 0}
    ranked_voting.voters = {}
    vote_preferences = ['Candidate B', 'Candidate A']

    # Check that adding the vote raises a ValueError
    with pytest.raises(ValueError, match="Candidate 'Candidate B' does not exist. Add the candidate first."):
        ranked_voting.add_vote(vote_preferences)




if __name__ == '__main__':
    pytest.main()
