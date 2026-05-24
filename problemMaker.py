import csv
import glob
import random

voca = []
files = glob.glob("vocabulary/*.tsv")

for file_name in files:
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # 첫 줄(헤더) 건너뛰기
        for row in reader:
            hanzi = row[0]
            pinyin = row[1]
            meaning = row[2]
            voca.append([hanzi, pinyin, meaning])

#단순 랜덤 문제만(엔터치면 다음 문제, 채점 X)

problemType = {"hanzi": 0, "pinyin": 1, "meaning": 2}
testList = voca.copy()
problemNum = 0
while True:
    if problemNum == 0 :
        random.shuffle(testList)
    #아래 problemType을 바꾸면 문제 유형 바꿀 수 있음
    print(f"문제 {problemNum + 1}: {testList[problemNum][problemType['hanzi']]}")
    endCode = input("")
    if endCode != '' :
        break
    print(testList[problemNum])
    problemNum += 1
    if problemNum >= len(testList):
        problemNum = 0
    