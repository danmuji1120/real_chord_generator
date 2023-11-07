import os
import re
from datetime import datetime
import music21
from PIL import Image
import pygame
import time

CURRENT_PATH = os.path.split(__file__)[0]

NOTE_PITCH = 0
NOTE_POSTION = 1
NOTE_DURATION = 2

ex_data = [    
    ["C3", 0, 0.5],
    ["E3", 0, 0.5],
    ["G3", 0, 0.5],
    ["G4", 1, 1],
    ["G2", 1.5, 0.5],
    ["D4", 2, 0.5],
    ["E4", 3, 0.5],
    ["E4", 1, 1],
    ["rest", 2.5, 0.5]
]

# 해당 경로에 폴더가 없는 겨우 생성
def folder_generator(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

#현재 시간을 반환
def current_time():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    return timestamp

# 출력 경로, bpm, 데이터를 입력 받아 미디 파일로 출력
def crete_midi(midi_path: str, bpm=120, data=ex_data):
    start_time = time.time()

    # print('[sui]: MIDI파일 생성 시작')
    if re.search(r'\.mid$', midi_path):
        # .mid로 끝나면 그대로 저장
        pass
    else:
        # .mid로 끝나지 않으면 끝에 .mid를 붙여서 저장
        midi_path = f'{midi_path}.mid'
    

    # 3. 객체들을 Part 객체에 추가
    score = music21.stream.Score()
    part = music21.stream.Part()
    measure1 = music21.stream.Measure()
    # 2. 음표, 쉼표, 리듬 등의 정보를 담은 객체 생성
    for i in data:
        if i[NOTE_PITCH] == 'rest':
            rest = music21.note.Rest(quarterLength=i[NOTE_DURATION])
            measure1.insert(i[NOTE_POSTION], rest)
        else:
            if 's' in i[NOTE_PITCH]:
                i[NOTE_PITCH] = i[NOTE_PITCH].replace('s', '#')
            # print(f'i[NOTE_PITCH]: {i[NOTE_PITCH]}, i[NOTE_DURATION]: {i[NOTE_DURATION]}')
            current_note = music21.note.Note(i[NOTE_PITCH], quarterLength=i[NOTE_DURATION])
            measure1.insert(i[NOTE_POSTION], current_note)
            # print(f'음높이: {i[NOTE_PITCH]}, 음 위치: {i[NOTE_POSTION]}')

    # 4. Part 객체들을 Score 객체에 추가
    part.insert(0, measure1)
    score.insert(0, part)
    # 5. Tempo 설정
    mm = music21.tempo.MetronomeMark(number=bpm)
    score.insert(0, mm)

    # 6. Score 객체를 미디 파일로 저장
    mf = music21.midi.translate.streamToMidiFile(score)
    mf.open(midi_path, 'wb')
    mf.write()
    mf.close()
    # print('[sui]: MIDI파일 생성 완료')

    end_time = time.time()

    execution_time = end_time - start_time
    # print(f"함수 실행 시간: {execution_time}초")

# 미디 파일 경로, 출력 경로를 입력 받아 악보로 출력
def sheet_generator(sheet_path, midi_path):
    start_time = time.time()

    # print('[sui]: 악보 생성중')
    if re.search(r'\.mid$', midi_path):
        # .mid로 끝나면 그대로 저장
        pass
    else:
        # .mid로 끝나지 않으면 끝에 .mid를 붙여서 저장
        midi_path = f'{midi_path}.mid'

    # MIDI 파일 로드
    score = music21.converter.parse(midi_path)

    

    # 높은음자리표 Part 객체 생성
    part_high = music21.stream.Part()
    part_high.insert(0, music21.instrument.Piano())
    part_high.insert(0, music21.clef.TrebleClef())

    # 낮은음자리표 Part 객체 생성
    part_low = music21.stream.Part()
    part_low.insert(0, music21.instrument.Piano())
    part_low.insert(0, music21.clef.BassClef())

    # 높은음자리표와 낮은음자리표에 각각의 음표 추가
    pre_high_note_duration = 0
    pre_high_note_position = 0
    pre_low_note_duration = 0
    pre_low_note_position = 0
    for note in score.flat.notes:
        # print(note.duration.quarterLength)
        if note.pitches[0].midi < 60:
            # 반대쪽 음자리표에 쉽표 생성
            rest1 = music21.note.Rest()
            rest_duration = note.offset - pre_low_note_duration - pre_low_note_position
            if rest_duration != 0:
                rest1.quarterLength = rest_duration
                part_low.append(rest1)
            pre_low_note_duration = note.duration.quarterLength
            pre_low_note_position = note.offset
            part_low.append(note)
        else:
            rest1 = music21.note.Rest()
            rest_duration = note.offset - pre_high_note_duration - pre_high_note_position
            if rest_duration != 0:
                rest1.quarterLength = rest_duration
                part_high.append(rest1)
            pre_high_note_duration = note.duration.quarterLength
            pre_high_note_position = note.offset
            part_high.append(note)

    # 높은음자리표와 낮은음자리표를 포함한 Score 객체 생성
    score_with_clefs = music21.stream.Score()
    score_with_clefs.insert(0, part_high)
    score_with_clefs.insert(0, part_low)



    # 악보 이미지 생성
    path = f'{sheet_path}.png'
    score_with_clefs.write('musicxml.png', fp=path)
    # print('[sui]: 악보 배경 입히는중')
    

    # 이미지의 배경색을 흰색으로 변경
    path = f'{sheet_path}-1.png'
    image = Image.open(path).convert('RGBA')
    data = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if data[x, y][3] == 0:
                data[x, y] = (255, 255, 255, 255)
    image.save(path, 'PNG')
    # print('[sui]: 악보 생성 완료')
    
    end_time = time.time()

    execution_time = end_time - start_time
    # print(f"함수 실행 시간: {execution_time}초")
    

# 미디 파일 경로를 입력 받아 소리로 출력
def play_midi(midi_file_path):
    """
    pygame을 사용하여 MIDI 파일을 재생하는 함수입니다.
    :param midi_file_path: 재생할 MIDI 파일 경로
    """
    if re.search(r'\.mid$', midi_file_path):
        # .mid로 끝나면 그대로 저장
        pass
    else:
        # .mid로 끝나지 않으면 끝에 .mid를 붙여서 저장
        midi_file_path = f'{midi_file_path}.mid'
    pygame.init()
    pygame.mixer.music.load(midi_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
      # print('대기중')
      pygame.time.wait(1000)
    #pygame.mixer.music.load('test6.mid')
    pygame.mixer.music.stop()
    pygame.quit()

test_path = os.path.join(CURRENT_PATH, "test9")

# crete_midi(midi_path=test_path)
# sheet_generator(midi_path=test_path, sheet_path=test_path)