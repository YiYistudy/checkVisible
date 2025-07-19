import os
from numpy import log10, mean, sqrt
from pandas import DataFrame as DF
from matplotlib import pyplot as plt
from cv2 import imread, imwrite
from tqdm import tqdm
os.chdir(os.path.abspath(os.path.dirname(__file__)))
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = -1
indexLSB = 1
indexPVD = 3
indexDCT = 2


def computRMSE(img1, img2) -> float:
	mse = mean((img1 - img2) ** 2)
	rmse = sqrt(mse)
	return rmse

def computPSNR(img1, img2) -> float:
	mse = mean((img1 - img2) ** 2)
	if mse == 0:
		return float("inf")
	max_pixel = 255.0
	psnr = 20 * log10(max_pixel / sqrt(mse))
	return psnr

def draw(l:list, saveFigurePath = ["Result1.png", "Result2.png"]) -> bool:
	x = list(range(10, 101, 10))
	y1 = {indexLSB:[], indexPVD:[], indexDCT:[], 7:[], 8:[], 9:[]}
	y2 = {indexLSB:[], indexPVD:[], indexDCT:[], 7:[], 8:[], 9:[]}
	for item in l:
		if item[1] % 10 == 0:
			y1[item[0]].append(item[2])
			y2[item[0]].append(item[3])
	
	# Result 1 #
	plt.rcParams["figure.dpi"] = 300
	plt.rcParams["savefig.dpi"] = 300
	plt.rcParams["font.family"] = "Times New Roman"
	plt.rcParams["mathtext.fontset"] = "stix"
	plt.plot(x, y1[indexLSB], color = "black", marker = "<")
	plt.plot(x, y1[indexPVD], color = "green", marker = "^")
	plt.plot(x, y1[indexDCT], color = "blue", marker = ">")
	plt.plot(x, y1[7], color = "purple", marker = "v")
	plt.plot(x, y1[8], color = "orange", marker = "o")
	plt.plot(x, y1[9], color = "red", marker = "x")
	plt.legend(["LSB", "PVD", "DCT", "Row", "Column", "Block"])
	plt.xlabel("$N(m)$ (Byte)")
	plt.ylabel("RMSE")
	plt.rcParams["figure.dpi"] = 1200
	plt.rcParams["savefig.dpi"] = 1200
	plt.savefig(saveFigurePath[0])
	plt.close()
	
	# Result 2 #
	plt.rcParams["figure.dpi"] = 300
	plt.rcParams["savefig.dpi"] = 300
	plt.rcParams["font.family"] = "Times New Roman"
	plt.rcParams["mathtext.fontset"] = "stix"
	plt.plot(x, y2[indexLSB], color = "black", marker = "<")
	plt.plot(x, y2[indexPVD], color = "green", marker = "^")
	plt.plot(x, y2[indexDCT], color = "blue", marker = ">")
	plt.plot(x, y2[7], color = "purple", marker = "v")
	plt.plot(x, y2[8], color = "orange", marker = "o")
	plt.plot(x, y2[9], color = "red", marker = "x")
	plt.legend(["LSB", "PVD", "DCT", "Row", "Column", "Block"])
	plt.xlabel("$N(m)$ (Byte)")
	plt.ylabel("PSNR")
	plt.rcParams["figure.dpi"] = 1200
	plt.rcParams["savefig.dpi"] = 1200
	plt.savefig(saveFigurePath[1])
	plt.close()

def main():
	successCount, totalCount = 0, 0
	originalPath = "lena_color_256.png"
	try:
		originalImg = imread(originalPath)
	except Exception as e:
		print("Exceptions occurred when reading the original image. Details are as follows. \n{0}".format(e))
		return EOF
	lists = []
	for i in [indexLSB, indexPVD, indexDCT] + list(range(7, 10)):
		if os.path.isdir(str(i)):
			try:
				newList = sorted(os.listdir(str(i)), key = lambda x:int(os.path.splitext(x)[0]))
			except:
				newList = os.listdir(str(i))
			for fname in tqdm(newList, desc = str(i), ncols = 100):
				if os.path.splitext(fname)[1].lower() == ".png":
					stegoPath = os.path.join(str(i), fname)
					stegoImg = imread(stegoPath)
					totalCount += 1
					try:
						lists.append([i, int(os.path.splitext(fname)[0]), computRMSE(originalImg, stegoImg), computPSNR(originalImg, stegoImg)])
						successCount += 1
					except Exception as e:
						pass
	try:
		DF(lists, columns = ["MethodID", "Size", "RMSE", "PSNR"]).to_csv("Result.csv", index = False)
		draw(lists)
	except Exception as e:
		print("Exceptions occurred when writing the result. Details are as follows. \n{0}".format(e))
		return EOF
	return EXIT_SUCCESS if successCount == totalCount else EXIT_FAILURE



if __name__ == "__main__":
	exit(main())