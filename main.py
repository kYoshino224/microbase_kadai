import numpy as np
import cv2
import sys
from utils.api import get_word_list
from utils.concat_number import concat_number
from utils.character_to_word import character_to_word
from utils.split_region import split_region
from utils.Line import Line
pic_path = sys.argv[1]
img = cv2.imread(pic_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
binary = cv2.threshold(gray, thresh=200, maxval=255, type=cv2.THRESH_BINARY)[1]
edges = cv2.Canny(image=binary, threshold1=100, threshold2=200)
lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=1, maxLineGap=1000)
line_list = []
for i, line in enumerate(lines):
    x1, y1, x2, y2 = line[0]
    line_list.append(Line(x1, y1, x2, y2))

word_list_by_api = get_word_list(input_image_path=pic_path)
number_concatted = concat_number(ocred_list=word_list_by_api)

word_list_with_region = split_region(word_list=number_concatted, line_list=line_list)

for region in word_list_with_region["region"].unique():
    char_list = word_list_with_region[word_list_with_region["region"] == region].sort_values(by="x").reset_index(drop=True)
    word_list = character_to_word(char_list)
    print(word_list)