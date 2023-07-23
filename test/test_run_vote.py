import pytest
from RankedVoting import RankedVoting


@pytest.fixture
def ranked_voting():
    candidates = ["Candidate 1", "Candidate 2", "Candidate 3"]
    voters = {
        "Voter 1": {"Candidate 1": 1, "Candidate 2": 2, "Candidate 3": 3},
        "Voter 2": {"Candidate 1": 2, "Candidate 2": 1, "Candidate 3": 3},
        "Voter 3": {"Candidate 1": 3, "Candidate 2": 2, "Candidate 3": 1}
    }
    return RankedVoting(candidates, voters)


def test_run_vote(ranked_voting):
    ranked_voting.run_vote()
    vote_history = ranked_voting.vote_history

    # Verify the structure of the vote_history DataFrame
    assert 'round' in vote_history.columns
    assert 'removed' in vote_history.columns
    assert 'vote_counts' in vote_history.columns

    # Verify that all rounds are accounted for
    assert vote_history['round'].tolist() == list(range(1, len(ranked_voting.candidates) + 1))

    # Verify that the removed candidates.yaml are correct
    assert vote_history['removed'].iloc[0] == ['Candidate 2']  # The candidate with the lowest votes in the first round
    assert vote_history['removed'].iloc[1] == [
        'Candidate 1']  # The remaining candidate with the lowest votes in the second round

    # Verify the winner (the candidate in the last round)
    final_round_votes = vote_history['vote_counts'].iloc[-1]
    assert max(final_round_votes, key=final_round_votes.get) == 'Candidate 3'
