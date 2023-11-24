RC = 8 # 주변의 데이터를 얼마나 반영할지 결정. 수가 작아 질수록 반영이 커짐
DP = 2 # decimal point
RA = 2 # 반영범위
DA = 4# 데이터 거리에 따른 반영 계수. 제곱으로 감소
# 기본 데이터와 추가 데이터를 합친다.
def sum_data(default_data, add_data):
    data = {}
    for key, item in default_data.items():
        data[key] = [item]
    for key, items in add_data.items():
        for item in items:
            data[key].append(item)
    return data
# 데이터들의 평균을 계산한다.
def data_average(data):
    result = {}
    for key, items in data.items():
        result[key] = round(sum(items)/len(items), 2)
    return result
# 주변 데이터를 반영한 데이터를 출력
def data_reflect(data: dict):
    data_keys = list(data.keys())
    data_items = list(data.values())
    result = {}
    num = 0
    for i in range(0, len(data_items)):
        data_sum = 0
        for j in range(i-RA, i+RA+1):
            if j >= 0 and j < len(data):
                if data_items[i] <= data_items[j]:
                    data_sum += data_items[j]/(DA**abs(j - i))
                else:
                    data_sum -= data_items[j]/(DA**abs(j - i))
        result[data_keys[num]] = round(data_sum, 2)
        num += 1
    return result
def reflect_neighbor_probability(default_data, add_data):
    result = {}
    mydata = sum_data(default_data, add_data)
    mydata_average = data_average(mydata)
    mydata_reflect = data_reflect(mydata_average)
    for key in mydata.keys():
      result[key] = round(mydata_average[key] + (mydata_reflect[key] - mydata_average[key]) / len(mydata[key]), 2)
    return result



if __name__ == "__main__":
  import data_manager
  import os
  CURRENT_PATH = os.path.split(__file__)[0]
  test = data_manager.DataContainer(os.path.join(CURRENT_PATH, "sample", "sample_data.json"), "chord")
  print(test.mydata)