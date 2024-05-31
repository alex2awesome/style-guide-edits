# style_guide_rule_title= 'Noun gender'
# style_guide_rule = "English nouns have no true gender, as that property is understood in many other languages. For example, whether a noun refers to a masculine or feminine person or thing does not determine the form of the accompanying article as it does in French, German, Spanish, and many other languages. Still, some English words—almost exclusively nouns denoting people or animals—are inherently masculine {uncle} {rooster} {lad} or feminine {aunt} {hen} {lass} and take the gender-appropriate pronouns. But most English nouns are common in gender and may refer to either sex {relative} {chicken} {child}. Many words once considered strictly masculine—especially words associated with jobs and professions—have been accepted as common (or indefinite) in gender over time {author} {executor} {proprietor}. Similarly, many forms made feminine by the addition of a suffix {aviatrix} {poetess} have been essentially abandoned."
n = 20
ZERO_SHOT_PAIR_SYNTHETIC_DATA = """You are a journalist's assistant.
Here is a rule from the Chicago Manual of Style that either captures a grammatical inaccuracy, or a changing style:

The title of this rule is: "{style_guide_rule_title}"

The rule is:

```{style_guide_rule}```

If you cannot identify a clear rule or linguistic preference expressed, say "No clear rule or preference expressed".
If you are able to identify a clear rule or linguistic preference expressed, 
write me {n} examples of pairs of two sentences: one that VIOLATES this rule ("bad sentence") 
and one corrected version of the same sentence ("good sentence") that DOES NOT violate this rule. 
Make them topically sound like news-article sentences: they should be about current events, or similar news writing.
Respond with a list of {n} python dictionaries, each with the keys "bad sentence", "good sentence".

Don't say anything else.
"""

ZERO_SHOT_BAD_SYNTHETIC_DATA = """You are a journalist's assistant.
Here is a rule from the Chicago Manual of Style that either captures a grammatical inaccuracy, or a changing style:

The title of this rule is: "{style_guide_rule_title}"

The rule is:

```{style_guide_rule}```

If you cannot identify a clear rule or linguistic preference expressed, say "No clear rule or preference expressed".
If you are able to identify a clear rule or linguistic preference expressed, 
write me {n} examples of sentences that VIOLATES these rules in different ways. 
Make them topically sound like news-article sentences: they should be about current events, or similar news writing.
Respond with a python list.

Don't say anything else.
"""

ZERO_SHOT_COT_BAD_SYNTHETIC_DATA = """You are a helpful editor's assistant. I am trying to read a style guide. Here is an entry in the style guide:

Title: {style_guide_rule_title}

```{style_guide_rule}```

The entry might specify a generic grammar definition, a specific rule, a specific spelling, or something else.
If the rule contains just a single word, it is likely demonstrating the correct spelling of that word.

I want examples of sentences that this would be applicable to.

Let's think about this step-by-step. 
1. Is there a rule being expressed? 
2. Is this rule something that can be violated?

If the answer to 1 or 2 is No, then say "No clear rule or preference expressed." and STOP.

If the answer to 1 and 2 is Yes, then:
3. Simplify the rule in plain language and specify ways it can be broken.
(Note: if it is a spelling rule, to violate it, simply misspell the word).

Then, generate {n} example sentences that violate this rule. Don't worry about them sounding wrong.
Make them topically sound like news-article sentences: they should be about current events, or similar news writing.
The example sentences in A PYTHON LIST. Don't output in any other format.
"""


ZERO_SHOT_PAIRED_CHECK = """Please check my work. I used the following editing rule:

```{rule_title}.

{rule}```

And I edited the following {k} sentences:
{sentences}

Did I do a good job? For each sentence, answer one of three answers: [yes, no, unclear]. Don't say anything else. 
Answer "yes" if and ONLY if the rule is correctly applied. In other words: (1) The OLD sentence VIOLATES this rule. (2) The NEW sentence DOES NOT VIOLATE this rule.
Answer "no" if the rule does NOT apply to the edit.
"unclear" if the rule doesn't make sense as a editing rule."""

######## parsing prompts
FEW_SHOT_DICT_PARSING_PROMPT = """Can you help me correct the formatting of this malformed JSON? Return just the correctly formatted JSON list, with all the information
correctly copied. 

Example 1: Input:
1. {{'key_1': 'a', 'key_2': 'b'}}
2. {{'key_3': 'c', 'key_4': 'd'}}

return:
[{{'key_1': 'a', 'key_2': 'b'}}, {{'key_3': 'c', 'key_4': 'd'}}]

Example 2: Input:
[{{'key_1': 'a', 'key_2': 'b'

return
[{{'key_1': 'a', 'key_2': 'b'}}]

Now it's your turn. Do NOT return ANYTHING besides the JSON string.

{json_str}
"""

FEW_SHOT_LIST_PARSING_PROMPT = """Can you help me correct the formatting of this malformed JSON? Return just the correctly formatted JSON list, with all the information
correctly copied. 

Example 1: Input:
1. example item
2. example another item

return:
['example item', 'example another item']

Example 2: Input:
[
    'example item'
    'example another item'
]

return
['example item', 'example another item']

Now it's your turn. Do NOT return ANYTHING besides a correct JSON string.

{json_str}
"""


######## checking prompts
ZERO_SHOT_SINGLE_PAIRWISE_SEMANTIC_CHECK = """Please check this work. I followed this editing rule:

```{rule_title}

{rule}```

To edit this bad sentence:
```{b}```

Into this good one: 
```{g}```

Did I do a good job? Answer one of three answers: [yes, no, unclear]. Don't say anything else.
Answer "yes" if and ONLY if the rule is correctly applied. In other words: (1) The OLD sentence VIOLATES this rule. (2) The NEW sentence DOES NOT VIOLATE this rule.
Answer "no" if the rule does NOT apply to the edit.
"unclear" if the rule doesn't make sense as a editing rule."""

ZERO_SHOT_BATCH_PAIRWISE_SEMANTIC_CHECK = """Please check my work. I used the following editing rule:

```{rule_title}.

{rule}```

And I edited the following {k} sentences:
{sentences}

Did I do a good job? For each sentence, answer one of three answers: [yes, no, unclear]. Don't say anything else. 
Answer "yes" if and ONLY if the rule is correctly applied. In other words: (1) The OLD sentence VIOLATES this rule. (2) The NEW sentence DOES NOT VIOLATE this rule.
Answer "no" if the rule does NOT apply to the edit.
"unclear" if the rule doesn't make sense as a editing rule."""

ZERO_SHOT_BATCH_BAD_SENTENCE_SEMANTIC_CHECK = """Does the following editing rule:

```{rule_title}.

{rule}```

Apply to the following sentences:
{sentences}

For each sentence, answer one of three answers: [yes, no, unclear]. Don't say anything else. 
Answer "yes" if and ONLY if the rule does apply and the sentence VIOLATES this rule.
Answer "no" if the rule does NOT apply to the edit or the sentence does NOT violate this rule.
"unclear" if the rule doesn't make sense as a editing rule or is too vague."""