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
    self.note_weight = {}
    self.note_interval_weight = {}
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
      self.note_count_weight[key] += item
  def reflect_weight(self):
    mydata = note_count_score(self.mydata[self.data_name])
    # print(mydata)
    self.note_count_weight = data_analyzer.reflect_neighbor_probability(self.note_count_weight, mydata)
  # 범위 안의 노트 기본 확룰 생성
  def default_note_weight(self):
    for i in range(self.min_note, self.max_note + 1):
      self.note_weight[i] = 50
    # print(self.note_weight)
  # 루드 노트에 대한 확룰를 적용
  def return_root_note_weight(self):
    self.default_note_weight()
    self.note_weight = data_analyzer.reflect_neighbor_probability(self.note_weight, self.root_note_score())
  # 루트 노트에 대한 모든 점수를 반환
  def root_note_score(self):
    root_note_data = {}
    for note_and_score in self.mydata[self.data_name].values():
      notes = note_and_score[0]
      notes.sort()
      root_note = notes[0]
      score = note_and_score[1]
      if root_note in root_note_data.keys():
        root_note_data[root_note].append(score)
      else:
        root_note_data[root_note] = [score]
    root_note_data = dict(sorted(root_note_data.items()))
    return root_note_data
  
  # 노트 간격에 따른 확률 반환
  def return_note_interval_weight(self):
    pass

  # 노트 간격에 대한 점수를 반환
  def note_inteval_score(self):
    note_interval_data = {}
    for notes_and_score in self.mydata[self.data_name].values():
      notes = notes_and_score[0]
      score = notes_and_score[1]
      notes.sort()
      if score > 0:
        for i in range(0, len(notes)-1):
          interval = notes[i+1] - notes[i]
          if interval in note_interval_data:
            note_interval_data[interval].append(score)
          else:
            note_interval_data[interval] = [score]
    note_interval_data = dict(sorted(note_interval_data.items()))
    for i in note_interval_data.keys():
      print(i, ": ", note_interval_data[i])

if __name__ == "__main__":
  test = ChordDataAnalyzer()
  test.reflect_weight()
  test.root_note_score()
  print(test.note_count_weight)
  import matplotlib.pyplot as plt
  data = test.root_note_score()
  sub_data = {}
  for i, j in data.items():
    sub_data[i] = round(sum(j)/len(j), 2)
  test.return_root_note_weight()
  plt.plot(sub_data.keys(), sub_data.values(), test.note_weight.keys(), test.note_weight.values())
  plt.show()
  test.note_inteval_score()
