# coding=utf-8
import simplejson as simplejson
import requests as request
import numpy as numpy
import time as time
import pandas as pd
import sys as sys

headers = {"Content-type": "application/json"}
mainUrl = "http://api.scb.se/OV0104/v1/doris/en/ssd/START/"
populationData = {}
birthsData = {}
deathsData = {}
immigrationData = {}
emigrationData = {}
moveinsData = {}
moveoutsData = {}
housesData = {}
holidaysHousesData = {}
demolitionData = {}
soldHousesData = {}
soldHousesDataByPropertType = {}
averageRentData = {}
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
		populationUrl = mainUrl + "BE/BE0101/BE0101A/BefolkningNy"
		requestBodyForPopulationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}
		populationData[code] = getYearByYearDataFrame(populationUrl, requestBodyForPopulationYearByYear)


	return populationData[code]

def getDeathsData(code):
	global deathsData

	if code not in deathsData:
		deathsUrl = mainUrl + "BE/BE0101/BE0101I/DodaFodelsearK"
		requestBodyForDeathsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}
		deathsData[code] = getYearByYearDataFrame(deathsUrl, requestBodyForDeathsYearByYear)

	return deathsData[code]

def getBirthsData(code):
	global birthsData

	if code not in birthsData:
		birthsUrl = mainUrl + "BE/BE0101/BE0101H/FoddaK"
		requestBodyForBirthsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"AlderModer","selection":{"filter":"vs:Ålder1årUS","values":["-14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49+","us"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}
		birthsData[code] = getYearByYearDataFrame(birthsUrl, requestBodyForBirthsYearByYear)

	return birthsData[code]

def getImmigrationData(code):
	global immigrationData

	if code not in immigrationData:
		immgrationUrl = mainUrl + "BE/BE0101/BE0101J/Flyttningar97"
		requestBodyForImmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AX"]}}],"response":{"format":"json"}}
		immigrationData[code] = getYearByYearDataFrame(immgrationUrl, requestBodyForImmigrationYearByYear)

	return immigrationData[code]

def getEmigrationData(code):
	global emigrationData

	if code not in emigrationData:
		emigrationUrl = mainUrl + "BE/BE0101/BE0101J/Flyttningar97"
		requestBodyForEmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AY"]}}],"response":{"format":"json"}}	
		emigrationData[code] = getYearByYearDataFrame(emigrationUrl, requestBodyForEmigrationYearByYear)

	return emigrationData[code]
	
def getMoveinsData(code):
	global moveinsData

	if code not in moveinsData:
		moveinsUrl = mainUrl + "BE/BE0101/BE0101J/Flyttningar97"
		requestBodyForMoveinsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A2"]}}],"response":{"format":"json"}}
		moveinsData[code] = getYearByYearDataFrame(moveinsUrl, requestBodyForMoveinsYearByYear)

	return moveinsData[code]

def getMoveoutsData(code):
	global moveoutsData

	if code not in moveoutsData:
		moveoutsUrl = mainUrl + "BE/BE0101/BE0101J/Flyttningar97"
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
		deathRiskUrl = mainUrl + "BE/BE0101/BE0101I/LivslangdEttariga"		
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
		sumF = sum(femalesPopulation[i])
		sumM = sum(malesPopulation[i])
		if sumF == 0:
			sumF = 1
		if sumM == 0:
			sumM = 1

		femalesKommDeathRisk.append(100 * (sum(femalesDeadPopulation[i]) / sumF))
		malesKommDeathRisk.append(100 * (sum(malesDeadPopulation[i]) / sumM))

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
		totalBirthsUrl = mainUrl + "BE/BE0101/BE0101H/FoddaK"
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

def processDataframe(dataFrame):
	years = list(dataFrame["keys"])
	dataFrame = dataFrame.drop(columns = ["keys"])
	dataFrame = dataFrame.reindex(["SMÅHUS", "FLERBOST", "ÖVRHUS"], axis=1)

	return {"dataFrame" : dataFrame, "years" : years}

def printException1():
	print("\nUnexpected error:", sys.exc_info()[0])
	print("First try, wait 5 seconds and try again...")
	time.sleep(5)

def getNumberOfAppartmentsData(code):
	global housesData
	global exception

	if code not in housesData:
		housesDataUrl = mainUrl + "BO/BO0104/BO0104T02"
		jsonBody = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Byggnadsperiod","selection":{"filter":"item","values":["UPPG. SAKNAS","-1930","1931-1940","1941-1950","1951-1960","1961-1970","1971-1980","1981-1990","1991-2000","2001-2010","2011-"]}},{"code":"Tid","selection":{"filter":"item","values":["2017"]}}],"response":{"format":"json"}}
		housesDataLocal = {}
		housesDataLocal["keys"] = []
		lastKey = None

		try:
			response = request.post(url = housesDataUrl, json = jsonBody, headers = headers);
			json_data = simplejson.loads(response.text)["data"]

			for val in json_data:
				if val["key"][1] != lastKey:
					lastKey = val["key"][1]
					housesDataLocal[lastKey] = []
				if val["key"][2] == "UPPG. SAKNAS":
					housesDataLocal[lastKey].insert(0, (int)(val["values"][0]))
				else:
					housesDataLocal[lastKey].append((int)(val["values"][0]))
				
				if val["key"][2] not in housesDataLocal["keys"]:
					housesDataLocal["keys"].append(val["key"][2])

			housesDataLocal["keys"].insert(0, housesDataLocal["keys"].pop())

			housesData[code] = processDataframe(pd.DataFrame.from_dict(housesDataLocal))
		except:
			if exception:
				print("Second try. Raise an exception and continue...")
				exception = False
				
				raise ValueError('No value for this code: ', code)
			else:
				printException1()
				exception = True
				getNumberOfAppartmentsData(code)

	return housesData[code]

def getNumberOfHolidaysByRegion(code):
	global holidaysHousesData
	global exception

	if code not in holidaysHousesData:
		holidaysHousesUrl = mainUrl + "BO/BO0104/BO0104T08"
		jsonBody = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}}],"response":{"format":"json"}}
		holidaysHousesDataLocal = {"years" : [], "data": []}
		
		try:
			response = request.post(url = holidaysHousesUrl, json = jsonBody, headers = headers);
			json_data = simplejson.loads(response.text)["data"]

			for val in json_data:
				holidaysHousesDataLocal["years"].append(val["key"][1])
				holidaysHousesDataLocal["data"].append((int)(val["values"][0]))
			holidaysHousesData[code] = pd.DataFrame.from_dict(holidaysHousesDataLocal)
		except:
			if exception:
				print("Second try. Raise an exception and continue...")
				exception = False
				
				raise ValueError('No value for this code: ', code)
			else:
				printException1()
				exception = True
				getNumberOfHolidaysByRegion(code)
	return holidaysHousesData[code]

def getNumberOfSoldHouses(code):
	global soldHousesData
	global exception

	if code not in soldHousesData:
		soldHousesUrl = mainUrl + "BO/BO0101/BO0101A/LagenhetNyKv16"
		jsonBody = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Hustyp","selection":{"filter":"item","values":["FLERBO","SMÅHUS"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BO0101A4"]}},{"code":"Tid","selection":{"filter":"item","values":["1991K1","1991K2","1991K3","1991K4","1992K1","1992K2","1992K3","1992K4","1993K1","1993K2","1993K3","1993K4","1994K1","1994K2","1994K3","1994K4","1995K1","1995K2","1995K3","1995K4","1996K1","1996K2","1996K3","1996K4","1997K1","1997K2","1997K3","1997K4","1998K1","1998K2","1998K3","1998K4","1999K1","1999K2","1999K3","1999K4","2000K1","2000K2","2000K3","2000K4","2001K1","2001K2","2001K3","2001K4","2002K1","2002K2","2002K3","2002K4","2003K1","2003K2","2003K3","2003K4","2004K1","2004K2","2004K3","2004K4","2005K1","2005K2","2005K3","2005K4","2006K1","2006K2","2006K3","2006K4","2007K1","2007K2","2007K3","2007K4","2008K1","2008K2","2008K3","2008K4","2009K1","2009K2","2009K3","2009K4","2010K1","2010K2","2010K3","2010K4","2011K1","2011K2","2011K3","2011K4","2012K1","2012K2","2012K3","2012K4","2013K1","2013K2","2013K3","2013K4","2014K1","2014K2","2014K3","2014K4","2015K1","2015K2","2015K3","2015K4","2016K1","2016K2","2016K3","2016K4","2017K1","2017K2","2017K3","2017K4","2018K1","2018K2","2018K3","2018K4"]}}],"response":{"format":"json"}}
		soldHousesDataLocal = {}
		soldHousesDataLocal["keys"] = []
		lastKey = None

		try:
			response = request.post(url = soldHousesUrl, json = jsonBody, headers = headers);
			json_data = simplejson.loads(response.text)["data"]

			for val in json_data:
				if val["key"][1] != lastKey:
					lastKey = val["key"][1]
					soldHousesDataLocal[lastKey] = []
				if val["key"][2] not in soldHousesDataLocal["keys"]:
					soldHousesDataLocal["keys"].append(val["key"][2])
				soldHousesDataLocal[lastKey].append(int(val["values"][0]))
			soldHousesData[code] = pd.DataFrame.from_dict(soldHousesDataLocal)
		except:
			if exception:
				print("Second try. Raise an exception and continue...")
				exception = False
				
				raise ValueError('No value for this code: ', code)
			else:
				printException1()
				exception = True
				getNumberOfSoldHouses(code)
	return soldHousesData[code]

def getDemolitionData(code):
	global demolitionData
	global exception

	if code not in demolitionData:
		demolitionUrl = mainUrl + "BO/BO0102/BO0102C/LghRivRegUppAr"
		jsonBody = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":[code]}},{"code":"Upplatelseform","selection":{"filter":"item","values":["1","2","3"]}}],"response":{"format":"json"}}
		demolitionDataLocal = {}
		demolitionDataLocal["keys"] = []
		lastKey = None

		try:
			response = request.post(url = demolitionUrl, json = jsonBody, headers = headers);
			json_data = simplejson.loads(response.text)["data"]

			for val in json_data:
				if val["key"][1] != lastKey:
					lastKey = val["key"][1]
					demolitionDataLocal[lastKey] = []
				if val["key"][2] not in demolitionDataLocal["keys"]:
					demolitionDataLocal["keys"].append(val["key"][2])
				demolitionDataLocal[lastKey].append(int(val["values"][0]))
			demolitionData[code] = pd.DataFrame.from_dict(demolitionDataLocal)
		except:
			if exception:
				print("Second try. Raise an exception and continue...")
				exception = False
				
				raise ValueError('No value for this code: ', code)
			else:
				printException1()
				exception = True
				getDemolitionData(code)
	return demolitionData[code]

def getAverageRentByRegion(code):
	global averageRentData
	global exception

	if code not in averageRentData:
		url = mainUrl + "BO/BO0406/BO0406E/BO0406Tab01"
		jsonBody = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"Hyresuppg","selection":{"filter":"item","values":["Ah_kvm"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["000000RZ", "000000MQ"]}}],"response":{"format":"json"}}
		averageRentDataLocal = {}
		averageRentDataLocal["keys"] = []
		averageRentDataLocal["average"] = []
		averageRentDataLocal["deviation"] = []
		
		try:
			response = request.post(url = url, json = jsonBody, headers = headers);
			json_data = simplejson.loads(response.text)["data"]

			for val in json_data:
				averageRentDataLocal["keys"].append(val["key"][2])
				averageRentDataLocal["average"].append((int)(val["values"][0]))
				averageRentDataLocal["deviation"].append((int)(val["values"][1]))
			
			averageRentData[code] = pd.DataFrame.from_dict(averageRentDataLocal)
		except:
			if exception:
				print("Second try. Raise an exception and continue...")
				exception = False
				
				raise ValueError('No value for this code: ', code)
			else:
				printException1()
				exception = True
				getAverageRentByRegion(code)
	return averageRentData[code]

def getSoldHousesByPropertyAndRegion(code):
	global soldHousesDataByPropertType
	global exception

	if code not in averageRentData:
		url = mainUrl + "BO/BO0501/BO0501B/FastprisSHRegionAr"
		jsonBody = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":[code]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BO0501C1"]}}],"response":{"format":"json"}}
		soldHousesDataByPropertTypeLocal = {}
		soldHousesDataByPropertTypeLocal["keys"] = []
		
		try:
			response = request.post(url = url, json = jsonBody, headers = headers);
			json_data = simplejson.loads(response.text)["data"]
			lastKey = None

			for val in json_data:
				if val["key"][1] != lastKey:
					lastKey = val["key"][1]
					soldHousesDataByPropertTypeLocal[lastKey] = []
				if val["key"][2] not in soldHousesDataByPropertTypeLocal["keys"]:
					soldHousesDataByPropertTypeLocal["keys"].append(val["key"][2])
				soldHousesDataByPropertTypeLocal[lastKey].append(int(val["values"][0]))
			soldHousesDataByPropertType[code] = pd.DataFrame.from_dict(soldHousesDataByPropertTypeLocal)
		except:
			if exception:
				print("Second try. Raise an exception and continue...")
				exception = False
				
				raise ValueError('No value for this code: ', code)
			else:
				printException1()
				exception = True
				getSoldHousesByPropertyAndRegion(code)
	return soldHousesDataByPropertType[code]



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