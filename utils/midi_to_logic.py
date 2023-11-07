import mido
import os

CURRENT_PATH = os.path.split(__file__)[0]


# MIDI 파일 경로
# midi_file_path = os.path.join(CURRENT_PATH, "test9.mid")
# MIDI 파일 파싱
# midi_file = mido.MidiFile(midi_file_path)

def playlogic(midi_path:str):
    # Logic Pro X의 MIDI 출력 포트 이름을 확인하고 설정합니다.
    midi_file = mido.MidiFile(midi_path)
    output_ports = mido.get_output_names()
    # print(output_ports)

    # Check if the Logic Pro X port is found
    # if midi_out_port is None:
        # raise ValueError("Logic Pro X port not found. Please check your MIDI setup.")

    # MIDI 이벤트를 라이브로 보냅니다.
    try:
        midi_out_port = output_ports[0]

        with mido.open_output(midi_out_port) as port:
            for msg in midi_file.play():
                port.send(msg)
    except:
        print('logic pro를 찾지 못함. 재생 불가능')

# playlogic('/Users/y-danmuji/Documents/code/python/soundAI/midi/20230723_125548173.mid')