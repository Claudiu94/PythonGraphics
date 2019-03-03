from plotly.offline import download_plotlyjs, plot
import dataFrameCrawler as dataFrameService
import plotly.graph_objs as go
import graphsHelper as gh

includePlotlyInHtml = True
auto_open = True
colors = ["blue", "red", "yellow"]

def processDataframe(dataFrame):
	years = list(dataFrame["keys"])
	dataFrame = dataFrame.drop(columns = ["keys"])
	dataFrame = dataFrame.reindex(["SMÅHUS", "FLERBOST", "ÖVRHUS"], axis=1)

	return {"dataFrame" : dataFrame, "years" : years}

def graph2ProcessData(dataList):
	for i in range(1, len(dataList)):
		dataList[i] = dataList[i] + dataList[i - 1]

	return dataList

def plotBarHousesData(dataDict):
	dataFrame = dataDict["dataFrame"]
	years = dataDict["years"]
	data = []
	index = 0
	
	for key in dataFrame:
		data.append(go.Bar(x = years, y = dataFrame[key], name = key, marker = dict(color = colors[index])))
		index += 1

	layout = go.Layout(barmode = 'stack', title = "Fördelning över byggår för bestånd per 2017")
	plot(go.Figure(data = data, layout = layout), filename = "houses/fördelning_över_byggår_för_bestånd_per_2017.html", include_plotlyjs = includePlotlyInHtml, auto_open = auto_open)

def plotLineHosesData(dataDict):
	dataFrame = dataDict["dataFrame"]
	years = dataDict["years"]
	data = []
	index = 0

	for key in dataFrame:
		y = graph2ProcessData(list(dataFrame[key]))
		data.append(go.Scatter(x = years, y = y, name = key, marker = dict(color = colors[index], opacity = 0.2, line = dict(color = colors[index])), fill = 'tozeroy'))
		index += 1

	layout = go.Layout(title = "Bestånd idag ackumulerat efer byggnadsår")
	plot(go.Figure(data = data, layout = layout), filename = "houses/bestånd_idag_ackumulerat_efer_byggnadsår.html", include_plotlyjs = includePlotlyInHtml, auto_open = auto_open)

def plotPieChartHousesData(dataFrame):
	labels = []
	values = []

	for key in dataFrame:
		labels.append(key)
		values.append(sum(dataFrame[key]))

	layout = go.Layout(barmode = 'stack', title = "Fördelning av lågenheter")
	plot(go.Figure(data = [go.Pie(labels=labels, values=values)], layout = layout), filename = "houses/fördelning_av_lågenheter.html", include_plotlyjs = includePlotlyInHtml, auto_open = auto_open)

if __name__ == "__main__":
	gh.createDirectories(["houses"])
	dataFrame = processDataframe(dataFrameService.getNumberOfAppartmentsData())
	# plotBarHousesData(dataFrame)
	# plotLineHosesData(dataFrame)
	plotPieChartHousesData(dataFrame["dataFrame"])