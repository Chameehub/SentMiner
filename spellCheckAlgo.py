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


text = "The gvnmnt initiatvs in dvlpmnt of tursm dte bk to 1937 whn the cyln turst burau ws estblshd. 7 hwevr, it ws clsd dwn in sptmbr 1939 due to wrld wr ¡¡. Aftr sr lnkas indpndnc the prmotion of tursm ws agin cnsidrd by reestablishng the cylon turst brd wch took ovr the fnction of the turst burau. Mor frml rcognition fr the cuntrys tursm sctr ws gvn wth the enctmnt of act no. 10 of 1966. 8 ths prvidd the lgisltion fr the estblishmnt of cyln turst brd. Snce thn the cyln turst brd hs fncitiond as the stat agncy, rspnsibl fr dvlpmnt and prmtion of the tursm sctr in sri lnka"

correctTest = "The government initiatives in development of tourism date back to 1937 when the Ceylon Tourist Bureau was established.[7] However, it was closed down in September 1939 due to World War II. After Sri Lanka's independence the promotion of tourism was again considered by re-establishing the Ceylon Tourist Board which took over the function of the Tourist Bureau. More formal recognition for the country's tourism sector was given with the enactment of Act No. 10 of 1966.[8] This provided the legislation for the establishment of Ceylon Tourist Board. Since then the Ceylon Tourist Board has functioned as the state agency, responsible for development and promotion of the tourism sector in Sri Lanka"
# text = "sri lnka"
# set input into lower case
text = text.lower()
correctTest = correctTest.lower()

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
        # word = "gvnment"
        # suggestList = languageReference.suggest(word)
        # if suggestList.__len__() == 1:
        #     suggetion = noSuggestionPrediction(word, suggestList, languageReference)
        #     text = text.replace(word, suggetion)
        #     # print(suggetion)
        #
        #
        # elif suggestList.__len__() == 0:
        #     suggetion = noSuggestionPrediction(word, suggestList, languageReference)
        #     suggetion = suggetion.replace(" ", "")
        #     text = text.replace(word, suggetion)
        #     # print(suggetion)
        #
        # else:
        #     # suggetion = wordPrediction(word, suggestList, languageReference)
        #     suggetion = noSuggestionPrediction(word, suggestList, languageReference)
        #     uggetion = suggetion.replace(" ", "")
        #     text = text.replace(word, suggetion)
        # print(suggetion)

        # print(suggestList)

print(text)
wordOfOriginalText = inputText.count(" ") + 1
textCount = text.count(" ") + 1
# print(wordOfOriginalText)
# print(textCount)


def findAccuracy(text, correctText):
    text = re.sub(r'[^A-Za-z\d\s]', '', text)
    text = ''.join([i for i in text if not i.isdigit()])

    correctText = re.sub(r'[^A-Za-z\d\s]', '', correctText)
    correctText = ''.join([i for i in correctText if not i.isdigit()])

    countText = text.count(" ") + 1
    countCorrectText = correctText.count(" ") + 1

    splittedText = text.split()
    splittedOriginal = correctText.split()
    accuracyVal = 0
    count = 0

    if splittedText.__len__() == splittedOriginal.__len__():
        while count < splittedOriginal.__len__():
            val = similar(splittedText[count],splittedOriginal[count])
            if val == 1:
                accuracyVal += 1
            count += 1

    return accuracyVal/countCorrectText

accuracy = findAccuracy(text,correctTest)
print(accuracy)

