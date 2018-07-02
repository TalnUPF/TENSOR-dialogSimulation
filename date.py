from chatFeatures import ChatFeatures
from topic import Topic
from role import Role


class Date:

	def __init__(self):
		self.iChat = ChatFeatures()
		self.iChat.process()
		self.linkFeatsDayUser = self.iChat.linkAnalysis()
		self.domainWordsDayUser = self.iChat.domainWordsPerDay()
		self.msgPerTurnDayUser = self.iChat.msgPerTurn()
		self.quranCitesDayUser = self.iChat.quranCites()

		self.iTopic = Topic()

		#generalRelevance[date] = score
		self.generalRelevanceDay = self.iTopic.relevantDayDetection()
		
		
		self.userRelevanceDay = {}
		for user in self.iChat.userSet:
			self.userRelevanceDay[user] = self.iTopic.relevantDayDetection("./stats/distances"+user[0].upper()+user[1:]+".tsv")
		

		self.iRole = Role()
		self.roleScoresDayUser = self.iRole.computeRolesPerDay()
		self.wordsPerDayUser = self.iChat.wordsPerDay()


	def dayReport(self):

		sortedDates = sorted(self.generalRelevanceDay.keys())
		for date in sortedDates:
			score = self.generalRelevanceDay[date]

			print "\n===================================="
			print "REPORT FOR DAY " + date,"\n"
			print "Day Relevance Score " + str(score)

			for user in self.iChat.userSet:
				print "   Relevance Score of "+user+" :"+str(self.userRelevanceDay[user][date])

			'''
				LINK INFO
			'''
			if date in self.linkFeatsDayUser:
				print "\nLink Info\n"
				linkInfo = self.linkFeatsDayUser[date]
				for user, linkList in linkInfo.iteritems():
					print "\t",user
					for link, category in linkList:
						print "\t\t",link,category
			
			'''
				QURAN CITES
			'''
			if date in self.quranCitesDayUser:
				print "\nQuran Cites\n"
				quranCiteInfo = self.quranCitesDayUser[date]
				for user, quranDict in quranCiteInfo.iteritems():
					print "\t",user
					for tupl in quranDict:
						print "\t\t",tupl

			'''
				DOMAIN WORDS
			'''
			if date in self.domainWordsDayUser:
				print "\nDomain Frequencies\n"
				domainWordInfo = self.domainWordsDayUser[date]
				for user, dictCategory in domainWordInfo.iteritems():
					print "\t",user
					for category, frequency in dictCategory.iteritems():
						print "\t\t",category,frequency

			for user in self.iChat.userSet:
				print "\nNumber of Words\n"
				print  "\t",user,str(self.wordsPerDayUser[date][user])

			'''
				ROLE SCORES
			'''
			if date in self.roleScoresDayUser:
				print "\nUser Activity Score\n"
				userRelevance = self.roleScoresDayUser[date]
				for user, score in userRelevance.iteritems():
					print "\t",user,score

			'''
				MSG PER TURN
			'''
			if date in self.msgPerTurnDayUser:
				print "\nMessages per turn\n"
				msgInfo = self.msgPerTurnDayUser[date]
				for user, mean in msgInfo.iteritems():
					print "\t",user,mean

if __name__ == '__main__':
	iDate = Date()
	iDate.dayReport()