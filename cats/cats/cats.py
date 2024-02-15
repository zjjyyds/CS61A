"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime
import string

###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    select_par = [p for p in paragraphs if select(p)]

    assert k>=0 ,"k is negative"
    if k < len(select_par):
        return select_par[k]
    else:
        return ""
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph):
        # 段落处理，小写和去符号
        paragraph=paragraph.lower()
        for punc in string.punctuation:
            paragraph = paragraph.replace(punc,'')
        words = paragraph.split()
        for word in words:
            if word in topic:
                return True
        return False

    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed_words) == 0:
        return 0.0
    matchs = 0
    for i in range(min(len(typed_words),len(reference_words))):
        if typed_words[i]==reference_words[i]:
            matchs += 1

    return matchs/len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    num_chars = len(typed)
    num_words = num_chars / 5
    elapsed_minutes = elapsed / 60

    return num_words / elapsed_minutes
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word

    # Find the word with the minimum difference using the diff_function
    min_diff_word = min(valid_words, key=lambda word: diff_function(user_word, word, limit))

    # Check if the minimum difference is within the limit
    if diff_function(user_word, min_diff_word, limit) <= limit:
        return min_diff_word
    else:
        return user_word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit < 0:
        return limit + 1

    if len(start) == 0:
        return len(goal)
    elif len(goal) == 0:
        return len(start)

    if start[0] != goal[0]:
        diff = 1 + shifty_shifts(start[1:], goal[1:], limit - 1)
        return diff if diff <= limit else limit + 1
    else:
        return shifty_shifts(start[1:], goal[1:], limit)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if limit < 0:
        return limit + 1

    if start == goal:
        return 0
    elif len(goal) == 0:
        return len(start)
    elif len(start) == 0:
        return len(goal)

    if start[0] == goal[0]:
        return pawssible_patches(start[1:], goal[1:], limit)

    add_diff = 1 + pawssible_patches(start, goal[1:], limit - 1)
    remove_diff = 1 + pawssible_patches(start[1:], goal, limit - 1)
    substitute_diff = 1 + pawssible_patches(start[1:], goal[1:], limit - 1)

    diffs = [add_diff, remove_diff, substitute_diff]
    min_diff = min(diffs)

    return min_diff if min_diff <= limit else limit + 1
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct_count = 0
    total_words = min(len(typed), len(prompt))

    for i in range(total_words):
        if typed[i] == prompt[i]:
            correct_count += 1
        else:
            break  # Stop counting as soon as an incorrect word is encountered

    progress = correct_count / len(prompt)

    # Create a dictionary with id and progress
    progress_dict = {'id': user_id, 'progress': progress}

    # Send the progress dictionary to the multiplayer server
    send(progress_dict)

    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    # BEGIN PROBLEM 9
    time = []  # Initialize an empty list to store time data

    # Iterate over each player's timestamps
    for player_times in times_per_player:
        player_time = []  # Initialize an empty list for each player's time data
        start_time = player_times[0]  # Get the start time for the player

        # Iterate over each word's timestamp for the current player
        for i in range(1, len(player_times)):
            # Calculate the time difference and append it to the player's time list
            player_time.append(player_times[i] - start_time)
            start_time = player_times[i]  # Update the start time for the next word

        time.append(player_time)  # Append the player's time list to the overall time list

    # Create a game using the game constructor with words and time data
    game_data = game(words, time)

    return game_data
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    words = all_words(game)
    times = all_times(game)
    player_count = len(times)

    fastest_words = []

    for player in range(player_count):

        player_fastest = []

        for word in range(len(words)):

            player_time = time(game, player, word)

            # Get min time and min player
            min_time, min_player = min([(time(game, p, word), p) for p in range(player_count)])

            if player_time == min_time and player <= min_player:
                player_fastest.append(word_at(game, word))

        fastest_words.append(player_fastest)

    return fastest_words
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)