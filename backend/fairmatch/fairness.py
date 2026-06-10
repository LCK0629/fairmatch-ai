from __future__ import annotations


def calculate_total_satisfaction(satisfaction_scores: list[int]) -> int:
    return sum(satisfaction_scores)


def calculate_average_satisfaction(satisfaction_scores: list[int]) -> float:
    if not satisfaction_scores:
        return 0.0
    return calculate_total_satisfaction(satisfaction_scores) / len(satisfaction_scores)


def calculate_satisfaction_gap(satisfaction_scores: list[int]) -> int:
    if not satisfaction_scores:
        return 0
    return max(satisfaction_scores) - min(satisfaction_scores)


def calculate_max_min_value(satisfaction_scores: list[int]) -> int:
    if not satisfaction_scores:
        return 0
    return min(satisfaction_scores)


def calculate_gini_coefficient(satisfaction_scores: list[int]) -> float:
    if not satisfaction_scores:
        return 0.0

    total_satisfaction = calculate_total_satisfaction(satisfaction_scores)
    if total_satisfaction == 0:
        return 0.0

    score_count = len(satisfaction_scores)
    absolute_difference_sum = sum(
        abs(left_score - right_score)
        for left_score in satisfaction_scores
        for right_score in satisfaction_scores
    )
    return absolute_difference_sum / (2 * score_count * total_satisfaction)
