import os
from sys import exit
try:
	from numpy import array, log10, sqrt as npSqrt, sum as npSum
	from cv2 import imread
	from scipy.signal import convolve2d
	from scipy.ndimage import variance
	from tqdm import tqdm
except:
	print("The required libraries are not ready. Please check your environments. ")
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)

def mse(imageA, imageB):
	# 计算并返回两个图像之间的均方误差
	err = npSum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err
 
def psnr(imageA, imageB):
	# 计算并返回两个图像之间的峰值信噪比（PSNR）
	mse_value = mse(imageA, imageB)
	if mse_value == 0:  # MSE为0意味着两幅图完全相同，因此PSNR无穷大
		return float('inf')
	MAX_I = 255.0  # 8位图像的最大值
	return 20 * log10(MAX_I / npSqrt(mse_value))
 
def main():
	# Parameters #
	originalFolderPath, stegoFolderPath, outputFilePath, ncols = "clean", "stego", "psnrResults.xlsx", 120
	
	# Algorithms #
	successCnt, totalCnt = 0, 0
	methods = {key:[] for key in os.listdir(stegoFolderPath)}
	for item in tqdm(os.listdir(originalFolderPath), ncols = ncols):
		totalCnt += 1
		imageAFilePath = os.path.join(originalFolderPath, item)
		try:
			imageA = imread(imageAFilePath)
		except:
			continue
		if imageA is None:
			continue
		isASuccess = True
		for method in methods.keys():
			imageBFilePath = os.path.join(os.path.join(stegoFolderPath, method), item)
			if os.path.isfile(imageBFilePath):
				try:
					imageB = imread(imageBFilePath)
				except:
					isASuccess = False
				if imageB is None:
					isASuccess = False
					continue
				methods[method].append(psnr(imageA, imageB))
		if isASuccess:
			successCnt += 1
	for method in tuple(methods.keys()):
		if methods[method]:
			methods[method].insert(0, sum(methods[method]) / len(methods[method]))
		else:
			del methods[method]
	longest = len(max(methods.values(), key = lambda x:len(x)))
	for method in tuple(methods.keys()):
		methods[method] += [None] * (longest - len(methods[method]))
		methods[method].append(methods[method][0])
		del methods[method][0]
	try:
		__import__("pandas").DataFrame(methods).to_excel(outputFilePath, index = False)
	except:
		print(methods)
	if totalCnt:
		print("Successfully procceded {0} / {1} with a success rate of {2:.2f}%. ".format(successCnt, totalCnt, successCnt * 100 / totalCnt))
	else:
		print("Nothing was proceeded. ")
	print("Please press the enter key to exit. ")
	try:
		input()
	except:
		print()
	return EXIT_SUCCESS if successCnt == totalCnt else EXIT_FAILURE
	



if "__main__" == __name__:
	exit(main())