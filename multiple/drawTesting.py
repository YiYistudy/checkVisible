import os
from sys import exit
try:
	from pandas import read_excel
	import matplotlib.pyplot as plt
	import seaborn as sns
except:
	print("Missing necessary libraries, please press the enter key to exit. ")
	try:
		input()
	except:
		print()
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


def main():
	inputFilePath = "testing.xlsx"
	outputFilePath = "testing.pdf"
	matrix = read_excel(inputFilePath, index_col = 0)
	if matrix.shape[0] == matrix.shape[1]:
		plt.figure(figsize=(8, 6))
		plt.rcParams["font.family"] = "Times New Roman"
		sns.heatmap(matrix, annot = True, cmap = "Blues", fmt = "d", xticklabels = [str(i) for i in range(matrix.shape[0])], yticklabels = [str(i) for i in range(matrix.shape[0])])
		plt.xlabel("Predicted Label")
		plt.ylabel("True Label")
		try:
			plt.savefig(outputFilePath, bbox_inches = "tight")
			print("Successfully saved to \"{0}\". ".format(outputFilePath))
			return EXIT_SUCCESS
		except BaseException as e:
			print("Failed to save the figure to \"{0}\". Details are as follows. \n\t{1}".format(outputFilePath, e))
			try:
				plt.plot()
			except:
				pass
			return EXIT_FAILURE
		plt.close()
	else:
		print("The shape of the matrix is not a square. ")
		return EOF



if "__main__" == __name__:
	exit(main())