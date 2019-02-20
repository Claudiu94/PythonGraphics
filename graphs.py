# coding=utf-8

from plotly.offline import download_plotlyjs, plot
import plotly.figure_factory as ff
import simplejson as simplejson
import plotly.graph_objs as go
import requests as request
import numpy as numpy
import pandas as pd

headers = {"Content-type": "application/json"}
mainUrl = "http://api.scb.se/OV0104/v1/doris/en/ssd/START/BE/BE0101/"
populationBirthsDeathsPredictionsCache = None
populationData = None
birthsData = None
deathsData = None
immigrationData = None
emigrationData = None
moveinsData = None
moveoutsData = None
deathRiskData = None
kommData = None
scbData = None

def getYearByYearDataFrame(statsUrl, jsonBody):
	matrixMales = []
	matrixFemales = []
	years = []	
	lineM = []
	lineF = []
	
	response = request.post(url = statsUrl, json = jsonBody, headers = headers);
	json_data = simplejson.loads(response.text)["data"]
	firstIndex = json_data[0]["key"][1]
	lastIndexM = firstIndex
	lastIndexF = firstIndex

	for val in json_data:
		# male
		if val["key"][2] == "1":
			if val["key"][1] != lastIndexM:
				lastIndexM = val["key"][1]
				matrixMales.append(lineM)
				lineM = []

			if lastIndexM == firstIndex:
				years.append(int(val["key"][3]))
			lineM.append(int(val["values"][0]))
		# female
		else:
			if val["key"][1] != lastIndexF:
				lastIndexF = val["key"][1]
				matrixFemales.append(lineF)
				lineF = []
			lineF.append(int(val["values"][0]))

	matrixMales.append(lineM)
	matrixFemales.append(lineF)
	dataFrame = pd.DataFrame(data = {"malesMatrix": matrixMales, "femalesMatrix": matrixFemales})

	allData = {"years" : years, "dataFrame" : dataFrame}
	return allData

def getPerTotalDataFrame(allData, negativeValues):
	malesNumber = numpy.zeros(len(allData["years"]))
	femalesNumber = numpy.zeros(len(allData["years"]))

	for line in allData["dataFrame"]["malesMatrix"]:
		for i in range(len(line)):
			malesNumber[i] += line[i]

	for line in allData["dataFrame"]["femalesMatrix"]:
		for i in range(len(line)):
			femalesNumber[i] += line[i]

	if negativeValues:
		malesNumber *= -1
		femalesNumber *= -1

	dataFrame = pd.DataFrame(data = {"year": allData["years"], "male": malesNumber, "female": femalesNumber})

	return dataFrame;


def getPopulationData():
	global populationData

	if populationData == None:
		populationUrl = mainUrl + "BE0101A/BefolkningNy"
		requestBodyForPopulationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}
		populationData = getYearByYearDataFrame(populationUrl, requestBodyForPopulationYearByYear)

	return populationData

def getDeathsData():
	global deathsData

	if deathsData == None:
		deathsUrl = mainUrl + "BE0101I/DodaFodelsearK"
		requestBodyForDeathsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}
		deathsData = getYearByYearDataFrame(deathsUrl, requestBodyForDeathsYearByYear)

	return deathsData

def getBirthsData():
	global birthsData

	if birthsData == None:
		birthsUrl = mainUrl + "BE0101H/FoddaK"
		requestBodyForBirthsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"AlderModer","selection":{"filter":"vs:Ålder1årUS","values":["-14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49+","us"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}
		birthsData = getYearByYearDataFrame(birthsUrl, requestBodyForBirthsYearByYear)

	return birthsData

def getImmigrationData():
	global immigrationData

	if immigrationData == None:
		immgrationUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForImmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AX"]}}],"response":{"format":"json"}}
		immigrationData = getYearByYearDataFrame(immgrationUrl, requestBodyForImmigrationYearByYear)

	return immigrationData

def getEmigrationData():
	global emigrationData

	if emigrationData == None:
		emigrationUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForEmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AY"]}}],"response":{"format":"json"}}	
		emigrationData = getYearByYearDataFrame(emigrationUrl, requestBodyForEmigrationYearByYear)

	return emigrationData
def getMoveinsData():
	global moveinsData

	if moveinsData == None:
		moveinsUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForMoveinsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A2"]}}],"response":{"format":"json"}}
		moveinsData = getYearByYearDataFrame(moveinsUrl, requestBodyForMoveinsYearByYear)

	return moveinsData

def getMoveoutsData():
	global moveoutsData

	if moveoutsData == None:
		moveoutsUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForMoveoutsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A3"]}}],"response":{"format":"json"}}
		moveoutsData = getYearByYearDataFrame(moveoutsUrl, requestBodyForMoveoutsYearByYear)

	return moveoutsData

def getPopulationByGenderDataframe():
	return getPerTotalDataFrame(getPopulationData(), False)
	

def getBirthsByGenderDataFrame():
	return getPerTotalDataFrame(getBirthsData(), False)

def getDeathsByGenderDataFrame():
	return getPerTotalDataFrame(getDeathsData(), True)

def getImmigrationByGenderDataFrame():
	return getPerTotalDataFrame(getImmigrationData(), False)

def getEmigrationByGenderDataFrame():
	return getPerTotalDataFrame(getEmigrationData(), True)

def getMoveinsByGenderDataFrame():
	return getPerTotalDataFrame(getMoveinsData(), False)

def getMoveoutsByGenderDataFrame():
	return getPerTotalDataFrame(getMoveoutsData(), True)

def calculatePredictions(dataFrame):
	maleData = list(dataFrame["male"])
	femaledata = list(dataFrame["female"])
	numberOfElements = len(maleData)
	predictionEnd = 2037
	startYear = dataFrame["year"][numberOfElements - 1] + 1
	startIndex = 0;
	femalePrediction = [femaledata[numberOfElements - 1]]
	maleValue = sum(maleData) / numberOfElements
	femaleValue = sum(femaledata) / numberOfElements

	malePrediction =  [maleValue] * (predictionEnd - startYear + 1)
	femalePrediction = [femaleValue] * (predictionEnd - startYear + 1)

	# for i in range(0, predictionEnd - startYear + 1):
	# 	print((sum(maleData[i : numberOfElements + 1]) + sum(malePrediction[0 : len(malePrediction) + 1])) / numberOfElements)

	return {"malePrediction" : malePrediction, "femalePrediction" : femalePrediction}

def calculateScbData(data):
	malesScb = []
	femalesScb = []

	for line in data["males"]:
		malesScb.append(sum(line)/len(line)/10)

	for line in data["females"]:
		femalesScb.append(sum(line)/len(line)/10)

	return {"males" : malesScb, "females" : femalesScb}

def getDeathRiskScbData():
	global deathRiskData

	if deathRiskData == None:
		deathRiskUrl = mainUrl + "BE0101I/LivslangdEttariga"		
		requestBodyDeathRisk = {"query":[{"code":"Alder","selection":{"filter":"item","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A¤"]}},{"code":"Tid","selection":{"filter":"item","values":["2015","2016","2017"]}}],"response":{"format":"json"}}
		response = request.post(url = deathRiskUrl, json = requestBodyDeathRisk, headers = headers);
		json_data = simplejson.loads(response.text)["data"]
		firstIndex = json_data[0]["key"][1]
		lastIndexM = firstIndex
		lastIndexF = firstIndex
		deathRiskMales = []
		deathRiskFemales = []
		lineM = []
		lineF = []

		for val in json_data:
			if val["key"][0] == "1":
				if lastIndexM != val["key"][1]:
					deathRiskMales.append(lineM)
					lineM = []
					lastIndexM = val["key"][1]
				lineM.append(float(val["values"][0]))
			else:
				if lastIndexF != val["key"][1]:
					deathRiskFemales.append(lineF)
					lineF = []
					lastIndexF = val["key"][1]
				lineF.append(float(val["values"][0]))

		deathRiskMales.append(lineM)
		deathRiskFemales.append(lineF)
		deathRiskData = calculateScbData({"males": deathRiskMales, "females": deathRiskFemales})

	return deathRiskData

def getDeathRiskKommData():
	populationData = getPopulationData()
	deathData = getDeathsData()
	malesPopulation = populationData["dataFrame"]["malesMatrix"]
	malesDeadPopulation = deathData["dataFrame"]["malesMatrix"]
	femalesPopulation = populationData["dataFrame"]["femalesMatrix"]
	femalesDeadPopulation = deathData["dataFrame"]["femalesMatrix"]
	malesKommDeathRisk = []
	femalesKommDeathRisk = []
	
	for i in range(len(malesPopulation)):
		femalesKommDeathRisk.append(100 * (sum(femalesDeadPopulation[i]) / sum(femalesPopulation[i])))
		malesKommDeathRisk.append(100 * (sum(malesDeadPopulation[i]) / sum(malesPopulation[i])))

	return {"males" : malesKommDeathRisk, "females" : femalesKommDeathRisk}

def getTfrKommData():
	birthsData = getBirthsData()
	populationData = getPopulationData()
	length = len(birthsData["dataFrame"]["malesMatrix"])
	femalesPopulation = populationData["dataFrame"]["femalesMatrix"]
	last = len(femalesPopulation[0]) - 1
	avgTfrKomm = []
	tfrKomm2017 = []
	tfrKomm2012_2017 = []

	for i in range(length):
		sumArray = numpy.add(birthsData["dataFrame"]["malesMatrix"][i], birthsData["dataFrame"]["femalesMatrix"][i])
		avgTfrKomm.append(round(100 * (sum(sumArray) / length) / (sum(femalesPopulation[i + 14]) / length) , 2))
		tfrKomm2017.append(round(100 * sumArray[last] / femalesPopulation[i + 14][last], 2))
		tfrKomm2012_2017.append(round(100 * (sum(sumArray[last - 5 : last + 1]) / 6) / (sum(femalesPopulation[i + 14][last - 5 : last + 1]) / 6), 2))

	return {"avgTfrKomm" : avgTfrKomm, "tfrKomm2017" : tfrKomm2017, "tfrKomm2012_2017" : tfrKomm2012_2017}

def getBirthShares():
	totalBirthsUrl = mainUrl + "/BE0101H/FoddaK"
	requestTotalBirths = {"query":[{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"Tid","selection":{"filter":"item","values":["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"]}}],"response":{"format":"json"}}
	males = []
	females = []
	maleShares = []
	femaleShares = []
	response = request.post(url = totalBirthsUrl, json = requestTotalBirths, headers = headers);
	json_data = simplejson.loads(response.text)["data"]
	
	for val in json_data:
		# male
		if val["key"][0] == "1":
			males.append(int(val["values"][0]))
		else:
			females.append(int(val["values"][0]))

	for i in range(0, len(males)):
		total = males[i] + females[i]
		maleShares.append(males[i] / total)
		femaleShares.append(females[i] / total)
	
	return {"boyShare" : sum(maleShares) / len(maleShares), "girlShare" : sum(femaleShares) / len(femaleShares)}

def getTfrSverige():
	return [0, 0.00965481641509724, 0.0556729215856838, 0.214757530278841, 0.373823020523653, 0.894762501075413, 1.39310397568133, 2.34378793817093, 3.18136716024127, 4.01894638231161, 5.08271596677213, 6.3047863035436, 7.00668189769718, 8.47754060280467, 9.99363355670053, 11.5097456290447, 12.5961132194511, 13.9312882966418, 13.6606284233971, 14.0232671516379, 13.2097962929328, 12.5320281805928, 11.3114682012407, 9.61592949116249, 7.7846880347191, 5.81776295035895, 4.57460496506103, 3.48970949517737, 2.29174752177113, 1.04858953647321, 0.732714532888509, 0.507288908432193]

def getPredictionAtAge(age, type, sex, firstYear):
	data = None
	line = None

	if type == "immigration":
		data = getImmigrationData()["dataFrame"]
	elif type == "emigration":
		data = getEmigrationData()["dataFrame"]
	elif type == "moveins":
		data = getMoveinsData()["dataFrame"]
	elif type == "moveouts":
		data = getMoveoutsData()["dataFrame"]

	if sex == "male":
		line = data["malesMatrix"][age]
	elif sex =="female":
		line = data["femalesMatrix"][age]

	if line != None:
		if firstYear:
			return line[len(line) - 1]
		else:
			return sum(line) / len(line)
	else:
		return None

def getPopulation_Births_Deaths_Predictions():
	global populationBirthsDeathsPredictionsCache

	if populationBirthsDeathsPredictionsCache != None:
		return populationBirthsDeathsPredictionsCache

	populationData = getPopulationData()
	deathsData = getDeathsData()
	pMotherBirthAtX = getTfrSverige()
	birthShares = getBirthShares()
	deathRiskScb = getDeathRiskScbData()
	malesMatrix = populationData["dataFrame"]["malesMatrix"]
	femalesMatrix = populationData["dataFrame"]["femalesMatrix"]
	malesDeathsMatrix = deathsData["dataFrame"]["malesMatrix"]
	femalesDeathsMatrix = deathsData["dataFrame"]["femalesMatrix"]
	malePopulationPredictions = []
	femalePopulationPredictions = []
	malePopulationTotalPredictions = []
	femalePopulationTotalPredictions = []
	maleBirthsPredictions = []
	femaleBirthsPredictions = []
	maleDeathsPredictions = []
	femaleDeathsPredictions = []
	maleDeathsTotalPredictions = []
	femaleDeathsTotalPredictions = []
	startIndex = 14
	maleBirthPrediction = 0
	femaleBirthPrediction = 0
	maleDeathPrediction = 0
	femaleDeathPrediction = 0
	lastYear = 2037
	firstYear = 2018
	motherStartAge = 14
	motherEndAge = 45

	#first value for births predictions
	for i in range(0, motherEndAge - motherStartAge + 1):
		commonPart = femalesMatrix[14 + i][len(femalesMatrix[0]) - 1] * (pMotherBirthAtX[i] / 100)
		maleBirthPrediction +=  commonPart 
		femaleBirthPrediction += commonPart

	maleBirthsPredictions.append(maleBirthPrediction * birthShares["boyShare"])
	femaleBirthsPredictions.append(femaleBirthPrediction * birthShares["girlShare"])

	# first value for deaths prediction
	for i in range(0, len(deathRiskScb["males"])):
		maleDeathsPredictions.append([-(malesMatrix[i][len(malesMatrix[0]) - 1] * deathRiskScb["males"][i] / 100)])
		femaleDeathsPredictions.append([-(femalesMatrix[i][len(femalesMatrix[0]) - 1] * deathRiskScb["females"][i] / 100)])
		maleDeathPrediction += maleDeathsPredictions[i][0]
		femaleDeathPrediction += femaleDeathsPredictions[i][0]

	maleDeathsTotalPredictions.append(maleDeathPrediction)
	femaleDeathsTotalPredictions.append(femaleDeathPrediction)

	# first values for population predictions
	# X = 0
	malePopulationPredictions.append([maleBirthsPredictions[0] - getPredictionAtAge(0, "moveouts", "male", True)
		+ getPredictionAtAge(0, "moveins", "male", True) - getPredictionAtAge(0, "emigration", "male", True) 
		+ getPredictionAtAge(0, "immigration", "male", True)])
	femalePopulationPredictions.append([femaleBirthsPredictions[0] - getPredictionAtAge(0, "moveouts", "female", True)
		+ getPredictionAtAge(0, "moveins", "female", True) - getPredictionAtAge(0, "emigration", "female", True) 
		+ getPredictionAtAge(0, "immigration", "female", True)])

	sumMales = malePopulationPredictions[0][0]
	sumFemales = femalePopulationPredictions[0][0]
	# X > 0
	for i in range(1, 101):
		malePopulationPredictions.append([max(malesMatrix[i - 1][len(malesMatrix[i - 1]) - 1] - malesDeathsMatrix[i - 1][len(malesMatrix[i - 1]) - 1]
			- getPredictionAtAge(i, "moveouts", "male", True) + getPredictionAtAge(i, "moveins", "male", True)
			- getPredictionAtAge(i, "emigration", "male", True) + getPredictionAtAge(i, "immigration", "male", True), 0)])
		femalePopulationPredictions.append([max(femalesMatrix[i - 1][len(femalesMatrix[i - 1]) - 1] - femalesDeathsMatrix[i - 1][len(femalesMatrix[i - 1]) - 1]
			- getPredictionAtAge(i, "moveouts", "female", True) + getPredictionAtAge(i, "moveins", "female", True)
			- getPredictionAtAge(i, "emigration", "female", True) + getPredictionAtAge(i, "immigration", "female", True), 0)])
		sumMales += malePopulationPredictions[i][0]
		sumFemales += femalePopulationPredictions[i][0]

	malePopulationTotalPredictions.append(sumMales)
	femalePopulationTotalPredictions.append(sumFemales)

	for i in range(1, lastYear - firstYear + 1):
		maleBirthPrediction = 0
		femaleBirthPrediction = 0
		for j in range(0, motherEndAge - motherStartAge + 1):
			commonPart = femalePopulationPredictions[14 + j][i - 1] * (pMotherBirthAtX[j] / 100)
			maleBirthPrediction +=  commonPart 
			femaleBirthPrediction += commonPart
		maleBirthsPredictions.append(maleBirthPrediction * birthShares["boyShare"])
		femaleBirthsPredictions.append(femaleBirthPrediction * birthShares["girlShare"])

		maleDeathPrediction = 0
		femaleDeathPrediction = 0
		for j in range(0, len(deathRiskScb["males"])):
			maleDeathsPredictions[j].append(-(malePopulationPredictions[j][i - 1] * deathRiskScb["males"][j] / 100))
			femaleDeathsPredictions[j].append(-(femalePopulationPredictions[j][i - 1] * deathRiskScb["females"][j] / 100))
			maleDeathPrediction += maleDeathsPredictions[j][i]
			femaleDeathPrediction += femaleDeathsPredictions[j][i]
		maleDeathsTotalPredictions.append(maleDeathPrediction)
		femaleDeathsTotalPredictions.append(femaleDeathPrediction)

		# first values for population predictions
		# X = 0
		malePopulationPredictions[0].append(maleBirthsPredictions[i] - getPredictionAtAge(0, "moveouts", "male", False)
			+ getPredictionAtAge(0, "moveins", "male", False) - getPredictionAtAge(0, "emigration", "male", False) 
			+ getPredictionAtAge(0, "immigration", "male", False))
		femalePopulationPredictions[0].append(femaleBirthsPredictions[i] - getPredictionAtAge(0, "moveouts", "female", False)
			+ getPredictionAtAge(0, "moveins", "female", False) - getPredictionAtAge(0, "emigration", "female", False) 
			+ getPredictionAtAge(0, "immigration", "female", False))

		sumMales = malePopulationPredictions[0][i]
		sumFemales = femalePopulationPredictions[0][i]

		# X > 0
		for j in range(1, 101):
			malePopulationPredictions[j].append(max(malePopulationPredictions[j - 1][i - 1] + maleDeathsPredictions[j - 1][i - 1]
				- getPredictionAtAge(j, "moveouts", "male", False) + getPredictionAtAge(j, "moveins", "male", False)
				- getPredictionAtAge(j, "emigration", "male", False) + getPredictionAtAge(j, "immigration", "male", False), 0))
			femalePopulationPredictions[j].append(max(femalePopulationPredictions[j - 1][i - 1] + femaleDeathsPredictions[j - 1][i - 1]
				- getPredictionAtAge(j, "moveouts", "female", False) + getPredictionAtAge(j, "moveins", "female", False)
				- getPredictionAtAge(j, "emigration", "female", False) + getPredictionAtAge(j, "immigration", "female", False), 0))
			sumMales += malePopulationPredictions[j][i]
			sumFemales += femalePopulationPredictions[j][i]
		malePopulationTotalPredictions.append(sumMales)
		femalePopulationTotalPredictions.append(sumFemales)

	populationBirthsDeathsPredictionsCache = {"male" : {"populationPredictions" : malePopulationTotalPredictions, "birthsPredictions" : maleBirthsPredictions, "deathsPredictions" : maleDeathsTotalPredictions},
											"female" : {"populationPredictions" : femalePopulationTotalPredictions, "birthsPredictions" : femaleBirthsPredictions, "deathsPredictions" : femaleDeathsTotalPredictions}}

	return populationBirthsDeathsPredictionsCache

def plotRisk(data, fileName, figTitle):
	trace0 = go.Scatter(y = data["scb"], name = 'SCB data', line = dict(color = 'blue'))
	trace1 = go.Scatter(y = data["komm"], name = 'Kommun medel', line = dict(color = 'red'))
	layout = go.Layout(title = figTitle)
	plot(go.Figure(data = [trace0, trace1], layout = layout), filename = fileName)

def plotMaleRisk():
	dataScb = getDeathRiskScbData()
	dataKomm = getDeathRiskKommData()
	data = {"scb" : dataScb["males"], "komm" : dataKomm["males"]}
	plotRisk(data, "deathRiskMales.html", "Males death risk")

def plotFemaleRisk():
	dataScb = getDeathRiskScbData()
	dataKomm = getDeathRiskKommData()
	data = {"scb" : dataScb["females"], "komm" : dataKomm["females"]}
	plotRisk(data, "deathRiskFemales.html", "Females death risk")

def plotFertilityGraph():
	tfrSverige = getTfrSverige()
	tfrKommData = getTfrKommData()
	x = numpy.arange(14, 46, 1)
	trace0 = go.Scatter(y = tfrSverige, x = x, name = 'TFR Sverige', line = dict(color = 'blue'))
	trace1 = go.Scatter(y = tfrKommData["avgTfrKomm"], x = x, name = 'Average TFR Kommunen', line = dict(color = 'red'))
	trace2 = go.Scatter(y = tfrKommData["tfrKomm2017"], x = x, name = 'TFR Kommunen 2017', line = dict(color = 'yellow'))
	trace3 = go.Scatter(y = tfrKommData["tfrKomm2012_2017"], x = x, name = 'TFR Kommunen 2012-2017', line = dict(color = 'green'))
	layout = go.Layout(title = "Total fertility rate", xaxis = dict(title = "Age"), yaxis = dict(title = "Percentage"))

	plot(go.Figure(data = [trace0, trace1, trace2, trace3], layout = layout), filename = "fertilityGraph.html")

def plotDataFrameGraph(df, predictions, fileName, figTitle, xAxisTitle, yAxisTitle):
	trace0 = go.Scatter(x = df['year'], y = df['male'], name = 'males', line = dict(color = 'blue'))
	trace1 = go.Scatter(x = df['year'], y = df['female'], name = 'females', line = dict(color = 'red'))
	layout = go.Layout(title = figTitle,  xaxis = dict(title = xAxisTitle), yaxis = dict(title = yAxisTitle))

	if predictions != None:
		predictionEnd = 2037
		startYear = df["year"][len(df["year"]) - 1]
		predictionYears = list(range(startYear, predictionEnd + 1))
		trace2 = go.Scatter(x = predictionYears, y = [df['male'][len(df['male']) - 1]] + predictions['malePrediction'], name = 'prediction males', line = dict(color = 'green'))
		trace3 = go.Scatter(x = predictionYears, y = [df['female'][len(df['female']) - 1]] + predictions['femalePrediction'], name = 'prediction females', line = dict(color = 'yellow'))
		data = [trace0, trace1, trace2, trace3]
	else:
		data = [trace0, trace1]
	plot(go.Figure(data = data, layout = layout), filename = fileName)

def plotPopulationByGenderGraph():
	fileName = "populationByGender.html";
	figTitle = "Total population by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Population"
	predictions = getPopulation_Births_Deaths_Predictions()
	populationPredictions = {"malePrediction" : predictions["male"]["populationPredictions"], "femalePrediction" : predictions["female"]["populationPredictions"]}
	plotDataFrameGraph(getPopulationByGenderDataframe(), populationPredictions, fileName, figTitle, xAxisTitle, yAxisTitle)


def plotBirthsByGenderGraph():
	fileName = "birthsByGender.html";
	figTitle = "Births by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Births"
	predictions = getPopulation_Births_Deaths_Predictions()
	birthsPredictions = {"malePrediction" : predictions["male"]["birthsPredictions"], "femalePrediction" : predictions["female"]["birthsPredictions"]}
	plotDataFrameGraph(getBirthsByGenderDataFrame(), birthsPredictions, fileName, figTitle, xAxisTitle, yAxisTitle)

def plotDeathsByGenderGraph():
	fileName = "deathsByGender.html";
	figTitle = "Deaths by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Deaths"
	predictions = getPopulation_Births_Deaths_Predictions()
	deathsPredictions = {"malePrediction" : predictions["male"]["deathsPredictions"], "femalePrediction" : predictions["female"]["deathsPredictions"]}
	plotDataFrameGraph(getDeathsByGenderDataFrame(), deathsPredictions, fileName, figTitle, xAxisTitle, yAxisTitle)

def plotImmigrationByGenderGraph():
	fileName = "immigrationByGender.html";
	figTitle = "Immigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	immigrationDataFrame = getImmigrationByGenderDataFrame()
	plotDataFrameGraph(immigrationDataFrame, calculatePredictions(immigrationDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotEmigrationByGenderGraph():
	fileName = "emigrationByGender.html";
	figTitle = "Emigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	emigrationDataFrame = getEmigrationByGenderDataFrame()
	plotDataFrameGraph(emigrationDataFrame, calculatePredictions(emigrationDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotMoveinsByGenderGraph():
	fileName = "moveinsByGender.html";
	figTitle = "Moveins within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	moveinsDataFrame = getMoveinsByGenderDataFrame()
	plotDataFrameGraph(moveinsDataFrame, calculatePredictions(moveinsDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotMoveoutsByGenderGraph():
	fileName = "moveoutsByGender.html";
	figTitle = "Moveouts within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	moveoutsDataFrame = getMoveoutsByGenderDataFrame() 
	plotDataFrameGraph(moveoutsDataFrame, calculatePredictions(moveoutsDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotPopulationHeatMap(withNumbers, x, z, title, fileName):	
	xAxisTitle = "Year"
	yAxisTitle = "Age"

	if withNumbers:
		fig = ff.create_annotated_heatmap(z, x = x)
		fig.layout.title = title
		fig.layout.xaxis.side = 'bottom'
		fig.layout.xaxis.title = xAxisTitle
		fig.layout.yaxis.title = yAxisTitle
		plot(fig, filename=fileName)
	else:
		trace = go.Heatmap(x = x, z = z)
		layout = go.Layout(title = title,  xaxis = dict(title = xAxisTitle), yaxis = dict(title = yAxisTitle))
		fig = go.Figure(data=[trace], layout=layout)
		plot(fig, filename=fileName)

def plotMalePopulationHeatmap(withNumbers):
	dataFrame = getPopulationData()
	plotPopulationHeatMap(withNumbers, dataFrame["years"], dataFrame["dataFrame"]["malesMatrix"], "Male population heatmap", "malesHeatmap.html")

def plotFemalePopulationHeatmap(withNumbers):
	dataFrame = getPopulationData()
	plotPopulationHeatMap(withNumbers, dataFrame["years"], dataFrame["dataFrame"]["femalesMatrix"], "Female population heatmap", "femalesHeatmap.html")


if __name__ == "__main__":
	initial_text = """
	1. Total population by gender(+ prediction)
	2. Births by gender(+ prediction)
	3. Deaths by gender(+ prediction)
	4. Immigration by gender(+ prediction)
	5. Emigration by gender(+ prediction)
	6. Moveins within country by gender(+ prediction)
	7. Moveouts within country by gender(+ prediction)
	8. Male population heatmap with numbers
	9. Female population heatmap with numbers
	10. Male population heatmap without numbers
	11. Female population heatmap without numbers
	12. Males death risk
	13. Females death risk
	14. Total fertility rate
	"""
	print(initial_text)

	while True:
		cmd = input("Enter a number to select graph, or q to exit: ")
		if cmd == '1':
			plotPopulationByGenderGraph()
		elif cmd == '2':
			plotBirthsByGenderGraph()
		elif cmd == '3':
			plotDeathsByGenderGraph()
		elif cmd == '4':
			plotImmigrationByGenderGraph()
		elif cmd == '5':
			plotEmigrationByGenderGraph()
		elif cmd == '6':
			plotMoveinsByGenderGraph()
		elif cmd == '7':
			plotMoveoutsByGenderGraph()
		elif cmd == '8':
			plotMalePopulationHeatmap(True)
		elif cmd == '9':
			plotFemalePopulationHeatmap(True)
		elif cmd == '10':
			plotMalePopulationHeatmap(False)
		elif cmd == '11':
			plotFemalePopulationHeatmap(False)
		elif cmd == '12':
			plotMaleRisk()
		elif cmd == '13':
			plotFemaleRisk()
		elif cmd == '14':
			plotFertilityGraph()
		elif cmd == 'q':
			break
		else:
			print("Invalid command.")