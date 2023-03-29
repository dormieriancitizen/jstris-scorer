import requests, json

from discord import Webhook, RequestsWebhookAdapter

def getScores(playerName):
  url = f"https://jstris.jezevec10.com/api/u/{playerName}/records/1?mode=1&best"
  response = requests.request("GET", url).json()
  return response

playerScores = {}

    
def sendToWebhook(text):
  webhook = Webhook.from_url("webhook url", adapter=RequestsWebhookAdapter())
  webhook.send(text)

def run(playerName):
  with open("/home/pi/python/tetris-scorer/scores.json","r") as scores:
    playerScores = json.load(scores)
    try:
        playerScore = playerScores[playerName]
    except KeyError:
        playerScore=10000000000000000000000000000
  
  playerNewScore = getScores(playerName)['min']
  
  try:
    if playerNewScore < playerScores[playerName]:
      sendToWebhook(f"Record of player {playerName} is {playerNewScore}. This is a {playerScore-playerNewScore} second improvement over their previous score of {playerScores[playerName]}.")
  except:
    sendToWebhook(f"Record of player {playerName} is {playerNewScore}. This is a {playerScore-playerNewScore} second improvement over their previous score of {playerScores[playerName]}.")
  
  playerScores[playerName] = playerNewScore
  
  #print(f"Record of player {playerName} is {playerScores[playerName]}")
  
  with open("/home/pi/python/tetris-scorer/scores.json","w") as scores:
    scores.write(json.dumps(playerScores))


if __name__ == "__main__":
  players = ["foobar"]
  for player in players:
    try:
      run(player)
    except:
      pass
