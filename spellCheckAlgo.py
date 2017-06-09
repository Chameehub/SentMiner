# Input text
import enchant
from difflib import SequenceMatcher
import re
import operator


# Get Similarity ratio between two words
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Remove Vowals
def anti_vowel(text):
    vow = ["a", "e", "i", "o", "u"]
    chars = []

    for i in text:  # No need of the two separate loops
        if i.lower() not in vow:
            chars.append(i)

    return "".join(chars)


def wordPrediction(word, suggestList):
    coreWordComparingDictionary = {}
    vowalRemovedWordComparingDectionary = {}
    finalResult = {}

    for suggestedWord in suggestList:
        suggestedWord = suggestedWord.lower()
        dictionary1 = {suggestedWord: similar(word, suggestedWord)}
        coreWordComparingDictionary.update(dictionary1)

        dictionary2 = {suggestedWord: similar(anti_vowel(word), anti_vowel(suggestedWord))}
        vowalRemovedWordComparingDectionary.update(dictionary2)

    for suggestedWordList in suggestList:
        suggestedWordList = suggestedWordList.lower()
        valueMethod1 = coreWordComparingDictionary[suggestedWordList]

        valueMethod2 = vowalRemovedWordComparingDectionary[suggestedWordList]

        finalValue = (valueMethod1 + valueMethod2) / 2

        tempDictioary = {suggestedWordList: finalValue}
        finalResult.update(tempDictioary)

    try:
        output = max(finalResult, key=finalResult.get)
        if not output:
            output = word
    except ValueError:
        output = word

    output = output.replace(' ','')
    return output


# suggest new word
def noSuggestionPrediction(word,languageReference):
    # empty suggest list to be filled by meanwhile
    suggestList = []

    suggestList = languageReference.suggest(word)

    # English prefixes list
    # key : prefixes || value : short form of language
    prefixList = {'ante': 'ant', 'anti': 'ant', 'ante': 'ant', 'extra': 'extr', 'intra': 'intr', 'pre': 'pr',
                  'anti': 'ant',
                  'fore': 'fr', 'macro': 'mcr', 'circum': 'crcm', 'homo': 'hm', 'micro': 'mcro',
                  'semi': 'smi',
                  'hyper': 'hypr', 'mid': 'md', 'sub': 'sb', 'mis': 'ms', 'super': 'spr', 'dis': 'ds', 'mono': 'mn',
                  'non': 'nn',
                  'trans': 'trns', 'tri': 'tr', 'epi': 'ep', 'infra': 'infr', 'para': 'pr', 'inter': 'intr',
                  'post': 'pst'}

    # English Suffixes list
    suffixesList = {'ment': 'mnt', 'ise': 'is', 'ous': 'us', 'ize': 'z', 'ish': 'is', 'ance': 'nc', 'ness': 'ns',
                    'able': 'bl',
                    'ive': 'v', 'ence': 'nc', 'ship': 'sp', 'ible': 'bl', 'less': 'ls', 'dom': 'dm',
                    'sion': 'sn',
                    'tion': 'tn', 'esque': 'sq', 'ful': 'fl', 'ward': 'wrd', 'ism': 'sm', 'wards': 'wrds',
                    'ist': 'st',
                    'ify': 'fy', 'icalwise': 'clws', 'ity': 'ty', 'ious': 'is','tor':'tr'}

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

    return wordPrediction(word, suggestList)


text = ""

correctTest = ""
# text = "sri lnka"
# set input into lower case
text = text.lower()
# correctTest = correctTest.lower()

inputText = text
# Initialize language in to US English
# Import Personal word list to identify human name in local Context
languageReference = enchant.DictWithPWL("en_US", "srilanka_namelist.txt")
# Iterate word through the comment
for word in text.split():

    # Check whether the spellings are correct
    if not(languageReference.check(word)):

        suggetion = noSuggestionPrediction(word, languageReference)
        suggetion = suggetion.replace(" ", "")
        text = text.replace(word, suggetion)

print(text)
# wordOfOriginalText = inputText.count(" ") + 1
# textCount = text.count(" ") + 1
# print(wordOfOriginalText)
# print(textCount)



# def findAccuracy(text, correctText):
#     text = re.sub(r'[^A-Za-z\d\s]', '', text)
#     text = ''.join([i for i in text if not i.isdigit()])
#
#     correctText = re.sub(r'[^A-Za-z\d\s]', '', correctText)
#     correctText = ''.join([i for i in correctText if not i.isdigit()])
#
#     countText = text.count(" ") + 1
#     countCorrectText = correctText.count(" ") + 1
#
#     splittedText = text.split()
#     splittedOriginal = correctText.split()
#     accuracyVal = 0
#     count = 0
#
#     if splittedText.__len__() == splittedOriginal.__len__():
#         while count < splittedOriginal.__len__():
#             val = similar(splittedText[count],splittedOriginal[count])
#             if val == 1:
#                 accuracyVal += 1
#             count += 1
#
#     return accuracyVal/countCorrectText
#
# accuracy = findAccuracy(text,correctTest)
# print(accuracy)

