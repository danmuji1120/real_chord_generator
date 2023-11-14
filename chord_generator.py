from tkinter.tix import MAX
import random
import datetime
from utils import dchord
import time
from utils import midi_tools
from utils import midi_to_logic
from chord_data_analyzer import ChordDataAnalyzer

class NoteSelector(ChordDataAnalyzer):
  def __init__(self) -> None:
    super().__init__()
    self.note_count = 3
  def select_note(self):
    # print(f"min: {self.min_note}, max: {self.max_note}")
    return random.choice(range(self.min_note, self.max_note + 1))
  def select_note_count(self):
    # self.note_count = random.choice(range(1, 12))
    self.note_count = random.choice(range(1, self.max_note-self.min_note))
  # 정해진 확률로 노트 개수를 선택
  def select_note_count_weight(self):
    key = list(self.note_count_weight.keys())
    item = list(self.note_count_weight.values())
    # print(key)
    # print(item)
    self.note_count = random.choices(key, item)[0]
    # print("asfadsf: ", self.note_count)

class ChordGenerator(NoteSelector):
  def __init__(self) -> None:
    super().__init__()
    self.mychord = []
  def random_chord_generator(self):
    self.mychord = []
    self.pre_note = self.min_note
    self.select_note_count()
    print(f"선택된 노트 개수: {self.note_count}")
    while len(self.mychord) < self.note_count and self.pre_note < self.max_note:
      selected_note = self.select_note()
      self.mychord.append(selected_note)
      self.pre_note = selected_note + 1
  def stack_chord_generator(self):
    self.mychord = []
    self.pre_note = self.min_note
    self.average_note_count()
    self.sum_weight_databox()
    self.select_note_count_weight()
    while len(self.mychord) <= self.note_count:
      selected_note = self.select_note()
      if not selected_note in self.mychord:
        self.mychord.append(selected_note)
  def reflect_stack_generator(self):
    self.mychord = []
    self.pre_note = self.min_note
    self.reflect_weight()
    self.select_note_count_weight()
    while len(self.mychord) <= self.note_count:
      selected_note = self.select_note()
      if not selected_note in self.mychord:
        self.mychord.append(selected_note)

  def render_midi(self):
    self.midi_data = []
    for note in self.mychord:
      self.midi_data.append([dchord.num_to_note(note), 0, 4])
  def render_chord(self):
    display_chord = []
    for note in self.mychord:
      display_chord.append(dchord.num_to_note(note))
    return display_chord

  def save_chord(self, score):
    x = datetime.datetime.now()
    key = f"{x.year}-{x.month}-{x.day}-{x.hour}-{x.minute}-{x.second}"
    self.update_data(key, [self.mychord, score])

def line_clear():
  for i in range(30):
    print()

class ChordMain(ChordGenerator):
  def __init__(self) -> None:
    super().__init__()
    self.temporary_name = "current"
    self.break_toggle = True
  
  def start(self):
    while True:
      line_clear()
      print("--작업--\n1. 코드생성\n2.설정\nx. 종료")
      answer = input("입력:")
      line_clear()
      if answer == "1":
        self.chord_menu()
      elif answer == "2":
        self.setting_menu()
      elif answer == "x":
        break
      else:
        self.start()
  def chord_menu(self):
    print("--선택--\n1. 완전랜덤\n2. 노트 개수 반영\n3. 인접 확률 반영\nx. 뒤로가기")
    answer = input("입력: ")
    while self.break_toggle:
      if answer == "1":
        self.random_chord_generator()
      elif answer == "2":
        self.stack_chord_generator()
      elif answer == "3":
        self.reflect_stack_generator()
      elif answer == "x":
        break
      self.temporary_save()
      print(self.mychord)
      self.input_score()
  def setting_menu(self):
    pass

  def input_score(self):
    midi_to_logic.playlogic(self.temporary_name+".mid")
    line_clear()
    # midi_tools.sheet_generator(self.temporary_name, self.temporary_name+".mid")
    print(self.note_count_weight)
    print("--선택--\n0~100: 점수 저장\nr: 다시듣기\nx: 뒤로가기")
    answer = input("입력: ")
    line_clear()
    if answer == "r":
      self.input_score()
    elif answer == "x":
      self.break_toggle = False
    else:
      try:
        score = int(answer)
        if score >= 0 and score <= 100:
          self.save_chord(score)
      except:
        print("잘못된 입력")
        self.input_score()

    


  def temporary_save(self):
    self.render_midi()
    midi_tools.crete_midi(self.temporary_name, data=self.midi_data)
    

if __name__ == "__main__":
  test = ChordMain()
  test.start()