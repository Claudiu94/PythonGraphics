# coding=utf-8
import simplejson as simplejson
import requests as request
import numpy as numpy
import time as time
import pandas as pd
import sys as sys

headers = {"Content-type": "application/json"}
mainUrl = "http://api.scb.se/OV0104/v1/doris/en/ssd/START/BE/BE0101/"
populationData = {}
birthsData = {}
deathsData = {}
immigrationData = {}
emigrationData = {}
moveinsData = {}
moveoutsData = {}
deathRiskData = None
birthsShare = None
kommData = None
scbData = None
exception = False

def getYearByYearDataFrame(statsUrl, jsonBody):
	global exception
	matrixMales = []
	matrixFemales = []
	years = []	
	lineM = []
	lineF = []
	
	try:
		response = request.post(url = statsUrl, json = jsonBody, headers = headers);
		json_data = simplejson.loads(response.text)["data"]
	except:
		if exception:
			print("Second try. Raise an exception and continue...")
			exception = False
			
			raise ValueError('No value for this code', jsonBody["query"][0]["selection"]["values"][0])
		else:
			print("\nUnexpected error:", sys.exc_info()[0])
			print("First try, wait 10 seconds and try again...")
			exception = True
			time.sleep(10)
			getYearByYearDataFrame(statsUrl, jsonBody)

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
	exception = False

	return allData

def getPerYearTotalDataFrame(allData, negativeValues):
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


def getPopulationData(code):
	global populationData

	if code not in populationData:
		populationUrl = mainUrl + "BE0101A/BefolkningNy"
		requestBodyForPopulationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}
		populationData[code] = getYearByYearDataFrame(populationUrl, requestBodyForPopulationYearByYear)


	return populationData[code]

def getDeathsData(code):
	global deathsData

	if code not in deathsData:
		deathsUrl = mainUrl + "BE0101I/DodaFodelsearK"
		requestBodyForDeathsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}
		deathsData[code] = getYearByYearDataFrame(deathsUrl, requestBodyForDeathsYearByYear)

	return deathsData[code]

def getBirthsData(code):
	global birthsData

	if code not in birthsData:
		birthsUrl = mainUrl + "BE0101H/FoddaK"
		requestBodyForBirthsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"AlderModer","selection":{"filter":"vs:Ålder1årUS","values":["-14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49+","us"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}
		birthsData[code] = getYearByYearDataFrame(birthsUrl, requestBodyForBirthsYearByYear)

	return birthsData[code]

def getImmigrationData(code):
	global immigrationData

	if code not in immigrationData:
		immgrationUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForImmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AX"]}}],"response":{"format":"json"}}
		immigrationData[code] = getYearByYearDataFrame(immgrationUrl, requestBodyForImmigrationYearByYear)

	return immigrationData[code]

def getEmigrationData(code):
	global emigrationData

	if code not in emigrationData:
		emigrationUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForEmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AY"]}}],"response":{"format":"json"}}	
		emigrationData[code] = getYearByYearDataFrame(emigrationUrl, requestBodyForEmigrationYearByYear)

	return emigrationData[code]
	
def getMoveinsData(code):
	global moveinsData

	if code not in moveinsData:
		moveinsUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForMoveinsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A2"]}}],"response":{"format":"json"}}
		moveinsData[code] = getYearByYearDataFrame(moveinsUrl, requestBodyForMoveinsYearByYear)

	return moveinsData[code]

def getMoveoutsData(code):
	global moveoutsData

	if code not in moveoutsData:
		moveoutsUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForMoveoutsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A3"]}}],"response":{"format":"json"}}
		moveoutsData[code] = getYearByYearDataFrame(moveoutsUrl, requestBodyForMoveoutsYearByYear)

	return moveoutsData[code]

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

def getDeathRiskKommData(code):
	populationData = getPopulationData(code)
	deathData = getDeathsData(code)
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

def getTfrKommData(code):
	birthsData = getBirthsData(code)
	populationData = getPopulationData(code)
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
	global birthsShare

	if birthsShare == None:
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
	
		birthsShare = {"boyShare" : sum(maleShares) / len(maleShares), "girlShare" : sum(femaleShares) / len(femaleShares)}

	return birthsShare

def getTfrSverige():
	return [0, 0.00965481641509724, 0.0556729215856838, 0.214757530278841, 0.373823020523653, 0.894762501075413, 1.39310397568133, 2.34378793817093, 3.18136716024127, 4.01894638231161, 5.08271596677213, 6.3047863035436, 7.00668189769718, 8.47754060280467, 9.99363355670053, 11.5097456290447, 12.5961132194511, 13.9312882966418, 13.6606284233971, 14.0232671516379, 13.2097962929328, 12.5320281805928, 11.3114682012407, 9.61592949116249, 7.7846880347191, 5.81776295035895, 4.57460496506103, 3.48970949517737, 2.29174752177113, 1.04858953647321, 0.732714532888509, 0.507288908432193]


def getPopulationByGenderDataframe(code):
	return getPerYearTotalDataFrame(getPopulationData(code), False)
	
def getBirthsByGenderDataFrame(code):
	return getPerYearTotalDataFrame(getBirthsData(code), False)

def getDeathsByGenderDataFrame(code):
	return getPerYearTotalDataFrame(getDeathsData(code), True)

def getImmigrationByGenderDataFrame(code):
	return getPerYearTotalDataFrame(getImmigrationData(code), False)

def getEmigrationByGenderDataFrame(code):
	return getPerYearTotalDataFrame(getEmigrationData(code), True)

def getMoveinsByGenderDataFrame(code):
	return getPerYearTotalDataFrame(getMoveinsData(code), False)

def getMoveoutsByGenderDataFrame(code):
	return getPerYearTotalDataFrame(getMoveoutsData(code), True)