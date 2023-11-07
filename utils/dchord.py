import re

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# 노트와 옥타브를 분리
def split_note_and_octave(note_octave):
  p_note = re.compile('[A-Z]#?')
  p_octave = re.compile('\d+')
  note = p_note.findall(note_octave)[0]
  octave = p_octave.findall(note_octave)[0]
  return [note, octave]
# 노트를 숫자로 변환
def note_to_num(input_note: str):
  note, octave = split_note_and_octave(input_note)
  note_index = NOTES.index(note)
  return note_index + (int(octave) * 12)
# 숫자를 노트로 변환
def num_to_note(num: int):
  '''숫자를 입력하면 노트로 변환합니다.
  \n숫자는 0의 C0노트부터 시작합니다.
  '''
  note = NOTES[num % 12]
  octave = num // 12
  return note+str(octave)
