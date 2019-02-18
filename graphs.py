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

def getPopulationByGenderDataframe():
	return getPerTotalDataFrame(getPopulationData(), False)
	

def getBirthsByGenderDataFrame():
	return getPerTotalDataFrame(getBirthsData(), False)

def getDeathsByGenderDataFrame():
	return getPerTotalDataFrame(getDeathsData(), True)

def getImmigrationByGenderDataFrame():
	return getPerTotalDataFrame(getImmigrationData(), False)

def getEmigrationByGenderDataFrame():
	global emigrationData

	if emigrationData == None:
		emigrationUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForEmigrationYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AY"]}}],"response":{"format":"json"}}	
		emigrationData = getYearByYearDataFrame(emigrationUrl, requestBodyForEmigrationYearByYear)

	return getPerTotalDataFrame(emigrationData, True)

def getMoveinsByGenderDataFrame():
	global moveinsData

	if moveinsData == None:
		moveinsUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForMoveinsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A2"]}}],"response":{"format":"json"}}
		moveinsData = getYearByYearDataFrame(moveinsUrl, requestBodyForMoveinsYearByYear)

	return getPerTotalDataFrame(moveinsData, False)

def getMoveoutsByGenderDataFrame():
	global moveoutsData

	if moveoutsData == None:
		moveoutsUrl = mainUrl + "BE0101J/Flyttningar97"
		requestBodyForMoveoutsYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A3"]}}],"response":{"format":"json"}}
		moveoutsData = getYearByYearDataFrame(moveoutsUrl, requestBodyForMoveoutsYearByYear)

	return getPerTotalDataFrame(moveoutsData, True)

def calculatePredictions(dataFrame):
	maleImmigration = list(dataFrame["male"])
	femaleImmigration = list(dataFrame["female"])
	numberOfElements = len(maleImmigration)
	predictionEnd = 2037
	startYear = dataFrame["year"][numberOfElements - 1] + 1
	startIndex = 0;
	femalePrediction = [femaleImmigration[numberOfElements - 1]]
	maleValue = sum(maleImmigration) / numberOfElements
	femaleValue = sum(femaleImmigration) / numberOfElements

	malePrediction =  [maleValue] * (predictionEnd - startYear + 1)
	femalePrediction = [femaleValue] * (predictionEnd - startYear + 1)
	predictionYears = list(range(startYear - 1, predictionEnd + 1))

	# for i in range(0, predictionEnd - startYear + 1):
	# 	print((sum(maleImmigration[i : numberOfElements + 1]) + sum(malePrediction[0 : len(malePrediction) + 1])) / numberOfElements)

	return {"year" : predictionYears, "malePrediction" : [maleImmigration[numberOfElements - 1]] + malePrediction, "femalePrediction" : [femaleImmigration[numberOfElements - 1]] + femalePrediction}

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
	tfrSverige = [0, 0.01, 0.06, 0.21, 0.37, 0.89, 1.39, 2.34, 3.18, 4.02, 5.08, 6.30, 7.01, 8.48, 9.99, 11.51, 12.60, 13.93, 13.66, 14.02, 13.21, 12.53, 11.31, 9.62, 7.78, 5.82, 4.57, 3.49, 2.29, 1.05, 0.73, 0.51]
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
		trace2 = go.Scatter(x = predictions['year'], y = predictions['malePrediction'], name = 'prediction males', line = dict(color = 'green'))
		trace3 = go.Scatter(x = predictions['year'], y = predictions['femalePrediction'], name = 'prediction females', line = dict(color = 'yellow'))
		data = [trace0, trace1, trace2, trace3]
	else:
		data = [trace0, trace1]
	plot(go.Figure(data = data, layout = layout), filename = fileName)

def plotPopulationByGenderGraph():
	fileName = "populationByGender.html";
	figTitle = "Total population by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Population"
	plotDataFrameGraph(getPopulationByGenderDataframe(), None, fileName, figTitle, xAxisTitle, yAxisTitle)


def plotBirthsByGenderGraph():
	fileName = "birthsByGender.html";
	figTitle = "Births by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Births"
	plotDataFrameGraph(getBirthsByGenderDataFrame(), None, fileName, figTitle, xAxisTitle, yAxisTitle)

def plotDeathsByGenderGraph():
	fileName = "deathsByGender.html";
	figTitle = "Deaths by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Deaths"
	plotDataFrameGraph(getDeathsByGenderDataFrame(), None, fileName, figTitle, xAxisTitle, yAxisTitle)

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
	# initial_text = """
	# 1. Total population by gender(- prediction)
	# 2. Births by gender(- prediction)
	# 3. Deaths by gender(- prediction)
	# 4. Immigration by gender(+ prediction)
	# 5. Emigration by gender(+ prediction)
	# 6. Moveins within country by gender(+ prediction)
	# 7. Moveouts within country by gender(+ prediction)
	# 8. Male population heatmap with numbers
	# 9. Female population heatmap with numbers
	# 10. Male population heatmap without numbers
	# 11. Female population heatmap without numbers
	# 12. Males death risk
	# 13. Females death risk
	# 14. Total fertility rate
	# """
	# print(initial_text)

	# while True:
	# 	cmd = input("Enter a number to select graph, or q to exit: ")
	# 	if cmd == '1':
	# 		plotPopulationByGenderGraph()
	# 	elif cmd == '2':
	# 		plotBirthsByGenderGraph()
	# 	elif cmd == '3':
	# 		plotDeathsByGenderGraph()
	# 	elif cmd == '4':
	# 		plotImmigrationByGenderGraph()
	# 	elif cmd == '5':
	# 		plotEmigrationByGenderGraph()
	# 	elif cmd == '6':
	# 		plotMoveinsByGenderGraph()
	# 	elif cmd == '7':
	# 		plotMoveoutsByGenderGraph()
	# 	elif cmd == '8':
	# 		plotMalePopulationHeatmap(True)
	# 	elif cmd == '9':
	# 		plotFemalePopulationHeatmap(True)
	# 	elif cmd == '10':
	# 		plotMalePopulationHeatmap(False)
	# 	elif cmd == '11':
	# 		plotFemalePopulationHeatmap(False)
	# 	elif cmd == '12':
	# 		plotMaleRisk()
	# 	elif cmd == '13':
	# 		plotFemaleRisk()
	# 	elif cmd == '14':
	# 		plotFertilityGraph()
	# 	elif cmd == 'q':
	# 		break
	# 	else:
	# 		print("Invalid command.")