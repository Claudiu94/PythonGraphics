# coding=utf-8
from plotly.offline import download_plotlyjs, plot
import plotly.figure_factory as ff
import plotly.graph_objs as go
import numpy as numpy
import dataFrameCrawler as dataFrameService

populationBirthsDeathsPredictionsCache = None
includePlotlyInHtml = False

def setPlotlyInclusion(value):
	global includePlotlyInHtml
	includePlotlyInHtml = value

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

def getPredictionAtAge(age, type, sex, firstYear):
	data = None
	line = None

	if type == "immigration":
		data = dataFrameService.getImmigrationData()["dataFrame"]
	elif type == "emigration":
		data = dataFrameService.getEmigrationData()["dataFrame"]
	elif type == "moveins":
		data = dataFrameService.getMoveinsData()["dataFrame"]
	elif type == "moveouts":
		data = dataFrameService.getMoveoutsData()["dataFrame"]

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

	populationData = dataFrameService.getPopulationData()
	deathsData = dataFrameService.getDeathsData()
	pMotherBirthAtX = dataFrameService.getTfrSverige()
	birthShares = dataFrameService.getBirthShares()
	deathRiskScb = dataFrameService.getDeathRiskScbData()
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
	dataScb = dataFrameService.getDeathRiskScbData()
	dataKomm = dataFrameService.getDeathRiskKommData()
	data = {"scb" : dataScb["males"], "komm" : dataKomm["males"]}
	plotRisk(data, "deathRiskMales.html", "Males death risk")

def plotFemaleRisk():
	dataScb = dataFrameService.getDeathRiskScbData()
	dataKomm = dataFrameService.getDeathRiskKommData()
	data = {"scb" : dataScb["females"], "komm" : dataKomm["females"]}
	plotRisk(data, "deathRiskFemales.html", "Females death risk")

def plotFertilityGraph():
	tfrSverige = dataFrameService.getTfrSverige()
	tfrKommData = dataFrameService.getTfrKommData()
	x = numpy.arange(14, 46, 1)
	trace0 = go.Scatter(y = tfrSverige, x = x, name = 'TFR Sverige', line = dict(color = 'blue'))
	trace1 = go.Scatter(y = tfrKommData["avgTfrKomm"], x = x, name = 'Average TFR Kommunen', line = dict(color = 'red'))
	trace2 = go.Scatter(y = tfrKommData["tfrKomm2017"], x = x, name = 'TFR Kommunen 2017', line = dict(color = 'yellow'))
	trace3 = go.Scatter(y = tfrKommData["tfrKomm2012_2017"], x = x, name = 'TFR Kommunen 2012-2017', line = dict(color = 'green'))
	layout = go.Layout(title = "Total fertility rate", xaxis = dict(title = "Age"), yaxis = dict(title = "Percentage"))

	plot(go.Figure(data = [trace0, trace1, trace2, trace3], layout = layout), filename = "fertilityGraph.html", include_plotlyjs=includePlotlyInHtml)

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
	plot(go.Figure(data = data, layout = layout), filename = fileName, include_plotlyjs=includePlotlyInHtml)

def plotPopulationByGenderGraph():
	fileName = "populationByGender.html";
	figTitle = "Total population by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Population"
	predictions = getPopulation_Births_Deaths_Predictions()
	populationPredictions = {"malePrediction" : predictions["male"]["populationPredictions"], "femalePrediction" : predictions["female"]["populationPredictions"]}
	plotDataFrameGraph(dataFrameService.getPopulationByGenderDataframe(), populationPredictions, fileName, figTitle, xAxisTitle, yAxisTitle)


def plotBirthsByGenderGraph():
	fileName = "birthsByGender.html";
	figTitle = "Births by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Births"
	predictions = getPopulation_Births_Deaths_Predictions()
	birthsPredictions = {"malePrediction" : predictions["male"]["birthsPredictions"], "femalePrediction" : predictions["female"]["birthsPredictions"]}
	plotDataFrameGraph(dataFrameService.getBirthsByGenderDataFrame(), birthsPredictions, fileName, figTitle, xAxisTitle, yAxisTitle)

def plotDeathsByGenderGraph():
	fileName = "deathsByGender.html";
	figTitle = "Deaths by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Deaths"
	predictions = getPopulation_Births_Deaths_Predictions()
	deathsPredictions = {"malePrediction" : predictions["male"]["deathsPredictions"], "femalePrediction" : predictions["female"]["deathsPredictions"]}
	plotDataFrameGraph(dataFrameService.getDeathsByGenderDataFrame(), deathsPredictions, fileName, figTitle, xAxisTitle, yAxisTitle)

def plotImmigrationByGenderGraph():
	fileName = "immigrationByGender.html";
	figTitle = "Immigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	immigrationDataFrame = dataFrameService.getImmigrationByGenderDataFrame()
	plotDataFrameGraph(immigrationDataFrame, calculatePredictions(immigrationDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotEmigrationByGenderGraph():
	fileName = "emigrationByGender.html";
	figTitle = "Emigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	emigrationDataFrame = dataFrameService.getEmigrationByGenderDataFrame()
	plotDataFrameGraph(emigrationDataFrame, calculatePredictions(emigrationDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotMoveinsByGenderGraph():
	fileName = "moveinsByGender.html";
	figTitle = "Moveins within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	moveinsDataFrame = dataFrameService.getMoveinsByGenderDataFrame()
	plotDataFrameGraph(moveinsDataFrame, calculatePredictions(moveinsDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotMoveoutsByGenderGraph():
	fileName = "moveoutsByGender.html";
	figTitle = "Moveouts within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	moveoutsDataFrame = dataFrameService.getMoveoutsByGenderDataFrame() 
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
		plot(fig, filename=fileName, include_plotlyjs=includePlotlyInHtml)
	else:
		trace = go.Heatmap(x = x, z = z)
		layout = go.Layout(title = title,  xaxis = dict(title = xAxisTitle), yaxis = dict(title = yAxisTitle))
		fig = go.Figure(data=[trace], layout=layout)
		plot(fig, filename=fileName, include_plotlyjs=includePlotlyInHtml)

def plotMalePopulationHeatmap(withNumbers):
	dataFrame = dataFrameService.getPopulationData()
	plotPopulationHeatMap(withNumbers, dataFrame["years"], dataFrame["dataFrame"]["malesMatrix"], "Male population heatmap", "malesHeatmap.html")

def plotFemalePopulationHeatmap(withNumbers):
	dataFrame = dataFrameService.getPopulationData()
	plotPopulationHeatMap(withNumbers, dataFrame["years"], dataFrame["dataFrame"]["femalesMatrix"], "Female population heatmap", "femalesHeatmap.html")


if __name__ == "__main__":
	cmd = input("Include plotlyjs(Y or N, default: N)?: ")

	if cmd == 'Y':
		setPlotlyInclusion(True)

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