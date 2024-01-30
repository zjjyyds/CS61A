def swine_align(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Swine Align.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> swine_align(30, 45)  # The GCD is 15.
    True
    >>> swine_align(35, 45)  # The GCD is 5.
    False
    """
    # BEGIN PROBLEM 4a
    if player_score == 0 or opponent_score == 0:
        return False

    # 辗转相除法（Euclidean Algorithm）
    def GCD(a, b):
        while b:
            a, b = b, a % b
        return a

    if GCD(player_score, opponent_score) >= 10:
        return True
    else:
        return False


result = swine_align(3, 4)
print(result)  # 应该输出 False
