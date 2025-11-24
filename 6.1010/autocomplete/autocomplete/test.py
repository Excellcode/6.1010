"""
6.101 Lab:
Autocomplete
"""

#!/usr/bin/env python3
import os.path
import lab
import json
import types
import pickle
import string

import sys
sys.setrecursionlimit(10000)

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


# convert prefix tree into a dictionary...
def dictify(t):
    assert set(t.__dict__) == {'value', 'children'}, "PrefixTree instances should only contain the two instance attributes mentioned in the lab writeup."
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out

# ...and back
def from_dict(d):
    t = lab.PrefixTree()
    for k, v in d.items():
        t[k] = v
    return t

# make sure the keys are not explicitly stored in any node
def any_key_stored(tree, keys):
    keys = [tuple(k) for k in keys]
    for i in dir(tree):
        try:
            val = tuple(getattr(tree, i))
        except:
            continue
        for j in keys:
            if j == val:
                return repr(i), repr(j)
    for child in tree.children:
        if len(child) != 1:
            return repr(child), repr(child)
    for child in tree.children.values():
        key_stored = any_key_stored(child, keys)
        if key_stored:
            return key_stored
    return None

# read in expected result
def read_expected(fname):
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', fname), 'rb') as f:
        return pickle.load(f)

def test_set():
    t = lab.PrefixTree()
    t['cat'] = 'kitten'
    t['car'] = 'tricycle'
    t['carpet'] = 'rug'
    expect = read_expected('1.pickle')
    assert dictify(t) == expect, "Your prefix tree is incorrect."
    assert any_key_stored(t, ('cat', 'car', 'carpet')) is None

    t = lab.PrefixTree()
    t['a'] = 1
    t['an'] = 1
    t['ant'] = 0
    t['anteater'] = 1
    t['ants'] = 1
    t['a'] = 2
    t['an'] = 2
    t['a'] = 3
    expect = read_expected('2.pickle')
    assert dictify(t) == expect, "Your prefix tree is incorrect."
    assert any_key_stored(t, ('an', 'ant', 'anteater', 'ants')) is None
    with pytest.raises(TypeError):
        t[(1, 2, 3)] = 20

    t = lab.PrefixTree()
    t['man'] = ''
    t['mat'] = 'object'
    t['mattress'] = ()
    t['map'] = 'pam'
    t['me'] = 'you'
    t['met'] = 'tem'
    t['a'] = '?'
    t['map'] = -1000
    expect = read_expected('3.pickle')
    assert dictify(t) == expect, "Your prefix tree is incorrect."
    assert any_key_stored(t, ('man', 'mat', 'mattress', 'map', 'me', 'met', 'map')) is None
    with pytest.raises(TypeError):
        t['something',] = 'pam'

    t = lab.PrefixTree()
    t[''] = 'hello'
    expected = {'value': "hello", 'children': {}}
    assert dictify(t) == expected, "Your prefix tree is incorrect."


def test_get():
    d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39, 'children': 0}
    t = from_dict(d)
    assert dictify(t) == read_expected('person.pickle')
    for k in d:
        assert t[k] == d[k], f'Expected key {repr(k)} to have value {repr(d[k])}, got {repr(t[k])}'

    assert any_key_stored(t, tuple(d)) is None
    t[''] = 5
    assert t[''] == 5

    c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige', 'storage space': ''}
    t = from_dict(c)
    assert dictify(t) == read_expected('car.pickle')
    assert all(t[k] == c[k] for k in c)
    assert any_key_stored(t, tuple(c)) is None
    for i in ('these', 'keys', 'dont', 'exist', 'storage'):
        with pytest.raises(KeyError):
            x = t[i]
    with pytest.raises(TypeError):
        x = t[(1, 2, 3)]


def test_contains():
    d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39, 'children': 0}
    t = from_dict(d)
    assert dictify(t) == read_expected('person.pickle')
    for k in d:
        assert k in t, f'Expected key {repr(k)} to be in tree!'

    with pytest.raises(TypeError):
        (1, 2, 3) in t

    c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige', 'storage space': ''}
    t = from_dict(c)
    assert dictify(t) == read_expected('car.pickle')
    for k in c:
        assert k in t, f'Expected key {repr(k)} to be in tree!'


    badkeys = ('these', 'keys', 'dont', 'exist', 'm', 'ma', 'mak', 'mo',
               'mod', 'mode', 'ye', 'yea', 'y', '', 'car.pickle',)
    for k in badkeys:
        assert k not in t, f'key {repr(k)} should not be in tree!'

    assert '' not in t  # this key has no value in the tree

    t[''] = 0
    assert '' in t      # now it should have a value


def test_iter():
    t = lab.PrefixTree()
    t['man'] = ''
    t['mat'] = 'object'
    t['mattress'] = ()
    t['map'] = 'pam'
    t['me'] = 'you'
    t['met'] = 'tem'
    t['a'] = '?'
    t['map'] = -1000
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    expected = [('a', '?'), ('man', ''), ('map', -1000), ('mat', 'object'),
                ('mattress', ()), ('me', 'you'), ('met', 'tem')]
    assert sorted(list(t)) == expected

    t = lab.PrefixTree()
    t[''] = ()
    t['a'] = 0
    t['ab'] = set()
    t['abc'] = []
    t['abcd'] = ''
    t['abcde'] = False
    t['ad'] = True
    expected = [('', ()), ('a', 0), ('ab', set()), ('abc', []), ('abcd', ''),
                ('abcde', False), ('ad', True)]
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    assert sorted(list(t)) == expected



def test_delete():
    c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige', 'storage space': ''}
    t = from_dict(c)
    assert dictify(t) == read_expected('car.pickle')
    del t['color']
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    with pytest.raises(KeyError):
        del t['color'] # can't delete again
    assert set(t) == set(c.items()) - {('color', 'beige')}
    t['color'] = 'silver'  # new paint job
    for i in t:
        if i[0] != 'color':
            assert i in c.items()
        else:
            assert i[1] == 'silver'

    for i in ('cat', 'dog', 'ferret', 'tomato'):
        with pytest.raises(KeyError):
            del t[i]

    with pytest.raises(TypeError):
        del t[1,2,3]

    t = lab.PrefixTree()
    t['man'] = ''
    t['mat'] = 'object'
    t['mattress'] = ()
    t['map'] = 'pam'
    t['me'] = 'you'
    t['met'] = 'tem'
    t['a'] = '?'
    t['map'] = -1000
    t[''] = 500
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    expected = [('', 500), ('a', '?'), ('man', ''), ('map', -1000),
                ('mat', 'object'), ('mattress', ()), ('me', 'you'), ('met', 'tem')]
    assert sorted(list(t)) == expected
    del t['mat']
    del t['']
    expected = [('a', '?'), ('man', ''), ('map', -1000),
                ('mattress', ()), ('me', 'you'), ('met', 'tem')]
    assert sorted(list(t)) == expected



def test_word_frequencies():
    # small test
    l = lab.word_frequencies('toonces was a cat who could drive a car very fast until he crashed.')
    assert dictify(l) == read_expected('6.pickle')

    l = lab.word_frequencies('a man at the market murmered that he had met a mermaid. '
                           'mark didnt believe the man had met a mermaid.')
    assert dictify(l) == read_expected('7.pickle')

    l = lab.word_frequencies('what happened to the cat who had eaten the ball of yarn?  she had mittens!')
    assert dictify(l) == read_expected('8.pickle')



@pytest.mark.parametrize('bigtext', ['holmes', 'earnest', 'frankenstein'])
def test_big_corpora(bigtext):
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', '%s.txt' % bigtext), encoding='utf-8') as f:
        text = f.read()
        w = lab.word_frequencies(text)

        w_e = read_expected('%s_words.pickle' % bigtext)

        assert w_e == dictify(w), 'word frequencies prefix tree does not match for %s' % bigtext


def test_autocomplete_small():
    # Autocomplete on simple prefix trees with less than N valid words

    tree = lab.word_frequencies("cat car carpet")
    prefix, max_count = 'car', 3
    result = lab.autocomplete(tree, prefix, max_count)
    expected = {"car", "carpet"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocomplete(tree, '{prefix}', {max_count})", result, expected)

    tree = lab.word_frequencies("a an ant anteater a an ant a")
    prefix, max_count = 'a', 2
    result = lab.autocomplete(tree, prefix, max_count)
    assert result in [{"a", "an"}, {"a", "ant"}], f"autocomplete(tree, '{prefix}', {max_count}) got {result=}"

    tree = lab.word_frequencies("man mat mattress map me met a man a a a map man met")
    prefix, max_count = 'm', 3
    result = lab.autocomplete(tree, prefix, max_count)
    expected = {"man", "map", "met"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocomplete(tree, '{prefix}', {max_count})", result, expected)

    tree = lab.word_frequencies("hello helm history")
    prefix, max_count = 'help', 3
    result = lab.autocomplete(tree, prefix, max_count)
    expected = set()
    passed = result == expected
    assert passed, make_set_error_message(f"autocomplete(tree, '{prefix}', {max_count})", result, expected)


def test_autocomplete_big_1():
    a = string.ascii_lowercase

    word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
    word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
    word_list.append("bruteforceisbad")

    tree = lab.word_frequencies(' '.join(word_list))
    inp_out = {
        ('ap', 1): {'apple'},
        ('ap', 2): {'apple', 'apricot'},
        ('ap', 3): {'apple', 'apricot', 'application'},
        ('ap', None): {'apple', 'apricot', 'application'},
        ('b', None): {'bruteforceisbad'}
    }


    for _ in range(50_000):
        for (prefix, max_count), expected in inp_out.items():
            result = lab.autocomplete(tree, prefix, max_count)
            passed = result == expected
            assert passed, make_set_error_message(f"autocomplete(tree, '{prefix}', {max_count})", result, expected)


def test_autocomplete_big_2():
    inp = {'t': [0, 1, 25, None],
            'th': [0, 1, 21, None],
            'the': [0, 5, 21, None],
            'thes': [0, 1, 21, None]}

    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    tree = lab.word_frequencies(text)
    for prefix in sorted(inp):
        for max_count in inp[prefix]:
            result = lab.autocomplete(tree, prefix, max_count)
            expected = read_expected(f'frank_autocomplete_{prefix}_{max_count}.pickle')
            passed = result == expected
            assert passed, make_set_error_message(f"autocomplete(tree, '{prefix}', {max_count})", result, expected)


def test_autocomplete_big_3():
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    frankenstein_tree = lab.word_frequencies(text)
    the_word = 'accompany'
    for ix in range(len(the_word)+1):
        prefix, max_count = the_word[:ix], None
        result = lab.autocomplete(frankenstein_tree, prefix)
        expected = read_expected(f'frank_autocomplete_{prefix}_{max_count}.pickle')
        passed = result == expected
        assert passed, make_set_error_message(f"autocomplete(frankenstein_tree, '{prefix}', {max_count})", result, expected)


def test_generate_edits_small():
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', "generate_small_edits.pickle"), 'rb') as f:
        inp_out = pickle.load(f)

    for word, expected in inp_out.items():
        edit_gen = lab.generate_edits(word)
        assert isinstance(edit_gen, types.GeneratorType), f"Expected generate_edits({word}) to return a generator but got {type(edit_gen)}"
        result = set(edit_gen)
        passed = result == expected
        assert passed, make_set_error_message(f"generate_edits('{word}')", result, expected)


def test_generate_edits_big():
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', "generate_big_edits.pickle"), 'rb') as f:
        inp_out = pickle.load(f)

    for word, expected in inp_out.items():
        edit_gen = lab.generate_edits(word)
        assert isinstance(edit_gen, types.GeneratorType), f"Expected generate_edits({word}) to return a generator but got {type(edit_gen)}"
        result = set(edit_gen)
        passed = result == expected
        assert passed, make_set_error_message(f"generate_edits('{word}')", result, expected)


def test_autocorrect_small_1():
    # Autocorrect on cat in small text
    tree = lab.word_frequencies("cats cats cattle hat car cat act act at chat crate act car act")

    # find all corrections
    prefix = 'cat'
    result = lab.autocorrect(tree, prefix)
    expected = {"act", "car", "cats", "cat", "cattle", "chat", "at", "hat"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocorrect(tree, '{prefix}')", result, expected)

    # take completions first
    result = lab.autocorrect(tree, prefix, 3)
    expected = {"cat", "cats", "cattle"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocorrect(tree, '{prefix}', 3)", result, expected)

    # take completions + two most frequent corrections
    result = lab.autocorrect(tree, prefix, 5)
    expected = {"act", "car", "cat", "cats", "cattle"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocorrect(tree, '{prefix}', 5)", result, expected)



def test_autocorrect_small_2():
    # Autocorrect on ant in small text
    tree = lab.word_frequencies("a art at art at art anteater ants ants ants ants")
    prefix = 'ant'

    expected = {"anteater", "art", "at", "ants"}
    result = lab.autocorrect(tree, prefix)
    passed = result == expected
    assert passed, make_set_error_message(f"autocorrect(tree, '{prefix}')", result, expected)


    # take the autocompletions first
    result = lab.autocorrect(tree, prefix, 2)
    expected = {"anteater", "ants"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocorrect(tree, '{prefix}', 2)", result, expected)

    # take completions then fill remaining slots with edits sorted by frequency
    result = lab.autocorrect(tree, 'ant', 3)
    expected = {"anteater", "ants", "art"}
    passed = result == expected
    assert passed, make_set_error_message(f"autocorrect(tree, '{prefix}', 3)", result, expected)



def test_autocorrect_big():
    inp = {'thin': [0, 8, 10, None],
            'tom': [0, 2, 4, None],
            'mon': [0, 2, 15, 17, 20, None]}
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    frankenstein_tree = lab.word_frequencies(text)
    for prefix in sorted(inp):
        for count in inp[prefix]:
            result = lab.autocorrect(frankenstein_tree, prefix, count)
            expected = read_expected('frank_autocorrect_%s_%s.pickle' % (prefix, count))
            passed = result == expected
            assert passed, make_set_error_message(f'autocorrect(frankenstein_tree, "{prefix}", {count})', result, expected)


def test_filter_word():
    # words can contain any characters
    tree = lab.word_frequencies("1 man mat mattress map me met a man a a a map man met")

    # select specific words from the prefix tree
    result = lab.word_filter(tree, 'a')
    assert result == {"a"}, f"word_filter(tree, 'a') got an unexpected result!"

    result = lab.word_filter(tree, '1')
    assert result == {"1"}, f"word_filter(tree, '1') got an unexpected result!"

    result = lab.word_filter(tree, 'me')
    assert result == {"me"}, f"word_filter(tree, 'me') got an unexpected result!"

    result = lab.word_filter(tree, 'mattress')
    assert result == {"mattress"}, f"word_filter(tree, 'mattress') got an unexpected result!"

    # patterns that don't exist in the prefix tree
    tree = lab.word_frequencies("1 man mat mattress map me met a man a a a map man met")

    result = lab.word_filter(tree, 'mattresses')
    assert result == set(), f"word_filter(tree, 'mattresses') got an unexpected result!"

    result = lab.word_filter(tree, 'ma')
    assert result == set(), f"word_filter(tree, 'ma') got an unexpected result!"

    result = lab.word_filter(tree, '!')
    assert result == set(), f"word_filter(tree, '!') got an unexpected result!"

    result = lab.word_filter(tree, 'wh' + 'ee'*6_000)
    assert result == set()

    # handle empty word?
    tree = lab.word_frequencies("1 man mat mattress map me met a man a a a map man met")

    result = lab.word_filter(tree, '')
    assert result == set(), f"word_filter(tree, '') got an unexpected result!"

    tree[''] = 5
    result = lab.word_filter(tree, '')
    assert result == {''}, f"word_filter(tree, '') got an unexpected result!"


def test_filter_question():
    tree = lab.word_frequencies("I met a man with a mat who followed a map. The map led to more maps, 5 cats, and a bat.")
    # single letter words that exist
    pattern = '?'
    expected = {"5", "a", "i"}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    pattern = 'ma?'
    expected = {"man", "map", "mat"}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    pattern = '???s'
    expected = {"cats", "maps"}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    pattern = '??t'
    expected = {"bat", "mat", "met"}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    tree = lab.word_frequencies("I met a man with a mat who followed a map. The map led to more maps, 5 cats, and a bat.")
    pattern = '???'
    expected = {'map', 'man', 'led', 'met', 'bat', 'and', 'mat', 'the', 'who'}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    # non-existent patterns
    pattern = 'mat?'
    result = lab.word_filter(tree, pattern)
    assert result == set(), f"word_filter(tree, '{pattern}') got an unexpected result!"

    pattern = 'ca?'
    result = lab.word_filter(tree, pattern)
    assert result == set(), f"word_filter(tree, '{pattern}') got an unexpected result!"

    pattern = 't??????????'
    result = lab.word_filter(tree, pattern)
    assert result == set(), f"word_filter(tree, '{pattern}') got an unexpected result!"

    pattern = 'i?'
    result = lab.word_filter(tree, pattern)
    assert result == set(), f"word_filter(tree, '{pattern}') got an unexpected result!"

    pattern = '?o?'
    result = lab.word_filter(tree, pattern)
    assert result == set(), f"word_filter(tree, '{pattern}') got an unexpected result!"

    pattern = 'm'+'?'*11_000
    result = lab.word_filter(tree, pattern)
    assert result == set()


def test_filter_small():
    # Get all words
    tree = lab.word_frequencies("man mat mattress map me met a man a a a map man met")
    pattern = '*'
    expected = {'a', 'map', 'mattress', 'man', 'met', 'me', 'mat'}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    # All three-letter words
    pattern = '???'
    expected = {'map', 'man', 'met', 'mat'}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    # Words beginning with 'mat'
    pattern = 'mat*'
    expected = {'mattress', 'mat'}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    # Words beginning with 'm', third letter is 't'
    pattern = 'm?t*'
    expected = {"mat", "mattress", "met"}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    # Words with at least 4 letters
    pattern = '????*'
    expected = {"mattress"}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)

    # All words
    tree = lab.word_frequencies("man mat mattress map me met a man a a a map man met")
    tree[''] = 5
    pattern = '**'
    expected = {'', 'a', 'map', 'mattress', 'man', 'met', 'me', 'mat'}
    result = lab.word_filter(tree, pattern)
    passed = result == expected
    assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)


def test_filter_big_1():
    a = string.ascii_lowercase

    word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
    word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
    word_list.append("bruteforceisbad")

    tree = lab.word_frequencies(' '.join(word_list))
    expected = {'apple', 'application', 'apricot'}
    pattern = "ap*"

    for _ in range(1000):
        result = lab.word_filter(tree, pattern)
        passed = result == expected
        assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)


def test_filter_big_2():
    patterns = ('*ing', '*ing?', '****ing', '**ing**', '????', 'mon*',
                '*?*?*?*', '*???')
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()

    tree = lab.word_frequencies(text)
    for ix, pattern in enumerate(patterns):
        result = lab.word_filter(tree, pattern)
        expected = read_expected('frank_filter_%s.pickle' % (ix, ))
        passed = result == expected
        assert passed, make_set_error_message(f"word_filter(tree, '{pattern}')", result, expected)


def make_set_error_message(header, result, expected):
    msg = f'result = {header} != expected set of words\n'
    msg += f'{len(result) = } {"and" if len(result) == len(expected) else "but"} {len(expected) = }\n'
    msg += '------------------------------------\n'
    if not isinstance(result, set):
        msg += f'Expected result to be a set but got {type(result)=}!'
        return msg
    elif len(expected) < 10:
        expected_items = ", ".join(repr(x) for x in sorted(expected))
        try:
            result_items = ", ".join(repr(x) for x in sorted(result))
        except:
            result_items = ", ".join(repr(x) for x in result)
        msg += f'result contained: {result_items}\nbut expected had: {expected_items}\n'
        return msg

    missing = expected - result
    if missing:
        # chop missing to 5 words to make it readable
        short_missing = set(sorted(missing, reverse=True)[:5])
        msg += f'result has {len(missing)} missing word{"s" if len(missing) > 1 else ""}'
        msg += f'\nmissing_words_included = {short_missing}\n'
        msg += '------------------------------------\n'

    extra = result - expected
    if extra:
        # chop extra to 5 words to make it readable
        try:
            short_extra = set(sorted(extra, reverse=True)[:5])
        except:
            short_extra = set(list(extra)[:5])
        msg += f'result has {len(extra)} extra word{"s" if len(extra) > 1 else ""}'
        msg += f'\nextra_words_included = {short_extra}\n'

    return msg

