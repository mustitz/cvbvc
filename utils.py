"""
This module provides utility functions.

It includes a function to format a list of numbers into a human-readable
range string, combining consecutive numbers into ranges.
"""

def format_ranges(numbers):
    """
    Formats a list of integers into a string of ranges.

    Consecutive numbers are grouped into ranges separated by a dash.
    Non-consecutive numbers are listed individually.

    Args:
        numbers (list of int): The sorted list of numbers without dups to format.

    Returns:
        str: A string representing the formatted ranges.
    """
    numbers = sorted(numbers)
    if not numbers:
        return ""

    ranges = []
    start = numbers[0]
    end = numbers[0]

    for i in range(1, len(numbers)):
        if numbers[i] == end + 1:
            end = numbers[i]
        else:
            if start == end:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{end}")
            start = numbers[i]
            end = numbers[i]

    if start == end:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{end}")

    return ", ".join(ranges)
