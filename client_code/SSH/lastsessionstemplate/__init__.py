from ._anvil_designer import lastsessionstemplateTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ...devices_filter import check_if_pmp, wssh_connect, manual_connect
import re

class lastsessionstemplate(lastsessionstemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
   
    self.init_components(**properties)
    self.add_component(self.create_last_session_button(self.item))


  def create_last_session_button(self, i):
    
    all_inventory = i["all_inventory"] 
    v = re.search(r"'(.*?)'", i["hostname"]).group(1)
    
    s_button = anvil.Button(text=str(v), role="raised", icon=None)
    ip = ""
    pmp = check_if_pmp(all_inventory,v)
    # print(all_inventory)
    # print(pmp, v)
    if pmp:
      s_button.tag.pmp = True  
      s_button.background = "#909845"
      s_button.tag.hostname = v
      s_button.set_event_handler('click',wssh_connect )
    else:
      s_button.tag.pmp = False
      s_button.tag.hostname = v
      for sublist in all_inventory:
        if sublist[2] == v or sublist[0] == v  :
          ip = sublist[2]
          print("Found", sublist[0], v)
          
      # print(ip)
      s_button.tag.address = ip
      s_button.set_event_handler('click',manual_connect)
      
    return s_button




    # Any code you write here will run before the form opens.
# def get_item(input_value, data):
#     for sublist in data:
#         if sublist[0] == input_value and len(sublist) > 3:
#             return sublist[2]
#     return None