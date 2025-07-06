import os
from sys import exit
try:
	from cv2 import imread, imwrite
	from tqdm import tqdm
except:
	print("Failed importing imread, imwrite, or tqdm. Please press the enter key to exit. ")
	input()
	exit(-1)
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
inputFolderPath = "stego"
originalName = "0"
outputFolderPathFormat = "differential/{0}"


def gainOriginals(originalPath:str, ncols:int = 120) -> dict:
	originals = {}
	for root, dirs, files in os.walk(originalPath):
		for f in tqdm(files, desc = "Reading \"{0}\"".format(originalPath), ncols = ncols):
			path = os.path.join(root, f)
			originals[f] = imread(path)
	return originals

def handleFolder(folder:str) -> bool:
	if folder in ("", ".", "./", ".\\"):
		return True
	elif os.path.exists(folder):
		return os.path.isdir(folder)
	else:
		try:
			os.makedirs(folder)
			return True
		except:
			return False

def handleDifferential(inputFp:str, originals:dict, outputFp:str, ncols:int = 100) -> tuple:
	successCnt = 0
	totalCnt = 0
	for root, dirs, files in os.walk(inputFp):
		for f in tqdm(files, desc = "Handling \"{0}\"".format(outputFp), ncols = ncols):
			fromPath = os.path.join(root, f)
			toPath = os.path.join(outputFp, os.path.relpath(fromPath, inputFp))
			if not os.path.isfile(toPath):
				totalCnt += 1
				if handleFolder(os.path.split(toPath)[0]):
					try:
						imwrite(toPath, imread(fromPath) - originals[f])
						successCnt += 1
					except:
						pass
	return (successCnt, totalCnt)

def main() -> int:
	successCount = 0
	totalCount = 0
	originals = gainOriginals(os.path.join(inputFolderPath, originalName))
	for categoryName in os.listdir(inputFolderPath):
		if categoryName != originalName:
			categoryPath = os.path.join(inputFolderPath, categoryName)
			if os.path.isdir(categoryPath):
				successCnt, totalCnt = handleDifferential(categoryPath, originals, outputFolderPathFormat.format(categoryName))
				successCount += successCnt
				totalCount += totalCnt
	if totalCount:
		print("{0} / {1} = {2}%".format(successCount, totalCount, 100 * successCount / totalCount))
	else:
		print("Nothing was handled. ")
	print("Please press the enter key to exit. ")
	input()
	return EXIT_SUCCESS if successCount == totalCount else EXIT_FAILURE
			


if __name__ == "__main__":
	exit(main())