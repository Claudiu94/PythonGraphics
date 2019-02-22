# coding=utf-8
from plotly.offline import download_plotlyjs, plot
import dataFrameCrawler as dataFrameService
import plotly.figure_factory as ff
import plotly.graph_objs as go
import numpy as numpy
import os as os

populationBirthsDeathsPredictionsCache = {}
includePlotlyInHtml = False
regionCodes = ["0885","0114","0115","0117","0120","0123","0125","0126","0127","0128","0136","0138","0139","0140","0160","0162","0163","0180","0181","0182","0183","0184","0186","0187","0188","0191","0192","03","0305","0319","0330","0331","0360","0380","0381","0382","04","0428","0461","0480","0481","0482","0483","0484","0486","0488","05","0509","0512","0513","0560","0561","0562","0563","0580","0581","0582","0583","0584","0586","06","0604","0617","0642","0643","0662","0665","0680","0682","0683","0684","0685","0686","0687","07","0760","0761","0763","0764","0765","0767","0780","0781","08","0821","0834","0840","0860","0861","0862","0880","0881","0882","0883","0884","0885","09","0980","10","1060","1080","1081","1082","1083","12","1214","1230","1231","1233","1256","1257","1260","1261","1262","1263","1264","1265","1266","1267","1270","1272","1273","1275","1276","1277","1278","1280","1281","1282","1283","1284","1285","1286","1287","1290","1291","1292","1293","13","1315","1380","1381","1382","1383","1384","14","1401","1402","1407","1415","1419","1421","1427","1430","1435","1438","1439","1440","1441","1442","1443","1444","1445","1446","1447","1452","1460","1461","1462","1463","1465","1466","1470","1471","1472","1473","1480","1481","1482","1484","1485","1486","1487","1488","1489","1490","1491","1492","1493","1494","1495","1496","1497","1498","1499","17","1715","1730","1737","1760","1761","1762","1763","1764","1765","1766","1780","1781","1782","1783","1784","1785","18","1814","1860","1861","1862","1863","1864","1880","1881","1882","1883","1884","1885","19","1904","1907","1960","1961","1962","1980","1981","1982","1983","1984","20","2021","2023","2026","2029","2031","2034","2039","2061","2062","2080","2081","2082","2083","2084","2085","21","2101","2104","2121","2132","2161","2180","2181","2182","2183","2184","22","2260","2262","2280","2281","2282","2283","2284","23","2303","2305","2309","2313","2321","2326","2361","2380","24","2401","2403","2404","2409","2417","2418","2421","2422","2425","2460","2462","2463","2480","2481","2482","25","2505","2506","2510","2513","2514","2518","2521","2523","2560","2580","2581","2582","2583","2584"]
regionCodeValues = ["Borgholm","Upplands Väsby","Vallentuna","Österåker","Värmdö","Järfälla","Ekerö","Huddinge","Botkyrka","Salem","Haninge","Tyresö","Upplands-Bro","Nykvarn","Täby","Danderyd","Sollentuna","Stockholm","Södertälje","Nacka","Sundbyberg","Solna","Lidingö","Vaxholm","Norrtälje","Sigtuna","Nynäshamn","Uppsala län","Håbo","Älvkarleby","Knivsta","Heby","Tierp","Uppsala","Enköping","Östhammar","Södermanlands län","Vingåker","Gnesta","Nyköping","Oxelösund","Flen","Katrineholm","Eskilstuna","Strängnäs","Trosa","Östergötlands län","Ödeshög","Ydre","Kinda","Boxholm","Åtvidaberg","Finspång","Valdemarsvik","Linköping","Norrköping","Söderköping","Motala","Vadstena","Mjölby","Jönköpings län","Aneby","Gnosjö","Mullsjö","Habo","Gislaved","Vaggeryd","Jönköping","Nässjö","Värnamo","Sävsjö","Vetlanda","Eksjö","Tranås","Kronobergs län","Uppvidinge","Lessebo","Tingsryd","Alvesta","Älmhult","Markaryd","Växjö","Ljungby","Kalmar län","Högsby","Torsås","Mörbylånga","Hultsfred","Mönsterås","Emmaboda","Kalmar","Nybro","Oskarshamn","Västervik","Vimmerby","Borgholm","Gotlands län","Gotland","Blekinge län","Olofström","Karlskrona","Ronneby","Karlshamn","Sölvesborg","Skåne län","Svalöv","Staffanstorp","Burlöv","Vellinge","Östra Göinge","Örkelljunga","Bjuv","Kävlinge","Lomma","Svedala","Skurup","Sjöbo","Hörby","Höör","Tomelilla","Bromölla","Osby","Perstorp","Klippan","Åstorp","Båstad","Malmö","Lund","Landskrona","Helsingborg","Höganäs","Eslöv","Ystad","Trelleborg","Kristianstad","Simrishamn","Ängelholm","Hässleholm","Hallands län","Hylte","Halmstad","Laholm","Falkenberg","Varberg","Kungsbacka","Västra Götalands län","Härryda","Partille","Öckerö","Stenungsund","Tjörn","Orust","Sotenäs","Munkedal","Tanum","Dals-Ed","Färgelanda","Ale","Lerum","Vårgårda","Bollebygd","Grästorp","Essunga","Karlsborg","Gullspång","Tranemo","Bengtsfors","Mellerud","Lilla Edet","Mark","Svenljunga","Herrljunga","Vara","Götene","Tibro","Töreboda","Göteborg","Mölndal","Kungälv","Lysekil","Uddevalla","Strömstad","Vänersborg","Trollhättan","Alingsås","Borås","Ulricehamn","Åmål","Mariestad","Lidköping","Skara","Skövde","Hjo","Tidaholm","Falköping","Värmlands län","Kil","Eda","Torsby","Storfors","Hammarö","Munkfors","Forshaga","Grums","Årjäng","Sunne","Karlstad","Kristinehamn","Filipstad","Hagfors","Arvika","Säffle","Örebro län","Lekeberg","Laxå","Hallsberg","Degerfors","Hällefors","Ljusnarsberg","Örebro","Kumla","Askersund","Karlskoga","Nora","Lindesberg","Västmanlands län","Skinnskatteberg","Surahammar","Kungsör","Hallstahammar","Norberg","Västerås","Sala","Fagersta","Köping","Arboga","Dalarnas län","Vansbro","Malung-Sälen","Gagnef","Leksand","Rättvik","Orsa","Älvdalen","Smedjebacken","Mora","Falun","Borlänge","Säter","Hedemora","Avesta","Ludvika","Gävleborgs län","Ockelbo","Hofors","Ovanåker","Nordanstig","Ljusdal","Gävle","Sandviken","Söderhamn","Bollnäs","Hudiksvall","Västernorrlands län","Ånge","Timrå","Härnösand","Sundsvall","Kramfors","Sollefteå","Örnsköldsvik","Jämtlands län","Ragunda","Bräcke","Krokom","Strömsund","Åre","Berg","Härjedalen","Östersund","Västerbottens län","Nordmaling","Bjurholm","Vindeln","Robertsfors","Norsjö","Malå","Storuman","Sorsele","Dorotea","Vännäs","Vilhelmina","Åsele","Umeå","Lycksele","Skellefteå","Norrbottens län","Arvidsjaur","Arjeplog","Jokkmokk","Överkalix","Kalix","Övertorneå","Pajala","Gällivare","Älvsbyn","Luleå","Piteå","Boden","Haparanda","Kiruna"]

def setPlotlyInclusion(value):
	global includePlotlyInHtml
	includePlotlyInHtml = value

def createDirectories():
	dirs = ["population", "births", "deaths", "immigration", "emigration", "moveins", "moveouts"]

	for d in dirs:
		if not os.path.exists(d):
			os.makedirs(d)

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

def getPredictionAtAge(age, type, sex, firstYear, codeIndex):
	data = None
	line = None

	if type == "immigration":
		data = dataFrameService.getImmigrationData(regionCodes[codeIndex])["dataFrame"]
	elif type == "emigration":
		data = dataFrameService.getEmigrationData(regionCodes[codeIndex])["dataFrame"]
	elif type == "moveins":
		data = dataFrameService.getMoveinsData(regionCodes[codeIndex])["dataFrame"]
	elif type == "moveouts":
		data = dataFrameService.getMoveoutsData(regionCodes[codeIndex])["dataFrame"]

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

def getPopulation_Births_Deaths_Predictions(codeIndex):
	global populationBirthsDeathsPredictionsCache

	if regionCodes[codeIndex] in populationBirthsDeathsPredictionsCache:
		return populationBirthsDeathsPredictionsCache[regionCodes[codeIndex]]

	populationData = dataFrameService.getPopulationData(regionCodes[codeIndex])
	deathsData = dataFrameService.getDeathsData(regionCodes[codeIndex])
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
	malePopulationPredictions.append([maleBirthsPredictions[0] - getPredictionAtAge(0, "moveouts", "male", True, codeIndex)
		+ getPredictionAtAge(0, "moveins", "male", True, codeIndex) - getPredictionAtAge(0, "emigration", "male", True, codeIndex) 
		+ getPredictionAtAge(0, "immigration", "male", True, codeIndex)])
	femalePopulationPredictions.append([femaleBirthsPredictions[0] - getPredictionAtAge(0, "moveouts", "female", True, codeIndex)
		+ getPredictionAtAge(0, "moveins", "female", True, codeIndex) - getPredictionAtAge(0, "emigration", "female", True, codeIndex) 
		+ getPredictionAtAge(0, "immigration", "female", True, codeIndex)])

	sumMales = malePopulationPredictions[0][0]
	sumFemales = femalePopulationPredictions[0][0]
	# X > 0
	for i in range(1, 101):
		malePopulationPredictions.append([max(malesMatrix[i - 1][len(malesMatrix[i - 1]) - 1] - malesDeathsMatrix[i - 1][len(malesMatrix[i - 1]) - 1]
			- getPredictionAtAge(i, "moveouts", "male", True, codeIndex) + getPredictionAtAge(i, "moveins", "male", True, codeIndex)
			- getPredictionAtAge(i, "emigration", "male", True, codeIndex) + getPredictionAtAge(i, "immigration", "male", True, codeIndex), 0)])
		femalePopulationPredictions.append([max(femalesMatrix[i - 1][len(femalesMatrix[i - 1]) - 1] - femalesDeathsMatrix[i - 1][len(femalesMatrix[i - 1]) - 1]
			- getPredictionAtAge(i, "moveouts", "female", True, codeIndex) + getPredictionAtAge(i, "moveins", "female", True, codeIndex)
			- getPredictionAtAge(i, "emigration", "female", True, codeIndex) + getPredictionAtAge(i, "immigration", "female", True, codeIndex), 0)])
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
		malePopulationPredictions[0].append(maleBirthsPredictions[i] - getPredictionAtAge(0, "moveouts", "male", False, codeIndex)
			+ getPredictionAtAge(0, "moveins", "male", False, codeIndex) - getPredictionAtAge(0, "emigration", "male", False, codeIndex) 
			+ getPredictionAtAge(0, "immigration", "male", False, codeIndex))
		femalePopulationPredictions[0].append(femaleBirthsPredictions[i] - getPredictionAtAge(0, "moveouts", "female", False, codeIndex)
			+ getPredictionAtAge(0, "moveins", "female", False, codeIndex) - getPredictionAtAge(0, "emigration", "female", False, codeIndex) 
			+ getPredictionAtAge(0, "immigration", "female", False, codeIndex))

		sumMales = malePopulationPredictions[0][i]
		sumFemales = femalePopulationPredictions[0][i]

		# X > 0
		for j in range(1, 101):
			malePopulationPredictions[j].append(max(malePopulationPredictions[j - 1][i - 1] + maleDeathsPredictions[j - 1][i - 1]
				- getPredictionAtAge(j, "moveouts", "male", False, codeIndex) + getPredictionAtAge(j, "moveins", "male", False, codeIndex)
				- getPredictionAtAge(j, "emigration", "male", False, codeIndex) + getPredictionAtAge(j, "immigration", "male", False, codeIndex), 0))
			femalePopulationPredictions[j].append(max(femalePopulationPredictions[j - 1][i - 1] + femaleDeathsPredictions[j - 1][i - 1]
				- getPredictionAtAge(j, "moveouts", "female", False, codeIndex) + getPredictionAtAge(j, "moveins", "female", False, codeIndex)
				- getPredictionAtAge(j, "emigration", "female", False, codeIndex) + getPredictionAtAge(j, "immigration", "female", False, codeIndex), 0))
			sumMales += malePopulationPredictions[j][i]
			sumFemales += femalePopulationPredictions[j][i]
		malePopulationTotalPredictions.append(sumMales)
		femalePopulationTotalPredictions.append(sumFemales)

	populationBirthsDeathsPredictionsCache[regionCodes[codeIndex]] = {"male" : {"populationPredictions" : malePopulationTotalPredictions, "birthsPredictions" : maleBirthsPredictions, "deathsPredictions" : maleDeathsTotalPredictions},
											"female" : {"populationPredictions" : femalePopulationTotalPredictions, "birthsPredictions" : femaleBirthsPredictions, "deathsPredictions" : femaleDeathsTotalPredictions}}

	return populationBirthsDeathsPredictionsCache[regionCodes[codeIndex]]

def plotRisk(data, fileName, figTitle, codeIndex):
	trace0 = go.Scatter(y = data["scb"], name = 'SCB data', line = dict(color = 'blue'))
	trace1 = go.Scatter(y = data["komm"], name = 'Kommun medel', line = dict(color = 'red'))
	layout = go.Layout(title = figTitle)
	plot(go.Figure(data = [trace0, trace1], layout = layout), filename = fileName + regionCodeValues[codeIndex] + ".html")

def plotMaleRisk(startIndex, endIndex):
	dataScb = dataFrameService.getDeathRiskScbData()

	for codeIndex in range(startIndex, endIndex):
		dataKomm = dataFrameService.getDeathRiskKommData(regionCodes[codeIndex])
		data = {"scb" : dataScb["males"], "komm" : dataKomm["males"]}
		plotRisk(data, "deaths/deathRiskMales_", "Males death risk", codeIndex)

def plotFemaleRisk(startIndex, endIndex):
	dataScb = dataFrameService.getDeathRiskScbData()

	for codeIndex in range(startIndex, endIndex):
		dataKomm = dataFrameService.getDeathRiskKommData(regionCodes[codeIndex])
		data = {"scb" : dataScb["females"], "komm" : dataKomm["females"]}
		plotRisk(data, "deaths/deathRiskFemales_", "Females death risk", codeIndex)

def plotFertilityGraph(startIndex, endIndex):
	tfrSverige = dataFrameService.getTfrSverige()
	x = numpy.arange(14, 46, 1)

	for codeIndex in range(startIndex, endIndex):
		tfrKommData = dataFrameService.getTfrKommData(regionCodes[codeIndex])
		trace0 = go.Scatter(y = tfrSverige, x = x, name = 'TFR Sverige', line = dict(color = 'blue'))
		trace1 = go.Scatter(y = tfrKommData["avgTfrKomm"], x = x, name = 'Average TFR Kommunen', line = dict(color = 'red'))
		trace2 = go.Scatter(y = tfrKommData["tfrKomm2017"], x = x, name = 'TFR Kommunen 2017', line = dict(color = 'yellow'))
		trace3 = go.Scatter(y = tfrKommData["tfrKomm2012_2017"], x = x, name = 'TFR Kommunen 2012-2017', line = dict(color = 'green'))
		layout = go.Layout(title = "Total fertility rate", xaxis = dict(title = "Age"), yaxis = dict(title = "Percentage"))

		plot(go.Figure(data = [trace0, trace1, trace2, trace3], layout = layout), filename = "births/fertilityGraph_" + regionCodes[codeIndex] + ".html", include_plotlyjs=includePlotlyInHtml)

def plotDataFrameGraph(df, predictions, fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex):
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
	plot(go.Figure(data = data, layout = layout), filename = fileName + regionCodeValues[codeIndex] + ".html", include_plotlyjs=includePlotlyInHtml)

def plotPopulationByGenderGraph(startIndex, endIndex):
	fileName = "population/populationByGender_";
	figTitle = "Total population by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Population"

	for codeIndex in range(startIndex, endIndex):
		predictions = getPopulation_Births_Deaths_Predictions(codeIndex)
		populationPredictions = {"malePrediction" : predictions["male"]["populationPredictions"], "femalePrediction" : predictions["female"]["populationPredictions"]}
		plotDataFrameGraph(dataFrameService.getPopulationByGenderDataframe(regionCodes[codeIndex]), populationPredictions, fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)


def plotBirthsByGenderGraph(startIndex, endIndex):
	fileName = "births/birthsByGender_";
	figTitle = "Births by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Births"

	for codeIndex in range(startIndex, endIndex):
		predictions = getPopulation_Births_Deaths_Predictions(codeIndex)
		birthsPredictions = {"malePrediction" : predictions["male"]["birthsPredictions"], "femalePrediction" : predictions["female"]["birthsPredictions"]}
		plotDataFrameGraph(dataFrameService.getBirthsByGenderDataFrame(regionCodes[codeIndex]), birthsPredictions, fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)

def plotDeathsByGenderGraph(startIndex, endIndex):
	fileName = "deaths/deathsByGender_";
	figTitle = "Deaths by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Deaths"
	
	for codeIndex in range(startIndex, endIndex):
		predictions = getPopulation_Births_Deaths_Predictions(codeIndex)
		deathsPredictions = {"malePrediction" : predictions["male"]["deathsPredictions"], "femalePrediction" : predictions["female"]["deathsPredictions"]}
		plotDataFrameGraph(dataFrameService.getDeathsByGenderDataFrame(regionCodes[codeIndex]), deathsPredictions, fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)

def plotImmigrationByGenderGraph(startIndex, endIndex):
	fileName = "immigration/immigrationByGender_";
	figTitle = "Immigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	for codeIndex in range(startIndex, endIndex):
		immigrationDataFrame = dataFrameService.getImmigrationByGenderDataFrame(regionCodes[codeIndex])
		plotDataFrameGraph(immigrationDataFrame, calculatePredictions(immigrationDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)

def plotEmigrationByGenderGraph(startIndex, endIndex):
	fileName = "emigration/emigrationByGender_";
	figTitle = "Emigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	for codeIndex in range(startIndex, endIndex):
		emigrationDataFrame = dataFrameService.getEmigrationByGenderDataFrame(regionCodes[codeIndex])
		plotDataFrameGraph(emigrationDataFrame, calculatePredictions(emigrationDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)

def plotMoveinsByGenderGraph(startIndex, endIndex):
	fileName = "moveins/moveinsByGender_";
	figTitle = "Moveins within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	for codeIndex in range(startIndex, endIndex):
		moveinsDataFrame = dataFrameService.getMoveinsByGenderDataFrame(regionCodes[codeIndex])
		plotDataFrameGraph(moveinsDataFrame, calculatePredictions(moveinsDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)

def plotMoveoutsByGenderGraph(startIndex, endIndex):
	fileName = "moveouts/moveoutsByGender_";
	figTitle = "Moveouts within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"

	for codeIndex in range(startIndex, endIndex):
		moveoutsDataFrame = dataFrameService.getMoveoutsByGenderDataFrame(regionCodes[codeIndex]) 
		plotDataFrameGraph(moveoutsDataFrame, calculatePredictions(moveoutsDataFrame), fileName, figTitle, xAxisTitle, yAxisTitle, codeIndex)

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

def plotMalePopulationHeatmap(withNumbers, startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		dataFrame = dataFrameService.getPopulationData(regionCodes[codeIndex])
		plotPopulationHeatMap(withNumbers, dataFrame["years"], dataFrame["dataFrame"]["malesMatrix"], "Male population heatmap", "malesHeatmap_" + regionCodeValues[codeIndex] + ".html")

def plotFemalePopulationHeatmap(withNumbers, startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		dataFrame = dataFrameService.getPopulationData(regionCodes[codeIndex])
		plotPopulationHeatMap(withNumbers, dataFrame["years"], dataFrame["dataFrame"]["femalesMatrix"], "Female population heatmap", "femalesHeatmap_" + regionCodeValues[codeIndex] + ".html")


if __name__ == "__main__":
	createDirectories()
	maxIndex = len(regionCodes) - 1
	startIndex = 0
	endIndex = maxIndex
	cmd = input("Include plotlyjs(Y or N, default: N)?: ")
	if cmd == 'Y':
		setPlotlyInclusion(True)

	index1 = input("Select start index for regions(default is 0, 0 <= index < " + str(maxIndex) + "): ")
	index2 = input("Select end index for regions(default is " + str(maxIndex) + ", 0 < index <= " + str(maxIndex) + "): ")
	
	if index1:
		startIndex = int(index1)

	if index2:
		endIndex = int(index2)

	if startIndex < 0 or startIndex >= maxIndex or endIndex <= 0 or endIndex > maxIndex:
		print("Wrong indexes")
		exit()

	print("Start index: ", startIndex)
	print("End index: ", endIndex)

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
			plotPopulationByGenderGraph(startIndex, endIndex)
		elif cmd == '2':
			plotBirthsByGenderGraph(startIndex, endIndex)
		elif cmd == '3':
			plotDeathsByGenderGraph(startIndex, endIndex)
		elif cmd == '4':
			plotImmigrationByGenderGraph(startIndex, endIndex)
		elif cmd == '5':
			plotEmigrationByGenderGraph(startIndex, endIndex)
		elif cmd == '6':
			plotMoveinsByGenderGraph(startIndex, endIndex)
		elif cmd == '7':
			plotMoveoutsByGenderGraph(startIndex, endIndex)
		elif cmd == '8':
			plotMalePopulationHeatmap(True, startIndex, endIndex)
		elif cmd == '9':
			plotFemalePopulationHeatmap(True, startIndex, endIndex)
		elif cmd == '10':
			plotMalePopulationHeatmap(False, startIndex, endIndex)
		elif cmd == '11':
			plotFemalePopulationHeatmap(False, startIndex, endIndex)
		elif cmd == '12':
			plotMaleRisk(startIndex, endIndex)
		elif cmd == '13':
			plotFemaleRisk(startIndex, endIndex)
		elif cmd == '14':
			plotFertilityGraph(startIndex, endIndex)
		elif cmd == 'q':
			break
		else:
			print("Invalid command.")
	
	# data = {1 : ["2", "3"]}
	# if 0 not in data:
	# 	print("no")
	# plotPopulationByGenderGraph(startIndex, endIndex)