populationBirthsDeathsPredictionsCache = {}

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