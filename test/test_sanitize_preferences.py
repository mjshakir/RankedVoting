import pytest
from RankedVoting import RankedVoting

@pytest.fixture
def ranked_voting():
    return RankedVoting(['A', 'B', 'C'], {})

def test_sanitize_preferences(ranked_voting):

    # Test with integer preferences
    preferences = {'A': 1, 'B': 2, 'C': 3}
    expected_output = {'A': 1, 'B': 2, 'C': 3}
    assert ranked_voting._sanitize_preferences(preferences) == expected_output

    # Test with float preferences
    preferences = {'A': 1.5, 'B': 2.4, 'C': 3.6}
    expected_output = {'A': 2, 'B': 2, 'C': 4}  # Rounded to the nearest integer
    assert ranked_voting._sanitize_preferences(preferences) == expected_output

    # Test with string preferences
    preferences = {'A': '1', 'B': 2, 'C': '3'}
    expected_output = {'A': float('inf'), 'B': 2, 'C': float('inf')}  # Strings replaced with infinity
    assert ranked_voting._sanitize_preferences(preferences) == expected_output

    # Test with zero preferences
    preferences = {'A': 0, 'B': 2, 'C': 3}
    expected_output = {'B': 2, 'C': 3}  # Candidate A removed
    assert ranked_voting._sanitize_preferences(preferences) == expected_output
