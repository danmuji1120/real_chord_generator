from tkinter.tix import MAX
from data_manager import DataContainer
import random
import datetime
from utils import dchord
import time
from utils import midi_tools
from utils import midi_to_logic

DATA_PATH = "data/data.json"
DATA_NAME = "chord"

MIN_NOTE = 12 # C1
MAX_NOTE = 96 # C8

class ChordDataAnalyzer(DataContainer):
  def __init__(self) -> None:
    super().__init__(DATA_PATH, DATA_NAME)
    
class NoteSelector(ChordDataAnalyzer):
  def __init__(self) -> None:
    super().__init__()
    self.min_note = MIN_NOTE
    self.max_note = MAX_NOTE
    self.note_count = 3
  def select_note(self):
    # print(f"min: {self.min_note}, max: {self.max_note}")
    return random.choice(range(self.min_note, self.max_note + 1))
  def select_note_count(self):
    # self.note_count = random.choice(range(1, 12))
    self.note_count = random.choice(range(1, self.max_note-self.min_note))

class ChordGenerator(NoteSelector):
  def __init__(self) -> None:
    super().__init__()
    self.mychord = []
  def random_chord_generator(self):
    self.mychord = []
    self.min_note = MIN_NOTE
    self.select_note_count()
    print(f"선택된 노트 개수: {self.note_count}")
    while len(self.mychord) < self.note_count and self.min_note < self.max_note:
      selected_note = self.select_note()
      self.mychord.append(selected_note)
      self.min_note = selected_note + 1
  def random_chord_generator2(self):
    self.mychord = []
    self.min_note = MIN_NOTE
    self.select_note_count()
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
    self.start()
  def start(self):
    break_toggle = True
    while break_toggle:
      print("--작업--\n1. 코드생성\n2. 종료")
      answer = input("입력:")
      line_clear()
      if answer == "1":
        while break_toggle:
          self.chord()
          self.temporary_save()
          while True:
            line_clear()
            answer = input("--입력--\n 숫자: 점수 저장\n r: 다시 듣기\n x: 종료\n입력: ")
            if answer == "r":
              midi_to_logic.playlogic(self.temporary_name+".mid")
            elif answer == "x":
              break_toggle = False
              break
            else:
              try:
                answer = int(answer)
                if answer >= 0 and answer <= 100:
                  self.save_chord(answer)
                  line_clear()
                  break
              except:
                print("잘못된 입력")
                time.sleep(1)
                line_clear()
                print(self.render_chord())
              

      elif answer == "2":
        print("프로그램을 종료합니다")
        break
      else:
        print("잘못된 입력")
        time.sleep(1)
        line_clear()
  def chord(self):
    self.random_chord_generator2()
    print(self.render_chord())

  def temporary_save(self):
    self.render_midi()
    midi_tools.crete_midi(self.temporary_name, data=self.midi_data)
    midi_tools.sheet_generator(self.temporary_name, self.temporary_name+".mid")
    midi_to_logic.playlogic(self.temporary_name+".mid")
    

if __name__ == "__main__":
  test = ChordMain()