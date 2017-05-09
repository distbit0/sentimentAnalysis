wordScoresFilePath = "/home/pimania/projects/sentimentAnalysis/wordScores.txt"
delaySeconds = 100


def ensureWordScoresFile(wordScoresFilePath):
   try:
       with open(wordScoresFilePath) as wordScoresFile:
           pass
   except IOError:
       with open(wordScoresFilePath, "w") as wordScoresFile:
          pass


def getTwitterText():
   import tweepy
   try:
      auth = tweepy.auth.OAuthHandler("kqSndhybqhsSBcrY83ZpK2dkH", "EoJm0OmlZZmyhJOln7vIJg8en97NhVZQx0u9QSKKI7T9B7hvUg")
      auth.set_access_token("3685943952-BTfjGnef7QNdqnh9EMHtO5SInUcE2ZaROX9MMi8", "vD1q0887Cof3N8GKNQMHHW2Ad5vjFJCTsBONJZ47zNqC9")
      api = tweepy.API(auth)
   except:
      return False
   
   text = " ".join([tweet._json["text"] for tweet in api.search(q="good", count=100)]).lower() + " " + " ".join([tweet._json["text"] for tweet in api.search(q="bad", count=100)]).lower()
   
   sentences = text.replace("?", ".").replace("!", ".").split(". ")
   
   goodSentences = ". ".join([sentence for sentence in sentences if "good" in sentence])
   badSentences = ". ".join([sentence for sentence in sentences if "bad" in sentence])
   
   return [goodSentences, badSentences]
   

def getBadGoodRatio(wordScores):
   totalGoodScore = 0
   totalBadScore = 0
   
   for score in wordScores.values():
      if score > 0:
         totalGoodScore += score
      if score < 0:
         totalBadScore += score
         
   return abs(totalBadScore) / totalGoodScore


def getWordScores(goodText, badText):
   import string
   import re
   
   regex = re.compile('[%s]' % re.escape(string.punctuation))
   wordScores = {}

   goodWords = regex.sub('', goodText).split()
   badWords = regex.sub('', badText).split()

   for word in goodWords:
      wordScores[word] = wordScores.get(word, 0) + 1
      
   for word in badWords:
      wordScores[word] = wordScores.get(word, 0) - 1
      
   return wordScores
      
      
def getLastWordScores(wordScoresFilePath):
   import json
   
   with open(wordScoresFilePath) as wordScoresFile:
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
        twitterGoodtext, twitterBadtext = getTwitterText("good", "bad")
      except:
        print("Connection error...")
        continue
        
      wordScores = getWordScores(twitterGoodtext, twitterBadtext)
         
      badGoodScoreRatio = getBadGoodRatio(wordScores)
      newWordScores = getNewWordScores(badGoodScoreRatio, wordScores, lastWordScores)
      
      with open(wordScoresFilePath, "w") as wordScoresFile:
         json.dump(newWordScores, wordScoresFile)
      

main()
