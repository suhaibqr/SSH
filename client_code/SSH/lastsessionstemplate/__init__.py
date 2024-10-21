from ._anvil_designer import lastsessionstemplateTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ...devices_filter import check_if_pmp, wssh_connect, manual_connect
from .. import all_inventory
import re

class lastsessionstemplate(lastsessionstemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
   
    self.init_components(**properties)
    self.add_component(self.create_last_session_button(self.item))


  def create_last_session_button(self, h):
   
    v = re.search(r"'(.*?)'", h).group(1)
  
    s_button = anvil.Button(text=str(v), role="raised", icon=None)
    s_button.tag.pmp = 1
    s_button.background = "#28a745"
    pmp = check_if_pmp(all_inventory,v)
    if pmp:
      s_button.tag.pmp = True  
      s_button.background = "#909845"
      s_button.tag.hostname = v
      s_button.set_event_handler('click',wssh_connect )
    else:
      s_button.tag.pmp = False
    return s_button




    # Any code you write here will run before the form opens.
