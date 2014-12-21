import re

def make_matcher(rule):
    def _(input):
        # simply split on non-words
        split_input = re.split(r'\W+', input)
        print split_input
        return rule(split_input)
    return _

def match(word):
    def _(input):
        return word in input
    return _

def _any(*rules):
    def _(input):
        return any([rule(input) for rule in rules])
    return _

def _all(*rules):
    def _(input):
        return all([rule(input) for rule in rules])
    return _

def _match_n(num_matches, *rules):
    if type(num_matches) != int:
        raise Exception("first argument to match_n must be a number")
    def _(input):
        true_values = filter(None, [rule(input) for rule in rules])
        return len(true_values) == num_matches
    return _

def _not(rule):
    def _(input):
        return not rule(input)
    return _


def test():
    """I just watched the extended version of all the LotR movies and it
    has temporarily seeped into numerous elements of my existence...

    """
    print "enemy matching"
    enemy_matcher = make_matcher(_any(match("orc"), match("saurumon")))
    assert enemy_matcher("I am, gandalf") == False
    assert enemy_matcher("I am an orc") == True
    assert enemy_matcher("I am saurumon but not an orc") == True

    team_matcher = make_matcher(_match_n(1,
                                        _all(match("frodo"), match("samwise")),
                                        _all(match("pippin"), match("mery"))))

    assert team_matcher("santa and samwise") == False
    assert team_matcher("pippin and samwise") == False
    assert team_matcher("frodo and samwise") == True
    assert team_matcher("frodo and samwise and mary and pippin") == True

    always_good_hobbits = make_matcher(_all(_any(match("samwise"),
                                                 match("pippin"),
                                                 match("mary")),
                                            _not(match("frodo"))))
    assert always_good_hobbits("me and samwise") == True
    assert always_good_hobbits("frodo and samwise") == False
    assert always_good_hobbits("maryanne and the captain too") == False


if __name__ == '__main__':
    test()
