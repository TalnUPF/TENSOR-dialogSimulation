from chatFeatures import ChatFeatures

class Role:

	def __init__(self):
		self.iChat = ChatFeatures(None)
		self.iChat.process()
		self.computeRolesPerDay()

	
	def computeRolesPerDay(self):
		msgPerDayUser, turnsPerDayUser = self.iChat.turnsPerDay()
		relevantWordsPerDayUser = self.iChat.domainWordsPerDay()
		contentWordsPerDayUser = self.iChat.wordsPerDay()
		msgPerTurnDayUser = self.iChat.msgPerTurn()

		days = msgPerDayUser.keys()
		scoresPerDayUser = {}

		for day in days:
			scoresPerDayUser[day] = {}
			for user in self.iChat.setUsers:
				numMsg = msgPerDayUser[day][user]
				msgRatio = numMsg*1.0 / self.iChat.totalMsgPerDay[day]

				turns = turnsPerDayUser[day][user]
				turnRatio = turns * 1.0 / self.iChat.totalTurnsPerDay[day]

				dangerWords = relevantWordsPerDayUser[day][user]["dominio"]
				totalWords = len(contentWordsPerDayUser[day][user])
				dangerRatio = dangerWords*1.0/totalWords

				score = msgRatio + turnRatio + dangerRatio + msgPerTurnDayUser[day][user]*0.3
				scoresPerDayUser[day][user] = score

		return scoresPerDayUser

if __name__ == '__main__':
	iRol = Role()