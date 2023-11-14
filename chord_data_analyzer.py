from cgitb import reset
from random import weibullvariate
from utils.data_manager import DataContainer
from utils import data_analyzer
DATA_PATH = "data/data.json"
DATA_NAME = "chord"
MIN_NOTE = 12 # C1
MAX_NOTE = 96 # C8
DEFAULT_PERSENT = 10

# 노트 개수에 해당하는 모든 점수를 반환
def note_count_score(data):
  result = {}
  for key, item in data.items():
    if len(item[0]) in result.keys():
      result[len(item[0])].append(item[1])
    else:
      result[len(item[0])] = [item[1]]
  return result  
# 코드 데이터 분석 클래스
class ChordDataAnalyzer(DataContainer):
  def __init__(self) -> None:
    super().__init__(DATA_PATH, DATA_NAME)
    self.min_note = MIN_NOTE
    self.max_note = MAX_NOTE
    self.note_count_weight = {}
    self.note_count_databox = {}
    self.default_note_count_weight()
    # self.sum_weight_databox()
  
  def len_data(self):
    return len(self.mydata[self.data_name])
  # 노트 개수에 대한 초기 확률 설정
  def default_note_count_weight(self):
    for i in range(1, self.max_note - self.min_note+2):
      self.note_count_weight[i] = 50
    # print(self.note_count_weight)
  # 노트 개수의 점수의 평균을 반환
  def average_note_count(self):
    self.note_count_databox = note_count_score(self.mydata[self.data_name])
    for key, item in self.note_count_databox.items():
      self.note_count_databox[key] = sum(item) / len(item)
  # 기본으로 초기 확률과 가중 확률을 합친다.
  def sum_weight_databox(self):
    for key, item in self.note_count_databox.items():
      # print(self.note_count_weight)
      # print(key)
      # print(item)
      self.note_count_weight[key] += item
    # print(self.note_count_weight)
  def reflect_weight(self):
    mydata = note_count_score(self.mydata[self.data_name])
    # print(mydata)
    self.note_count_weight = data_analyzer.reflect_neighbor_probability(self.note_count_weight, mydata)
if __name__ == "__main__":
  test = ChordDataAnalyzer()
  test.reflect_weight()
  # print(test.note_count_weight)
