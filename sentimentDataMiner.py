wordScoresFilePath = "/home/ap/wordScores.txt"
delaySeconds = 500


def ensureWordScoresFile(wordScoresFilePath):
   try:
       with open(wordScoresFilePath) as wordScoresFile:
           pass
   except IOError:
       with open(wordScoresFilePath, "w") as wordScoresFile:
          pass


def getBadGoodRatio(wordScores):
   totalGoodScore = 0
   totalBadScore = 0
   
   for score in wordScores.values():
      if score > 0:
         totalGoodScore += score
      if score < 0:
         totalBadScore += score
         
   return abs(totalBadScore) / totalGoodScore


def getSynonyms(word):
   from PyDictionary import PyDictionary
   dictionary = PyDictionary()
   return dictionary.synonym(word)[:3]

def getWordScores(goodSynonyms, badSynonyms):
   import string
   import re
   import tweepy
  
   regex = re.compile('[%s]' % re.escape(string.punctuation))
   wordScores = {}
    
   try:
      auth = tweepy.auth.OAuthHandler("kqSndhybqhsSBcrY83ZpK2dkH", "EoJm0OmlZZmyhJOln7vIJg8en97NhVZQx0u9QSKKI7T9B7hvUg")
      auth.set_access_token("3685943952-BTfjGnef7QNdqnh9EMHtO5SInUcE2ZaROX9MMi8", "vD1q0887Cof3N8GKNQMHHW2Ad5vjFJCTsBONJZ47zNqC9")
      api = tweepy.API(auth)
   except:
      return False
   
   goodText = " ".join([tweet._json["text"] for tweet in api.search(q=" OR ".join(goodSynonyms), count=100)]).lower()
   badText = " ".join([tweet._json["text"] for tweet in api.search(q=" OR ".join(badSynonyms), count=100)]).lower()

   goodWords = regex.sub('', goodText).split()
   badWords = regex.sub('', badText).split()

   for word in goodWords:
      wordScores[word] = wordScores.get(word, 0) + 1
      
   for word in badWords:
      wordScores[word] = wordScores.get(word, 0) - 1
      
   return wordScores
      
      
def getLastWordScores(wordScoresFilePath):
   import json
   
   with open("wordScores.txt") as wordScoresFile:
      try:
         lastWordScores = json.load(wordScoresFile)
      except:
         lastWordScores = {}
   return lastWordScores
   
   
def getNewWordScores(badGoodScoreRatio, wordScores, lastWordScores):
   for word in wordScores:
      if wordScores[word] > 0:
         wordScore = wordScores[word] * badGoodScoreRatio
      else:
         wordScore = wordScores[word]
         
      if word in lastWordScores:
         lastWordScores[word][0] += wordScore
         lastWordScores[word][1] += 1
      else:
         lastWordScores[word] = [0, 0]
         lastWordScores[word][0] += wordScore
         lastWordScores[word][1] += 1 

   return lastWordScores
   
   
def main():
   while True:
      import json
      import time
      
      time.sleep(delaySeconds)
      ensureWordScoresFile(wordScoresFilePath)
      lastWordScores = getLastWordScores(wordScoresFilePath) 
      try:
         goodSynonyms = getSynonyms("good") + ["good"]
         badSynonyms = getSynonyms("bad") + ["bad"]
      except:
         print("Connection error...")
         continue
         
      wordScores = getWordScores(goodSynonyms, badSynonyms)
      if not wordScores:
         print("Connection error...")
         continue
         
      badGoodScoreRatio = getBadGoodRatio(wordScores)
      newWordScores = getNewWordScores(badGoodScoreRatio, wordScores, lastWordScores)
      
      with open(wordScoresFilePath, "w") as wordScoresFile:
         json.dump(newWordScores, wordScoresFile)
      

main()
