# coding=utf-8

import pandas as pd
import requests as request
import simplejson as simplejson
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot

mainUrl = "http://api.scb.se/OV0104/v1/doris/en/ssd/START/BE/BE0101/"
populationUrl = mainUrl + "BE0101A/BefolkningNy";
birthsUrl = mainUrl + "BE0101H/FoddaK"
headers = {"Content-type": "application/json"};

def getRequestBodyForPopulation():
	return {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}

def getRequestBodyForBirths():
	return {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Kon","selection":{"filter":"item","values":["1","2"]}}],"response":{"format":"json"}}

def getPopulationByGenderDataframe():
	years = []
	numberOfMen = []
	numberOfWomen = []

	# get population by gender 1968 - 2017
	response = request.post(url=populationUrl, json=getRequestBodyForPopulation(), headers=headers);
	json_data = simplejson.loads(response.text)["data"]

	for val in json_data:
		if val["key"][1] == "1":
			years.append(int(val["key"][2]));
			numberOfMen.append(int(val["values"][0]))
		else:
			numberOfWomen.append(int(val["values"][0]))

	populationByGenderDf = pd.DataFrame(data={"year": years, "men": numberOfMen, "women": numberOfWomen})

	return populationByGenderDf;

def getBirthsByGenderDataFrame():
	years = []
	numberOfBoys = []
	numberOfGirls = []

	response = request.post(url=birthsUrl, json=getRequestBodyForBirths(), headers=headers);
	json_data = simplejson.loads(response.text)["data"]

	for val in json_data:
		if val["key"][1] == "1":
			years.append(int(val["key"][2]));
			numberOfBoys.append(int(val["values"][0]))
		else:
			numberOfGirls.append(int(val["values"][0]))

	birthsByGenderDf = pd.DataFrame(data={"year": years, "boys": numberOfBoys, "girls": numberOfGirls})

	return birthsByGenderDf


def plotPopulationByGenderGraph(df):
	trace0 = go.Scatter(x = df['year'], y = df['men'], name = 'men', line = dict(color='blue'))
	trace1 = go.Scatter(x = df['year'], y = df['women'], name = 'women', line = dict(color='red'))

	layout = go.Layout(title= "Total population by gender",  xaxis = dict(title = 'Year'), yaxis = dict(title = 'Population'))
	plot(go.Figure(data = [trace0, trace1], layout=layout), filename='populationByGender.html')

def plotBirthsByGenderGraph(df):
	trace0 = go.Scatter(x=df['year'], y=df['boys'], name='boys', line = dict(color='blue'))
	trace1 = go.Scatter(x=df['year'], y=df['girls'], name='girls', line = dict(color='red'))

	layout = go.Layout(title= "Births by gender", xaxis = dict(title = 'Year'), yaxis = dict(title = 'Births'))
	plot(go.Figure(data = [trace0, trace1], layout=layout), filename='birthsByGender.html')


if __name__ == "__main__":
	plotPopulationByGenderGraph(getPopulationByGenderDataframe());
	plotBirthsByGenderGraph(getBirthsByGenderDataFrame());
