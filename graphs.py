# coding=utf-8

from plotly.offline import download_plotlyjs, plot
import simplejson as simplejson
import plotly.graph_objs as go
import requests as request
import pandas as pd

headers = {"Content-type": "application/json"}
mainUrl = "http://api.scb.se/OV0104/v1/doris/en/ssd/START/BE/BE0101/"

def getDataFrame(statsUrl, jsonBody):
	years = []
	malesNumber = []
	femalesNumber = []

	response = request.post(url = statsUrl, json = jsonBody, headers = headers);
	json_data = simplejson.loads(response.text)["data"]

	for val in json_data:
		if val["key"][1] == "1":
			years.append(int(val["key"][2]));
			malesNumber.append(int(val["values"][0]))
		else:
			femalesNumber.append(int(val["values"][0]))

	dataFrame = pd.DataFrame(data = {"year": years, "male": malesNumber, "female": femalesNumber})

	return dataFrame;

def getPopulationYearByYearDataFrame():
	populationUrl = mainUrl + "BE0101A/BefolkningNy"
	requestBodyYearByYear = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100+"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}
	matrix = [];
	
	response = request.post(url = populationUrl, json = requestBodyYearByYear, headers = headers);
	print response.text
	json_data = simplejson.loads(response.text)["data"]

def getPopulationByGenderDataframe():
	populationUrl = mainUrl + "BE0101A/BefolkningNy"
	requestBodyForPopulation = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}};

	return getDataFrame(populationUrl, requestBodyForPopulation)

def getBirthsByGenderDataFrame():
	birthsUrl = mainUrl + "BE0101H/FoddaK"
	requestBodyForBirths = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}

	return getDataFrame(birthsUrl, requestBodyForBirths)

def getDeathsByGenderDataFrame():
	deathsUrl = mainUrl + "BE0101I/DodaFodelsearK"
	requestBodyForDeaths = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}

	return getDataFrame(deathsUrl, requestBodyForDeaths)

def getImmigrationByGenderDataFrame():
	immgrationUrl = mainUrl + "BE0101J/Flyttningar97"
	requestBodyForImmigration = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AX"]}}],"response":{"format":"json"}}

	return getDataFrame(immgrationUrl, requestBodyForImmigration)

def getEmigrationByGenderDataFrame():
	emigrationUrl = mainUrl + "BE0101J/Flyttningar97"
	requestBodyForEmigration = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101AY"]}}],"response":{"format":"json"}}	
	dataFrameEmigration = getDataFrame(emigrationUrl, requestBodyForEmigration)
	dataFrameEmigration["male"] *= -1
	dataFrameEmigration["female"] *= -1

	return dataFrameEmigration

def getMoveinsByGenderDataFrame():	
	moveinssaUrl = mainUrl + "BE0101J/Flyttningar97"
	requestBodyForMoveins = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A2"]}}],"response":{"format":"json"}}

	return getDataFrame(moveinssaUrl, requestBodyForMoveins)

def getMoveoutsByGenderDataFrame():
	moveoutsaUrl = mainUrl + "BE0101J/Flyttningar97"
	requestBodyForMoveouts = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07EjAggr","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101A3"]}}],"response":{"format":"json"}}
	dataFrameMoveouts = getDataFrame(moveoutsaUrl, requestBodyForMoveouts)
	dataFrameMoveouts["male"] *= -1
	dataFrameMoveouts["female"] *= -1

	return dataFrameMoveouts

def plotDataFrameGraph(df, fileName, figTitle, xAxisTitle, yAxisTitle):
	trace0 = go.Scatter(x = df['year'], y = df['male'], name = 'males', line = dict(color = 'blue'))
	trace1 = go.Scatter(x = df['year'], y = df['female'], name = 'females', line = dict(color = 'red'))
	layout = go.Layout(title = figTitle,  xaxis = dict(title = xAxisTitle), yaxis = dict(title = yAxisTitle))

	plot(go.Figure(data = [trace0, trace1], layout = layout), filename = fileName)

def plotPopulationByGenderGraph():
	fileName = "populationByGender.html";
	figTitle = "Total population by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Population"
	plotDataFrameGraph(getPopulationByGenderDataframe(), fileName, figTitle, xAxisTitle, yAxisTitle)


def plotBirthsByGenderGraph():
	fileName = "birthsByGender.html";
	figTitle = "Births by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Births"
	plotDataFrameGraph(getBirthsByGenderDataFrame(), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotDeathsByGenderGraph():
	fileName = "deathsByGender.html";
	figTitle = "Deaths by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Deaths"
	plotDataFrameGraph(getDeathsByGenderDataFrame(), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotImmigrationByGenderGraph():
	fileName = "immigrationByGender.html";
	figTitle = "Immigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"
	plotDataFrameGraph(getImmigrationByGenderDataFrame(), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotEmigrationByGenderGraph():
	fileName = "emigrationByGender.html";
	figTitle = "Emigration by gender";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"
	plotDataFrameGraph(getEmigrationByGenderDataFrame(), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotMoveinsByGenderGraph():
	fileName = "moveinsByGender.html";
	figTitle = "Moveins within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"
	plotDataFrameGraph(getMoveinsByGenderDataFrame(), fileName, figTitle, xAxisTitle, yAxisTitle)

def plotMoveoutsByGenderGraph():
	fileName = "moveoutsByGender.html";
	figTitle = "Moveouts within country";
	xAxisTitle = "Year"
	yAxisTitle = "Persons"
	plotDataFrameGraph(getMoveoutsByGenderDataFrame(), fileName, figTitle, xAxisTitle, yAxisTitle)


if __name__ == "__main__":
	# plotPopulationByGenderGraph()
	# plotBirthsByGenderGraph()
	# plotDeathsByGenderGraph()
	# plotImmigrationByGenderGraph()
	# plotEmigrationByGenderGraph()
	# plotMoveinsByGenderGraph()
	# plotMoveoutsByGenderGraph()
	getPopulationYearByYearDataFrame()
