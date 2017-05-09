import json
import string
import re
import sys


wordScoresFilePath = "/home/pimania/projects/sentimentAnalysis/wordScores.txt"
regex = re.compile('[%s]' % re.escape(string.punctuation))

def getWordScores(wordScoresFilePath):
   try:
      wordScores = json.loads(open(wordScoresFilePath).read())
   except:
      print("No wordScores.txt file found.")
      return False
   else:
      return wordScores
      
      
def getSentenceSentiment(sentence, wordScores):
   sentenceScore = 0
   sentenceWordScores = {}
   sentence = regex.sub('', sentence.lower()).split()
   
   for word in sentence:
      wordScore = wordScores.get(word, [0, 1])
      sentenceScore += wordScore[0] / wordScore[1]
      sentenceWordScores[word] = wordScore[0] / wordScore[1]
   if sentenceScore > 0:
      sentenceSentiment = "Positive"
   elif sentenceScore  == 0:
      sentenceSentiment = "Neutral"
   else:
      sentenceSentiment = "Negative"
      
   return [sentenceSentiment, sentenceScore, sentenceWordScores]
   
   
def getSentimentStatistics(wordScores):
   totalGoodScore = 0
   totalBadScore = 0
   amountOfGoodWords = 0
   amountOfBadWords = 0

   for score in wordScores.values():
      if score[0]/score[1]  > 0:
         totalGoodScore += score[0]/score[1]
         amountOfGoodWords += 1
      if score[0]/score[1] < 0:
         totalBadScore += score[0]/score[1]
         amountOfBadWords += 1
         
   return [totalGoodScore, totalBadScore, amountOfGoodWords, amountOfBadWords]
   
   
def getTopNBadGoodWords(wordCount, wordScores):
   topTenGoodWords = sorted(wordScores, key = lambda x: -(wordScores[x][0] / wordScores[x][1]))[:wordCount]
   topTenBadWords = sorted(wordScores, key = lambda x: (wordScores[x][0] / wordScores[x][1]))[:wordCount]
   return [topTenGoodWords, topTenBadWords]
   
wordScores = getWordScores(wordScoresFilePath)
if not wordScores:
   sys.exit()

print("Available functions: getSentenceSentiment [1], getSentimentStatistics [2] and getTopNBadGoodWords [3]")
functionName = input("Chose a function to request: ")

if functionName == "1":
   sentence = input("Enter a sentence to analyse: ")
   sentiment, score, wordScores = getSentenceSentiment(sentence, wordScores)
   print("\nSentence sentiment: " + sentiment + "\nSentence score: " + str(score) + "\nSentence word scores:")
   for word in wordScores:
      print(word + " : " + str(wordScores[word]))
   
elif functionName == "2":
   totalGoodScore, totalBadScore, amountOfGoodWords, amountOfBadWords = getSentimentStatistics(wordScores)
   print("Total good score: " + str(totalGoodScore) + "\nTotal bad score: " + str(totalBadScore) + "\nAmount of good words: " + str(amountOfGoodWords) + "\nAmount of bad words: " + str(amountOfBadWords))
   
elif functionName == "3":
   wordCount = int(input("Enter how many extreme words you would like to see: "))
   goodWords, badWords = getTopNBadGoodWords(wordCount, wordScores)
   print("Top " + str(wordCount) + " good words: \n" + "\n".join(goodWords) + "\n\nTop " + str(wordCount) + " bad words: \n" + "\n".join(badWords))

else:
   print("Invalid function name")
