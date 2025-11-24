"""
6.101 Lab:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!

import string  # optional import

# import pprint  # optional import

# import typing # optional import
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    """
    Stores a condensed mapping from word strings to values.
    """

    def __init__(self):
        # Initialize a new node:
        # `value` is None if no word ends here, 
        # otherwise stores the word's associated value.
        self.value = None
        # `children` is a dictionary mapping a (str)
        # to another PrefixTree node.
        self.children = {}

    def __setitem__(self, word, value):
        """
        Mutates the tree so that the word is associated with the given value.
        Raises a TypeError if the given word is not a string.
        """

        if not isinstance(word, str):
            raise TypeError from None
        # Start traversal from the root node.
        current_node = self
        for char in word:
            # For each character, get the child node or create a new node.
            current_node = current_node.children.setdefault(char, PrefixTree())

        # After iterating through the word, set the value at the final node.
        current_node.value = value

    def __getitem__(self, word):
        """
        Returns the value for the specified word.
        Raises a KeyError if the given word is not in the tree.
        Raises a TypeError if the given word is not a string.
        """
        # This dunder method allows using the `value = tree[word]` syntax.
        if not isinstance(word, str):
            raise TypeError from None
        current_node = self
        # Navigate down the tree following the characters in the word.
        for char in word:
            if char not in current_node.children:
                raise KeyError from None
            current_node = current_node.children[char]

        # If the word path exists but no value is set raise KeyError.
        if current_node.value is None:
            raise KeyError from None
        return current_node.value

    def __contains__(self, word):
        """
        Returns a boolean indicating whether the given word has a set value in the tree.
        Raises a TypeError if the given key is not a string.
        """

        if not isinstance(word, str):
            raise TypeError from None
        current_node = self
        val = True
        # Traverse the tree, similar to __getitem__
        for char in word:
            current_node = current_node.children.get(char, None)
            # If the path breaks, the word isn't in the tree.
            if current_node is None:
                val = False
                break
        # Check that the path exists *and* a value is set at the end.
        if val and (current_node.value is None):
            val = False
        return val

    def __iter__(self):
        """
        Generator that yields tuples of all the (word, value) pairs in the tree.
        """

        # Implements iteration (e.g., `for word, val in tree`). Uses a recursive helper.
        def helper_recur(current_node, out=""):
            value_new = current_node.value
            # If the current node represents a complete word, yield it.
            if value_new is not None:
                yield out, value_new

            # Recursively explore all children, appending the character to out
            for node_key, node in current_node.children.items():
                yield from helper_recur(node, out + node_key)

        # Start the recursion from the root node (self).
        yield from helper_recur(self)

    def inc(self, word, inc_val=1):
        """A custom helper method to increment the value (frequency) of a word."""
        current_node = self
        for char in word:
            current_node = current_node.children.setdefault(char, PrefixTree())

        val = current_node.value
        # If the word wasn't in the tree, initialize its count to 0.
        if val is None:
            current_node.value = 0
        current_node.value += inc_val

    def get_item_small(self, word):
        """A helper to get the *node* at the end of a prefix, not just the value."""
        if not isinstance(word, str):
            raise TypeError from None
        current_node = self
        for char in word:
            # If the prefix doesn't exist, return None.
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node

    def __delitem__(self, word):
        """
        Deletes the value of the given word from the tree.
        Raises a KeyError if the given word does not exist.
        Raises a TypeError if the given word is not a string.
        """
        # This dunder method allows using the `del tree[word]` syntax.
        if not isinstance(word, str):
            raise TypeError from None
        current_node = self
        # Traverse the tree to find the node corresponding to the word.
        for char in word:
            if char not in current_node.children:
                raise KeyError from None
            current_node = current_node.children[char]
        # If the word exists as a prefix but not as a stored value, raise KeyError.
        if current_node.value is None:
            raise KeyError from None
        # "Delete" the word by setting its value back to None.
        current_node.value = None


def word_frequencies(text):
    """
    Given a piece of text as a single string, creates and returns a prefix tree whose
    keys are the words that appear in the text, and whose values are the number of times
    the associated word appears in the text.
    """
    # This function builds a frequency-counting PrefixTree from a raw text string.
    tree = PrefixTree()
    # Process the text one sentence at a time.
    sentence_build = tokenize_sentences(text)
    for sentence in sentence_build:
        word = ""
        # Manually build words by iterating through characters.
        for char in sentence:
            if char != " ":
                word += char
                continue
            # When a space is hit, increment the count for the completed word.
            tree.inc(word)
            word = ""
        tree.inc(word)
    return tree


def autocomplete(tree, prefix, max_count=None):
    """
    Returns the set of the most-frequently occurring words that start with the given
    prefix string in the given tree. Includes only the top max_count most common words
    if max_count is specified, otherwise returns all auto-completions.
    """
    # Find the node corresponding to the end of the prefix.
    tree_pref = tree.get_item_small(prefix)
    if tree_pref is None:
        return set()
    # `pref_dict` will store {frequency: {set_of_words}}.
    pref_dict = {}
    result = set()

    # Case 1: We need to find the top `max_count` words.
    if max_count is not None:
        # Iterate through all words *descending* from the prefix node.
        for key, val in tree_pref:
            pref_dict.setdefault(val, set())
            pref_dict[val].add(key)
        count = 0

        # Iterate through the frequencies from highest to lowest.
        for val in sorted(pref_dict.keys())[::-1]:
            for word in pref_dict[val]:
                check = max_count <= count
                # Stop once we have reached `max_count` words.
                if check:
                    break

                count += 1
                # Add the full word (prefix + suffix) to the result set.
                result.add(prefix + word)

            if check:
                break

    else:
        # Case 2: `max_count` is None, so return all completions.
        for key, val in tree_pref:
            result.add(prefix + key)
    return result


def generate_edits(word):
    """
    Generates and yields all the possible ways to edit the given word string consisting
    entirely of lowercase letters in the range from "a" to "z".

    An edit for a word can be any one of the following:
    * A single insertion (add a single letter from "a" to "z" anywhere in the word)
    * A single deletion  (remove any one character from the word)
    * A single replacement (replace any one character in the word with a character in
      the range "a" to "z")
    * A two-character transpose (switch the positions of any two adjacent characters)

    Must be a generator! May output duplicate edits or the original word.
    """
    alphabet = string.ascii_lowercase
    for index in range(len(word)):
        # Generate all single DELETIONS.
        yield word[0:index] + word[index + 1 :]
        # Generate all two-character TRANSPOSES.

        yield (
            word[0:index]
            + word[index + 1 : index + 2 if index < len(word) - 1 else index + 1]
            + word[index]
            + word[index + 2 :]
        )
        for char in alphabet:
            # Generate all single REPLACEMENTS.
            yield word[0:index] + char + word[index + 1 :]
            # Generate all single INSERTIONS (before the current character).
            yield word[0:index] + char + word[index:]
    for char in alphabet:
        # Generate all single INSERTIONS (at the very end of the word).
        yield word + char


def autocorrect(tree, prefix, max_count=None):
    """
    Returns the set of words that represent valid ways to autocorrect the given prefix
    string. Starts by including auto-completions. If there are fewer than max_count
    auto-completions (or if max_count is not specified), then includes the
    most-frequently occurring words that differ from prefix by a small edit, up to
    max_count total elements (or all elements if max_count is not specified).
    """
    result = set()
    # Get standard autocomplete suggestions first.
    main_edit = autocomplete(tree, prefix, max_count)
    count = 0

    check = False
    # Add the valid autocomplete suggestions to the result, honoring max_count.
    for edit in main_edit:
        check = count >= max_count if max_count is not None else False
        if check:
            break
        if (edit not in result) and (edit in tree):
            result.add(edit)
            count += 1
    # If we hit max_count with just autocomplete, we're done.
    if check:
        return result
    # If we still need more suggestions, generate extra words.
    pref_dict = {}
    # Find all generated edits that are *actually* in the tree.
    for word in generate_edits(prefix):
        val_word = tree.get_item_small(word)
        val = val_word.value if val_word is not None else None
        pref_dict.setdefault(val, [])
        pref_dict[val].append(word)

    # Remove edits that were not found in the tree (value is None).
    del pref_dict[None]
    # Iterate through the valid edits, from most to least frequent.
    for num in sorted(pref_dict.keys())[::-1]:
        for edit in pref_dict[num]:
            check = count >= max_count if max_count is not None else False
            # Add valid edits to the result until max_count is reached.
            if check:
                break
            if edit not in result:
                result.add(edit)
                count += 1
        if check:
            break
    return result


def satisfy_pattern(word, pattern):
    """This function checks if a `word` matches a
    `pattern` with wildcards '?' and '*'"""

    def help_recur(index, index_small):
        # Both word and pattern are exhausted.(return 2).
        if (index == len(word)) and (index_small == len(pattern)):
            return 2
        # Word is exhausted. Match if remaining pattern is all '*' (return 2).
        if index == len(word):
            if all(p == "*" for p in pattern[index_small:]):
                return 2
            # If word is exhausted but pattern isn't all '*',
            # it's a potential prefix match (return 1).
            return 1
        # Base case 3: Pattern is exhausted but word is not.
        # This is not a match (return 0).
        if index_small == len(pattern):
            return 0

        # Handle '*': Try matching '*' as an empty
        # string OR as one-or-more characters.
        if pattern[index_small] == "*":
            # Run both recursive calls and store their results
            res_empty = help_recur(index, index_small + 1)
            res_char = help_recur(index + 1, index_small)

            # Return 2 (full match) if *either* path finds a full match.
            if res_empty == 2 or res_char == 2:
                return 2
            # If no full match, check if either path found a potential match
            # Return 1 (prefix match) if *either* path finds a prefix match.
            if res_empty == 1 or res_char == 1:
                return 1
            # If both returned False, return False
            return 0

        # Handle '?': Match any single character.
        # Consume one char from both and continue.
        if pattern[index_small] == "?":
            return help_recur(index + 1, index_small + 1)
        # Handle standard characters: If they don't match,
        # it's a failed path (return 0).
        if word[index] != pattern[index_small]:
            return 0

        return help_recur(index + 1, index_small + 1)

    # Start the recursion from the beginning of both strings.
    return help_recur(0, 0)


def word_filter(tree, pattern):
    """This function finds all words in the tree that match the given pattern."""
    prefix = ""
    result = set()

    def recur_help(prefix, tree):
        # Check if the *current prefix* matches the pattern.
        pattern_val = satisfy_pattern(prefix, pattern)

        # If 0, the prefix doesn't match, so prune this branch (stop recursing).
        if pattern_val > 0:
            # If 2, it's a full match. If a word ends here, add it to results.
            if pattern_val == 2 and tree.value is not None:
                result.add(prefix)
            # If 1 or 2, it's a potential prefix, so continue exploring children.
            for prefix_new, tree_new in tree.children.items():
                recur_help(prefix + prefix_new, tree_new)

    recur_help(prefix, tree)
    return result


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # doctest.run_docstring_examples( # runs doctests for one function
    #   PrefixTree.__getitem__,
    #   globals(),
    #   optionflags=_doctest_flags,
    #   verbose=True
    # )
    # tree = PrefixTree()
    # tree['bat'] = 0
    # tree['bark'] = ':)'
    # tree['bar'] = 3
    # tree[''] = 7

    # #print(counter)
    # tree['bank'] = 4
    # #print(counter)
    # print('bar' in tree)
    # print('barking' in tree)
    # #print(tree.children)
    # #for key, val in tree:
    # #   print(f'{key=}')
    # new = word_frequencies("bat bat bark bar")
    # tree = word_frequencies("bat bat bark bar")  # tree from Figure 2
    # print(autocomplete(tree, "ba", 1))
    # print(autocomplete(tree, "ba", 2))
    # print(autocomplete(tree, "be", 2))
    # print(autocomplete(tree, "b"))
    # run = [1,2]
    # print(run[3:])
    # edits4 = set(generate_edits('bark'))
    # print(len(edits4) )
    # print(autocomplete(tree, 'bark'))
    # print(autocorrect(tree, "bar"))
    # print(autocorrect(tree, "bar", 2))
    # print(word_filter(tree, "bat"))
    # tree = word_frequencies("bat bat bark bar")  # tree from Figure 2
    # print(word_filter(tree, "ba"))
    # tree = word_frequencies("bat bat bark bar")
    # print(word_filter(tree, "???"))

    # if __name__ == "__main__":
    # Main execution block to test the `word_filter` function.
    # tree = word_frequencies("bat bat bark bar")
    # print(word_filter(tree, "*r*"))

    files = {
        "metamorphosis": "Metamorphosis by Franz Kafka.txt",
        "two_cities": "A Tale of Two Cities by Charles Dickens.txt",
        "alice": "Alice's Adventures in Wonderland by Lewis Carroll.txt",
        "pride": "Pride and Prejudice by Jane Austen.txt",
        "dracula": "Dracula by Bram Stoker.txt",
    }

    with open(files["metamorphosis"], encoding="utf-8") as f:
        text_metamorphosis = f.read()
    tree_metamorphosis = word_frequencies(text_metamorphosis)

    with open(files["two_cities"], encoding="utf-8") as f:
        text_two_cities = f.read()
    tree_two_cities = word_frequencies(text_two_cities)

    with open(files["alice"], encoding="utf-8") as f:
        text_alice = f.read()
    tree_alice = word_frequencies(text_alice)

    with open(files["pride"], encoding="utf-8") as f:
        text_pride = f.read()
    tree_pride = word_frequencies(text_pride)

    with open(files["dracula"], encoding="utf-8") as f:
        text_dracula = f.read()
    tree_dracula = word_frequencies(text_dracula)

    q1_answer = autocomplete(tree_metamorphosis, "gre", 6)
    print(f"\nQ1 (Metamorphosis, 'gre', top 6): \n{q1_answer}\n")

    q2_answer = word_filter(tree_metamorphosis, "c*h")
    print(f"Q2 (Metamorphosis, 'c*h'): \n{q2_answer}\n")

    q3_answer = word_filter(tree_two_cities, "r?c*t")
    print(f"Q3 (A Tale of Two Cities, 'r?c*t'): \n{q3_answer}\n")

    q4_answer = autocorrect(tree_alice, "hear", 12)
    print(f"Q4 (Alice, 'hear', top 12): \n{q4_answer}\n")

    q5_answer = autocorrect(tree_pride, "hear")
    print(f"Q5 (Pride & Prejudice, 'hear', all): \n{q5_answer}\n")
    q6_answer = len(list(tree_dracula))
    print(f"Q6 (Dracula, distinct words): \n{q6_answer}\n")
    q7_answer = sum(val for key, val in tree_dracula)
    print(f"Q7 (Dracula, total words): \n{q7_answer}\n")
