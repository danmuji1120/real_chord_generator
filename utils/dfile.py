import json
import os
import datetime

def today():
  x = datetime.datetime.now()
  return f"{x.year}-{x.month}-{x.day}"

def isfile(path: str):
  '''해당 경로에 폴더/파일이 존재하는지 확인'''
  if os.path.exists(path):
    return True
  else:
    return False

# 폴더 추가
def add_folder(path: str):
  os.mkdir(path)

# 해당 폴더가 존재하는지 확인하고 없다면 생성
def check_folder(path: str):
  if os.path.exists(path):
    print("이미 존재하는 폴더")
  else:
    print("존재하지 않는 폴더")
    add_folder(path)
    print(f"{path} 폴더 생성")

# json 파일로 로드
def load_json_file(path):
  # 경로가 .json으로 끝나지 않는 경우 예외 처리
  if not path.endswith('.json'):
    print("존재하지 않는 경로")
    return None
  
  # 경로에 JSON 파일이 존재하는지 확인
  if os.path.exists(path):
    # JSON 파일이 존재하면 파일 내용을 불러옴
    with open(path, 'r', encoding="utf8") as file:
      data = json.load(file)
      print(f"json파일을 로드하는데 성공: {path}")
      return data
  else:
    print(f"No JSON file found at {path}")
    return None

# json 파일을 저장
def save_json_file(path, data):
  # 경로가 .json으로 끝나지 않거나 데이터가 딕셔너리 형태가 아닌 경우 저장하지 않음
  if not path.endswith('.json') or not isinstance(data, dict):
    print("경로가 잘못되었거나 데이터의 타입이 올바르지 않습니다")
    return
  # 데이터를 JSON 파일로 저장
  with open(path, 'w', encoding="utf8") as file:
    json.dump(data, file, indent=1)
    # print(f"파일을 올바르게 저장: {path}")


if __name__ == "__main__":
  pass