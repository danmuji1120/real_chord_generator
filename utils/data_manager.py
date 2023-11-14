from .dfile import *
import os

class DataContainer():
  def __init__(self, data_path, data_name) -> None:
    self.data_path = data_path
    self.data_name = data_name
    self.mydata = {}
    self.check_data()
    self.backup()
  def check_data(self):
    path_list = self.data_path.split("/")
    path = ""
    for path_element in path_list[:-1]:
      path += path_element
      if isfile(path):
        pass
      else:
        add_folder(path)
      path += "/"
    if isfile(self.data_path):
      self.mydata = load_json_file(self.data_path)
    else:
      save_json_file(path=self.data_path, data={self.data_name: {}})
    if not isfile("backup"):
      add_folder("backup")
      
  def update_data(self, data_key, data_value):
    mydata = load_json_file(self.data_path)
    mydata[self.data_name][data_key] = data_value
    save_json_file(self.data_path, mydata)
  def remove_data(self, data_key):
    mydata = load_json_file(self.data_path)
    del mydata[self.data_name][data_key]
    save_json_file(self.data_path, mydata)
  def backup(self):
    backup_files = os.path.basename("backup")
    toggle = True
    for backup_file in backup_files:
      if today == backup_file.split("_")[0]:
        toggle = False
    if toggle:
      mydata = load_json_file(self.data_path)
      save_json_file("backup/"+today()+"_"+self.data_name+".json", mydata)


