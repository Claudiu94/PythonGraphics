from plotly.offline import download_plotlyjs, plot
import dataFrameCrawler as dataFrameService
import plotly.graph_objs as go
from termcolor import colored
import graphsHelper as gh
import numpy as numpy

regionCodes = ["0114","0115","0117","0120","0123","0125","0126","0127","0128","0136","0138","0139","0140","0160","0162","0163","0180","0181","0182","0183","0184","0186","0187","0188","0191","0192","03","0305","0319","0330","0331","0360","0380","0381","0382","04","0428","0461","0480","0481","0482","0483","0484","0486","0488","05","0509","0512","0513","0560","0561","0562","0563","0580","0581","0582","0583","0584","0586","06","0604","0617","0642","0643","0662","0665","0680","0682","0683","0684","0685","0686","0687","07","0760","0761","0763","0764","0765","0767","0780","0781","08","0821","0834","0840","0860","0861","0862","0880","0881","0882","0883","0884","0885","09","0980","10","1060","1080","1081","1082","1083","12","1214","1230","1231","1233","1256","1257","1260","1261","1262","1263","1264","1265","1266","1267","1270","1272","1273","1275","1276","1277","1278","1280","1281","1282","1283","1284","1285","1286","1287","1290","1291","1292","1293","13","1315","1380","1381","1382","1383","1384","14","1401","1402","1407","1415","1419","1421","1427","1430","1435","1438","1439","1440","1441","1442","1443","1444","1445","1446","1447","1452","1460","1461","1462","1463","1465","1466","1470","1471","1472","1473","1480","1481","1482","1484","1485","1486","1487","1488","1489","1490","1491","1492","1493","1494","1495","1496","1497","1498","1499","17","1715","1730","1737","1760","1761","1762","1763","1764","1765","1766","1780","1781","1782","1783","1784","1785","18","1814","1860","1861","1862","1863","1864","1880","1881","1882","1883","1884","1885","19","1904","1907","1960","1961","1962","1980","1981","1982","1983","1984","20","2021","2023","2026","2029","2031","2034","2039","2061","2062","2080","2081","2082","2083","2084","2085","21","2101","2104","2121","2132","2161","2180","2181","2182","2183","2184","22","2260","2262","2280","2281","2282","2283","2284","23","2303","2305","2309","2313","2321","2326","2361","2380","24","2401","2403","2404","2409","2417","2418","2421","2422","2425","2460","2462","2463","2480","2481","2482","25","2505","2506","2510","2513","2514","2518","2521","2523","2560","2580","2581","2582","2583","2584"]
regionCodeValues = ["Upplands Väsby","Vallentuna","Österåker","Värmdö","Järfälla","Ekerö","Huddinge","Botkyrka","Salem","Haninge","Tyresö","Upplands-Bro","Nykvarn","Täby","Danderyd","Sollentuna","Stockholm","Södertälje","Nacka","Sundbyberg","Solna","Lidingö","Vaxholm","Norrtälje","Sigtuna","Nynäshamn","Uppsala län","Håbo","Älvkarleby","Knivsta","Heby","Tierp","Uppsala","Enköping","Östhammar","Södermanlands län","Vingåker","Gnesta","Nyköping","Oxelösund","Flen","Katrineholm","Eskilstuna","Strängnäs","Trosa","Östergötlands län","Ödeshög","Ydre","Kinda","Boxholm","Åtvidaberg","Finspång","Valdemarsvik","Linköping","Norrköping","Söderköping","Motala","Vadstena","Mjölby","Jönköpings län","Aneby","Gnosjö","Mullsjö","Habo","Gislaved","Vaggeryd","Jönköping","Nässjö","Värnamo","Sävsjö","Vetlanda","Eksjö","Tranås","Kronobergs län","Uppvidinge","Lessebo","Tingsryd","Alvesta","Älmhult","Markaryd","Växjö","Ljungby","Kalmar län","Högsby","Torsås","Mörbylånga","Hultsfred","Mönsterås","Emmaboda","Kalmar","Nybro","Oskarshamn","Västervik","Vimmerby","Borgholm","Gotlands län","Gotland","Blekinge län","Olofström","Karlskrona","Ronneby","Karlshamn","Sölvesborg","Skåne län","Svalöv","Staffanstorp","Burlöv","Vellinge","Östra Göinge","Örkelljunga","Bjuv","Kävlinge","Lomma","Svedala","Skurup","Sjöbo","Hörby","Höör","Tomelilla","Bromölla","Osby","Perstorp","Klippan","Åstorp","Båstad","Malmö","Lund","Landskrona","Helsingborg","Höganäs","Eslöv","Ystad","Trelleborg","Kristianstad","Simrishamn","Ängelholm","Hässleholm","Hallands län","Hylte","Halmstad","Laholm","Falkenberg","Varberg","Kungsbacka","Västra Götalands län","Härryda","Partille","Öckerö","Stenungsund","Tjörn","Orust","Sotenäs","Munkedal","Tanum","Dals-Ed","Färgelanda","Ale","Lerum","Vårgårda","Bollebygd","Grästorp","Essunga","Karlsborg","Gullspång","Tranemo","Bengtsfors","Mellerud","Lilla Edet","Mark","Svenljunga","Herrljunga","Vara","Götene","Tibro","Töreboda","Göteborg","Mölndal","Kungälv","Lysekil","Uddevalla","Strömstad","Vänersborg","Trollhättan","Alingsås","Borås","Ulricehamn","Åmål","Mariestad","Lidköping","Skara","Skövde","Hjo","Tidaholm","Falköping","Värmlands län","Kil","Eda","Torsby","Storfors","Hammarö","Munkfors","Forshaga","Grums","Årjäng","Sunne","Karlstad","Kristinehamn","Filipstad","Hagfors","Arvika","Säffle","Örebro län","Lekeberg","Laxå","Hallsberg","Degerfors","Hällefors","Ljusnarsberg","Örebro","Kumla","Askersund","Karlskoga","Nora","Lindesberg","Västmanlands län","Skinnskatteberg","Surahammar","Kungsör","Hallstahammar","Norberg","Västerås","Sala","Fagersta","Köping","Arboga","Dalarnas län","Vansbro","Malung-Sälen","Gagnef","Leksand","Rättvik","Orsa","Älvdalen","Smedjebacken","Mora","Falun","Borlänge","Säter","Hedemora","Avesta","Ludvika","Gävleborgs län","Ockelbo","Hofors","Ovanåker","Nordanstig","Ljusdal","Gävle","Sandviken","Söderhamn","Bollnäs","Hudiksvall","Västernorrlands län","Ånge","Timrå","Härnösand","Sundsvall","Kramfors","Sollefteå","Örnsköldsvik","Jämtlands län","Ragunda","Bräcke","Krokom","Strömsund","Åre","Berg","Härjedalen","Östersund","Västerbottens län","Nordmaling","Bjurholm","Vindeln","Robertsfors","Norsjö","Malå","Storuman","Sorsele","Dorotea","Vännäs","Vilhelmina","Åsele","Umeå","Lycksele","Skellefteå","Norrbottens län","Arvidsjaur","Arjeplog","Jokkmokk","Överkalix","Kalix","Övertorneå","Pajala","Gällivare","Älvsbyn","Luleå","Piteå","Boden","Haparanda","Kiruna"]

includePlotlyInHtml = False
auto_open = False
colors = ["blue", "red", "yellow"]

def setAutoOpen(value):
	global auto_open
	auto_open = value

def setPlotlyInclusion(value):
	global includePlotlyInHtml
	includePlotlyInHtml = value

def graph2ProcessData(dataList):
	for i in range(1, len(dataList)):
		dataList[i] = dataList[i] + dataList[i - 1]

	return dataList

def getNumberOfApartments(code):
	return sum(dataFrameService.getNumberOfAppartmentsData(code)["dataFrame"]["FLERBOST"])

def plotBarHousesData(startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		try:
			dataDict = dataFrameService.getNumberOfAppartmentsData(regionCodes[codeIndex])
			dataFrame = dataDict["dataFrame"]
			years = dataDict["years"]
			data = []
			index = 0
			
			for key in dataFrame:
				data.append(go.Bar(x = years, y = dataFrame[key], name = key, marker = dict(color = colors[index])))
				index += 1

			layout = go.Layout(barmode = 'stack', title = "Fördelning över byggår för bestånd per 2017")
			plot(go.Figure(data = data, layout = layout), filename = "houses/fördelning_över_byggår_för_bestånd_per_2017_" + regionCodeValues[codeIndex] + ".html", include_plotlyjs = includePlotlyInHtml, auto_open = auto_open)
		except ValueError as err:
			print(colored("[Fördelning över byggår för bestånd per 2017]", "red"), " No data for region: ", regionCodeValues[regionCodes.index(err.args[1])], " code: ", err.args[1])

def plotLineHosesData(startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		try:
			dataDict = dataFrameService.getNumberOfAppartmentsData(regionCodes[codeIndex])
			dataFrame = dataDict["dataFrame"]
			years = dataDict["years"]
			data = []
			index = 0
			lastLists = []

			for key in dataFrame:
				initialValues = graph2ProcessData(list(dataFrame[key]))
				y = initialValues

				for l in lastLists:
					y = list(numpy.add(y, l))
				data.append(go.Scatter(x = years, y = y, text = initialValues, hoverinfo = 'text', name = key, marker = dict(color = colors[index], opacity = 0.2, line = dict(color = colors[index])), fill = 'tonexty'))
				index += 1
				lastLists.append(initialValues)

			layout = go.Layout(title = "Bestånd idag ackumulerat efer byggnadsår")
			plot(go.Figure(data = data, layout = layout), filename = "houses/bestånd_idag_ackumulerat_efer_byggnadsår_" + regionCodeValues[codeIndex] + ".html", include_plotlyjs = includePlotlyInHtml, auto_open = auto_open)
		except ValueError as err:
			print(colored("[Bestånd idag ackumulerat efer byggnadsår]", "red"), " No data for region: ", regionCodeValues[regionCodes.index(err.args[1])], " code: ", err.args[1])

def plotPieChartHousesData(startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		try:
			dataFrame = dataFrameService.getNumberOfAppartmentsData(regionCodes[codeIndex])["dataFrame"]
			labels = []
			values = []

			for key in dataFrame:
				labels.append(key)
				values.append(sum(dataFrame[key]))

			layout = go.Layout(barmode = 'stack', title = "Fördelning av lågenheter")
			plot(go.Figure(data = [go.Pie(labels=labels, values=values)], layout = layout), filename = "houses/fördelning_av_lågenheter_ " + regionCodeValues[codeIndex] + ".html", include_plotlyjs = includePlotlyInHtml, auto_open = auto_open)
		except ValueError as err:
			print(colored("[Fördelning av lågenheter]", "red"), " No data for region: ", regionCodeValues[regionCodes.index(err.args[1])], " code: ", err.args[1])

def plotHolidayHosesPerYear(startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		try:
			dataFrame = dataFrameService.getNumberOfHolidaysByRegion(regionCodes[codeIndex])
			data = [go.Scatter(y = dataFrame["data"], x = dataFrame["years"], line = dict(color = 'blue'))]
			layout = go.Layout(title = "Antal fritidshus mot År", xaxis = dict(title = "År"), yaxis = dict(title = "Antal fritidshus", range=[min(dataFrame["data"]), max(dataFrame["data"])]))
			plot(go.Figure(data = data, layout = layout), filename = "houses/antal_fritidshus_År_" + regionCodeValues[codeIndex] + ".html", include_plotlyjs = True, auto_open = True)
		except ValueError as err:
				print(colored("[Antal fritidshus mot År]", "red"), " No data for region: ", regionCodeValues[regionCodes.index(err.args[1])], " code: ", err.args[1])

def plotTable2Graph2(startIndex, endIndex):
	for codeIndex in range(startIndex, endIndex):
		try:
			dataFrame = dataFrameService.getNumberOfHolidaysByRegion(regionCodes[codeIndex])
			y = dataFrame["data"]
			trace0 = go.Scatter(x = dataFrame["years"], y = y, text = y, hoverinfo = 'text', marker = dict(color = "blue", opacity = 0.2, line = dict(color = "blue")), fill = 'tonexty')
			text = len(y) * [getNumberOfApartments(regionCodes[codeIndex])]
			trace1 = go.Scatter(x = dataFrame["years"], y = y + text, text = text, hoverinfo = 'text', marker = dict(color = "red", opacity = 0.2, line = dict(color = "red")), fill = 'tonexty')
			layout = go.Layout(title = "Antal fritidshus, Antal lagenheter och Antal Bostandshus", xaxis = dict(title = "År"))
			plot(go.Figure(data = [trace0, trace1], layout = layout), filename = "houses/antal_fritidshus_antal_lagenheter_och_antal_bostandshus_" + regionCodeValues[codeIndex] + ".html", include_plotlyjs = True, auto_open = True)
		except ValueError as err:
				print(colored("[Antal fritidshus, Antal lagenheter och Antal Bostandshus]", "red"), " No data for region: ", regionCodeValues[regionCodes.index(err.args[1])], " code: ", err.args[1])

if __name__ == "__main__":
	gh.createDirectories(["houses"])

	maxIndex = len(regionCodes) - 1
	startIndex = 0
	endIndex = maxIndex
	cmd = input("Include plotlyjs(Y or N, default: N)?: ")
	if cmd == 'Y':
		setPlotlyInclusion(True)

	cmd = input("Open each file after creation(Y or N, default: N)?: ")
	if cmd == 'Y':
		setAutoOpen(True)

	index1 = input("Select start index for regions(default is 0, 0 <= index < " + str(maxIndex) + "): ")
	index2 = input("Select end index for regions(default is " + str(maxIndex) + ", 0 < index <= " + str(maxIndex) + "): ")
	
	if index1:
		startIndex = int(index1)

	if index2:
		endIndex = int(index2)

	if startIndex < 0 or startIndex >= maxIndex or endIndex <= 0 or endIndex > maxIndex:
		print("Wrong indexes")
		exit()
	
	startIndex = regionCodes.index("0885")
	endIndex = startIndex + 1
	
	print("Start index: ", startIndex)
	print("End index: ", endIndex)

	initial_text = """
	1. Fördelning över byggår för bestånd per 2017
	2. Bestånd idag ackumulerat efer byggnadsår
	3. Fördelning av lågenheter
	4. Antal fritidshus mot År
	5. Antal fritidshus, Antal lagenheter och Antal Bostandshus
	"""

	print(initial_text)

	while True:
		cmd = input("\nEnter a number to select graph, or q to exit: ")
		if cmd == '1':
			plotBarHousesData(startIndex, endIndex)
		elif cmd == '2':
			plotLineHosesData(startIndex, endIndex)
		elif cmd == '3':
			plotPieChartHousesData(startIndex, endIndex)
		elif cmd == '4':
			plotHolidayHosesPerYear(startIndex, endIndex)
		elif cmd == '5':
			plotTable2Graph2(startIndex, endIndex)
		elif cmd == 'q':
			break
		else:
			print("Invalid command.")
	# getNumberOfApartments()