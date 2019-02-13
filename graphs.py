# coding=utf-8

import matplotlib.pyplot as plt
import pandas as pd
import requests as request
import simplejson as simplejson
import plotly
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def getRequestBodyForMalePopulation():
	body = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":[]}},{"code":"Kon","selection":{"filter":"item","values":["1"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}

	return body; 

def getRequestBodyForFemalePopulation():
	body = {"query":[{"code":"Region","selection":{"filter":"vs:RegionKommun07","values":["0885"]}},{"code":"Alder","selection":{"filter":"vs:Ålder1årA","values":[]}},{"code":"Kon","selection":{"filter":"item","values":["2"]}},{"code":"ContentsCode","selection":{"filter":"item","values":["BE0101N1"]}}],"response":{"format":"json"}}


	return body

def plotPopulationByGender():
	headers = {"Content-type": "application/json"};
	url = "http://api.scb.se/OV0104/v1/doris/en/ssd/START/BE/BE0101/BE0101A/BefolkningNy";
	years = []
	numberOfMen = []
	numberOfWomen = []

	# get number of men
	response = request.post(url=url, json=getRequestBodyForMalePopulation(), headers=headers);
	json_data_men = simplejson.loads(response.text)["data"]

	# get numbet of women
	response = request.post(url=url, json=getRequestBodyForFemalePopulation(), headers=headers);
	json_data_women = simplejson.loads(response.text)["data"]

	for val in json_data_men:
		years.append(int(val["key"][2]));
		numberOfMen.append(int(val["values"][0]))

	for val in json_data_women:
		numberOfWomen.append(int(val["values"][0]))

	data = {
		"year": years,
		"men": numberOfMen,
		"women": numberOfWomen
	}

	df = pd.DataFrame(data=data)
	# print df['men']
	# plot data
	# gca stands for 'get current axis'
	# ax = plt.gca()
	# df.plot(kind='line',x='year',y='women',ax=ax, color='red')
	# df.plot(kind='line',x='year',y='men',ax=ax, title='Total population by gender')
	# plt.show()

	# save with plotly
	trace0 = go.Scatter(
    	x=df['year'],
    	y=df['men'],
    	name='men'
	)
	trace1 = go.Scatter(
    	x=df['year'],
    	y=df['women'],
    	name='women'
	)

	layout = go.Layout(title= "Total population by gender")
	plot(go.Figure(data = [trace0, trace1], layout=layout))

if __name__ == "__main__":
	plotPopulationByGender();
