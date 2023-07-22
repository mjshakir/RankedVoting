# Import necessary modules and classes
import pytest
from RankedVoting import RankedVoting


# Part 1: Test redistribution with a single candidate
def test_redistribute_votes_single_candidate():
    # Create a new instance of RankedVoting
    ranked_voting = RankedVoting()

    # Add candidates to the RankedVoting object
    candidates_data = {'Candidate A'}
    ranked_voting.add_candidates(candidates_data)

    # Add voters to the RankedVoting object
    voters_data = {
        'Voter 1': {'Candidate A': 1},
        'Voter 2': {'Candidate A': 1},
        'Voter 3': {'Candidate A': 1},
    }

    for voter, ranked_preferences in voters_data.items():
        ranked_voting.add_vote(ranked_preferences)

    # Ensure that the initial vote counts are correct
    assert ranked_voting.candidates == {'Candidate A': 3}

    # Perform redistribution by eliminating 'Candidate A'
    ranked_voting.redistribute_votes('Candidate A')

    # Check the results after redistribution
    assert ranked_voting.candidates == {}
    assert ranked_voting.voters == {}

    # Try to redistribute votes again after all candidates have been eliminated
    ranked_voting.redistribute_votes('Candidate A')  # Should not raise any errors


# Part 2: Test redistribution with multiple candidates
def test_redistribute_votes_multiple_candidates():
    # Create a new instance of RankedVoting
    ranked_voting = RankedVoting()

    # Add candidates to the RankedVoting object
    candidates_data = {'Candidate A', 'Candidate B'}
    ranked_voting.add_candidates(candidates_data)

    # Add voters to the RankedVoting object
    voters_data = {
        'Voter 1': {'Candidate A': 1, 'Candidate B': 2},
        'Voter 2': {'Candidate A': 2, 'Candidate B': 1},
        'Voter 3': {'Candidate A': 1, 'Candidate B': 1},
    }

    for voter, ranked_preferences in voters_data.items():
        ranked_voting.add_vote(ranked_preferences)

    # Ensure that the initial vote counts are correct
    assert ranked_voting.candidates == {'Candidate A': 4, 'Candidate B': 4}

    # Perform redistribution by eliminating 'Candidate A'
    ranked_voting.redistribute_votes('Candidate A')

    # Check the results after redistribution
    assert ranked_voting.candidates == {'Candidate B': 4}
    assert ranked_voting.voters == {
        3: {'Candidate B': 1},
    }

    # Perform redistribution by eliminating 'Candidate B'
    ranked_voting.redistribute_votes('Candidate B')

    # Check the results after redistribution
    assert ranked_voting.candidates == {}
    assert ranked_voting.voters == {}

    # Try to redistribute votes again after all candidates have been eliminated
    ranked_voting.redistribute_votes('Candidate B')  # Should not raise any errors


# Part 3: Test redistribution with a more complex input
def test_redistribute_votes_complex_input():
    # Create a new instance of RankedVoting
    ranked_voting = RankedVoting()

    # Add candidates to the RankedVoting object
    candidates_data = {'Candidate A', 'Candidate B', 'Candidate C', 'Candidate D'}
    ranked_voting.add_candidates(candidates_data)

    # Add voters to the RankedVoting object
    voters_data = {
        'Voter 1': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3, 'Candidate D': 4},
        'Voter 2': {'Candidate A': 4, 'Candidate B': 3, 'Candidate C': 2, 'Candidate D': 1},
        'Voter 3': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 4, 'Candidate D': 3},
        'Voter 4': {'Candidate A': 3, 'Candidate B': 4, 'Candidate C': 1, 'Candidate D': 2},
        'Voter 5': {'Candidate A': 1, 'Candidate B': 3, 'Candidate C': 2, 'Candidate D': 4},
    }

    for voter, ranked_preferences in voters_data.items():
        ranked_voting.add_vote(ranked_preferences)

    # Ensure that the initial vote counts are correct
    assert ranked_voting.candidates == {'Candidate A': 11, 'Candidate B': 13, 'Candidate C': 12, 'Candidate D': 11}

    # Perform redistribution by eliminating 'Candidate A'
    ranked_voting.redistribute_votes('Candidate A')

    # Check the results after the first redistribution
    assert ranked_voting.candidates == {'Candidate B': 13, 'Candidate C': 11, 'Candidate D': 10}
    assert ranked_voting.voters == {
        2: {'Candidate B': 3, 'Candidate C': 2, 'Candidate D': 1},
        3: {'Candidate B': 1, 'Candidate C': 4, 'Candidate D': 3},
        4: {'Candidate B': 4, 'Candidate C': 1, 'Candidate D': 2},
    }

    # Perform redistribution by eliminating 'Candidate B'
    ranked_voting.redistribute_votes('Candidate B')

    # Check the results after the second redistribution
    assert ranked_voting.candidates == {'Candidate C': 10, 'Candidate D': 11}
    assert ranked_voting.voters == {
        2: {'Candidate C': 2, 'Candidate D': 1},
        3: {'Candidate C': 4, 'Candidate D': 3},
        4: {'Candidate C': 1, 'Candidate D': 2},
    }

    # Perform redistribution by eliminating 'Candidate C'
    ranked_voting.redistribute_votes('Candidate C')

    # Check the results after the third redistribution
    assert ranked_voting.candidates == {'Candidate D': 6}
    assert ranked_voting.voters == {
        2: {'Candidate D': 1},
        3: {'Candidate D': 3},
        4: {'Candidate D': 2},
    }

    # Perform redistribution by eliminating 'Candidate D'
    ranked_voting.redistribute_votes('Candidate D')

    # Check the results after the final redistribution
    assert ranked_voting.candidates == {}
    assert ranked_voting.voters == {}

    # Try to redistribute votes again after all candidates have been eliminated
    ranked_voting.redistribute_votes('Candidate D')  # Should not raise any errors


def test_redistribute_votes_original_input():
    # Create a new instance of RankedVoting
    ranked_voting = RankedVoting()

    # Add candidates to the RankedVoting object
    candidates_data = {'Candidate A', 'Candidate B', 'Candidate C'}
    ranked_voting.add_candidates(candidates_data)

    # Add voters to the RankedVoting object
    voters_data = {
        'Voter 1': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
        'Voter 2': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3},
        'Voter 3': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
        'Voter 4': {'Candidate A': 1, 'Candidate B': 3, 'Candidate C': 2},
        'Voter 5': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
    }

    for voter, ranked_preferences in voters_data.items():
        ranked_voting.add_vote(ranked_preferences)

    # Ensure that the initial vote counts are correct
    assert ranked_voting.candidates == {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 0}

    # Perform redistribution by eliminating 'Candidate C'
    ranked_voting.redistribute_votes('Candidate C')

    # Check the results after the first redistribution
    assert ranked_voting.candidates == {'Candidate A': 3, 'Candidate B': 3}
    assert ranked_voting.voters == {
        1: {'Candidate A': 1, 'Candidate B': 2},
        2: {'Candidate A': 2, 'Candidate B': 1},
        4: {'Candidate A': 1, 'Candidate B': 3},
        5: {'Candidate A': 2, 'Candidate B': 3},
    }

    # Perform redistribution by eliminating 'Candidate B'
    ranked_voting.redistribute_votes('Candidate B')

    # Check the results after the second redistribution
    assert ranked_voting.candidates == {'Candidate A': 4}
    assert ranked_voting.voters == {
        1: {'Candidate A': 1},
        2: {'Candidate A': 2},
        4: {'Candidate A': 1},
        5: {'Candidate A': 2},
    }

    # Perform redistribution by eliminating 'Candidate A'
    ranked_voting.redistribute_votes('Candidate A')

    # Check the results after the final redistribution
    assert ranked_voting.candidates == {}
    assert ranked_voting.voters == {}

    # Try to redistribute votes again after all candidates have been eliminated
    ranked_voting.redistribute_votes('Candidate A')  # Should not raise any errors

# Part 5: Test redistribution with the original input data after fixing the method


def test_redistribute_votes_original_input_after_fix():
    # Create a new instance of RankedVoting
    ranked_voting = RankedVoting()

    # Add candidates to the RankedVoting object
    candidates_data = {'Candidate A', 'Candidate B', 'Candidate C'}
    ranked_voting.add_candidates(candidates_data)

    # Add voters to the RankedVoting object
    voters_data = {
        'Voter 1': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
        'Voter 2': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3},
        'Voter 3': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
        'Voter 4': {'Candidate A': 1, 'Candidate B': 3, 'Candidate C': 2},
        'Voter 5': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
    }

    for voter, ranked_preferences in voters_data.items():
        ranked_voting.add_vote(ranked_preferences)

    # Ensure that the initial vote counts are correct
    assert ranked_voting.candidates == {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 0}

    # Perform redistribution by eliminating 'Candidate C'
    ranked_voting.redistribute_votes('Candidate C')

    # Check the results after the first redistribution
    assert ranked_voting.candidates == {'Candidate A': 2, 'Candidate B': 3}
    assert ranked_voting.voters == {
        1: {'Candidate A': 1, 'Candidate B': 2},
        2: {'Candidate A': 2, 'Candidate B': 1},
        4: {'Candidate A': 1, 'Candidate B': 3},
        5: {'Candidate A': 2, 'Candidate B': 3},
    }

    # Perform redistribution by eliminating 'Candidate B'
    ranked_voting.redistribute_votes('Candidate B')

    # Check the results after the second redistribution
    assert ranked_voting.candidates == {'Candidate A': 3}
    assert ranked_voting.voters == {
        1: {'Candidate A': 1},
        2: {'Candidate A': 2},
        4: {'Candidate A': 1},
        5: {'Candidate A': 2},
    }

    # Perform redistribution by eliminating 'Candidate A'
    ranked_voting.redistribute_votes('Candidate A')

    # Check the results after the final redistribution
    assert ranked_voting.candidates == {}
    assert ranked_voting.voters == {}

    # Try to redistribute votes again after all candidates have been eliminated
    ranked_voting.redistribute_votes('Candidate A')  # Should not raise any errors

# ... (other test cases remain unchanged)

def test_redistribute_votes_original_input_after_fix_with_numpy():
    # Create a new instance of RankedVoting
    ranked_voting = RankedVoting()

    # Add candidates to the RankedVoting object
    candidates_data = {'Candidate A', 'Candidate B', 'Candidate C'}
    ranked_voting.add_candidates(candidates_data)

    # Add voters to the RankedVoting object
    voters_data = {
        'Voter 1': {'Candidate A': 1, 'Candidate B': 2, 'Candidate C': 3},
        'Voter 2': {'Candidate A': 2, 'Candidate B': 1, 'Candidate C': 3},
        'Voter 3': {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 1},
        'Voter 4': {'Candidate A': 1, 'Candidate B': 3, 'Candidate C': 2},
        'Voter 5': {'Candidate A': 2, 'Candidate B': 3, 'Candidate C': 1},
    }

    for voter, ranked_preferences in voters_data.items():
        ranked_voting.add_vote(ranked_preferences)

    # Ensure that the initial vote counts are correct
    assert ranked_voting.candidates == {'Candidate A': 3, 'Candidate B': 2, 'Candidate C': 0}

    # Perform redistributions by eliminating 'Candidate C', 'Candidate B', and 'Candidate A'
    ranked_voting.redistribute_votes('Candidate C')
    ranked_voting.redistribute_votes('Candidate B')
    ranked_voting.redistribute_votes('Candidate A')

    # Check the results after the final redistributions
    assert ranked_voting.candidates == {}
    assert ranked_voting.voters == {}

    # Try to redistribute votes again after all candidates have been eliminated
    ranked_voting.redistribute_votes('Candidate A')  # Should not raise any errors



if __name__ == '__main__':
    pytest.main()
