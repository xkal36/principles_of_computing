"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

import holds_testsuite
import simpletest

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set



def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    return max([(hand.count(num) * num) for num in hand])


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    all_poss_hands = map(lambda hand: held_dice + hand, gen_all_sequences(range(1, num_die_sides + 1), num_free_dice))
    all_poss_scores = map(score, all_poss_hands)
    return (sum(all_poss_scores) + 0.0) / (len(all_poss_scores) + 0.0)
  

    
def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in range(r)[::-1]:
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_subsets = []
    for dummy_i in range(0, len(hand) + 1):
        subsets = combinations(hand, dummy_i)
        for subset in subsets:
            all_subsets.append(subset)
    return set(all_subsets)


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_expected = 0
    to_hold = None
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        expected_val = expected_value(hold, num_die_sides, num_free_dice)
        
        if expected_val > max_expected:
            max_expected = expected_val
            to_hold = hold
            
    return (max_expected, to_hold)
        
        
def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    

 

def run_test_suite():
    # Create a TestSuite object:
    suite = simpletest.TestSuite()
    
    
    # Testing score function:
    suite.run_test(score((1, 1, 1, 1, 1)), 5, "Test #1:")
    suite.run_test(score((5, 5, 5, 5, 5)), 25, "Test #2")
    suite.run_test(score((1, 1, 6, 1, 1)), 6, "Test #3")
    suite.run_test(score((1, 1, 5, 1, 1)), 5, "Test #4")
    suite.run_test(score((1, 1, 4, 1, 1)), 4,"Test #5")
    suite.run_test(score((1, 1, 3, 3, 1)), 6,"Test #6:")
    suite.run_test(score((1, 1, 6, 1, 6)), 12,"Test #7:")
    suite.run_test(score((1, 5, 3, 1, 2)), 5,"Test #8:")
    suite.run_test(score((1, 1, 1, 2, 2)), 4,"Test #9:")
    suite.run_test(score((5, 5, 6, 6, 1)), 12,"Test #10:")
    
    suite.run_test(gen_all_holds((5, 5, 5, 6, 6)), 
                   set([(), (5, 5, 5, 6), (5, 5, 5, 6, 6), (5, 5, 6), (5, 5, 5), (5,), (5, 5), (6,), (5, 6), (5, 5, 6, 6), (6, 6), (5, 6, 6)]), "Test #11:")
    
    
    # Collect and report results:
    suite.report_results()


# Simple tests:
run_test_suite()
holds_testsuite.run_suite(gen_all_holds)

# Main function:
run_example()