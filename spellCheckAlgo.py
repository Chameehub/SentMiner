# Input text
import enchant
from difflib import SequenceMatcher


# Get Similarity ratio between two words
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Remove Vowals
def anti_vowel(text):
    vow = ["a", "e", "i", "o", "u"]
    chars = []

    for i in text: #No need of the two separate loops
        if i.lower() not in vow:
            chars.append(i)

    return "".join(chars)


def wordPrediction(word, suggestList, languageReference):

    coreWordComparingDictionary = {}
    vowalRemovedWordComparingDectionary = {}

    for suggestedWord in suggestList:

        dictionary1 = {suggestedWord:similar(word,suggestedWord)}
        coreWordComparingDictionary.update(dictionary1)

        dictionary2 = {suggestedWord:similar(anti_vowel(word),anti_vowel(suggestedWord))}
        vowalRemovedWordComparingDectionary.update(dictionary2)





# suggest new word
def noSuggestionPrediction(word, languageReference):
    # empty suggest list to be filled by meanwhile
    suggestList = []

    # English prefixes list
    # key : prefixes || value : short form of language
    prefixList = {'ante': 'ant', 'anti': 'ant'}

    # English Suffixes list
    suffixesList = {}

    # Iterate Prefixes List
    for key in prefixList:

        # get length of short form prefix value
        valeLength = prefixList[key].__len__()

        # get first n characters from given word
        wordFirstCharacters = word[:valeLength]

        # Compare the similarity between given n characters of list and actual word
        if wordFirstCharacters == prefixList[key]:
            # Remove and add new corrected prefixes
            newWordpre = word[valeLength:]
            newWordpre = key + newWordpre
            suggestList.extend(languageReference.suggest(newWordpre))

    for key in suffixesList:

        # get length of short form suffixes value
        valeLength = suffixesList[key].__len__()

        # get last n characters from given word
        wordLastCharacters = word[-valeLength:]

        # Compare the similarity between given n characters of list and actual word
        if wordLastCharacters == suffixesList[key]:
            newWordsuf = word[:-valeLength]
            newWordsuf = newWordsuf + key

            suggestList.extend(languageReference.suggest(newWordsuf))

    return wordPrediction(word,suggestList,languageReference)


text = "helo my nme is Chameera"

# Iterate word through the comment
for word in text.split():
    print(word)

    # Initialize language in to US English
    # Import Personal word list to identify human name in local Context
    languageReference = enchant.DictWithPWL("en_US", "srilanka_namelist.txt")

    # Check whether the spellings are correct
    if (languageReference.check(word)):
        print("true")

    else:
        word = "gvnment"
        suggestList = languageReference.suggest(word)
        suggestList = []
        if suggestList.__len__() == 1:
             text.replace(word,suggestList[0])


        elif suggestList.__len__() == 0:
            text.replace(word, noSuggestionPrediction(word, languageReference))

        else:
            text.replace(word,wordPrediction(word,suggestList,languageReference))

        print(suggestList)
