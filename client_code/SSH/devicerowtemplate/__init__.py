from ._anvil_designer import devicerowtemplateTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


class devicerowtemplate(devicerowtemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)
    # print(self.get_components())
    self.tasks_flow_panel.clear()
    self.initialize_task_buttons()
   
    # 

    # Any code you write here will run before the form opens.


  def initialize_task_buttons(self):
    self.create_cli_button()
    self.create_gui_login()
  
  def create_cli_button(self):
    is_pmp = self.item.get('account_list', None)
    if is_pmp:
      cli_button = anvil.Button(text=str("AutoLogin"), role="raised", icon=None)
      cli_button.tag.pmp = 1
      cli_button.background = "#28a745"
      self.tasks_flow_panel.add_component(cli_button)
    else:
      cli_button = anvil.Button(text=str("ManualLogin"), role="raised", icon=None)
      cli_button.tag.pmp = 0
      self.tasks_flow_panel.add_component(cli_button)
  
  def create_gui_login(self):
    is_gui = self.item.get('type', None)
    if is_gui == "GUI":
      gui_button = anvil.Button(text=str("GUI"), role="raised", icon=None)
      gui_button.tag.pmp = 1
      gui_button.background = "#28a745"
      self.tasks_flow_panel.add_component(gui_button)
      
      gui_credentials_button = anvil.Button(text=str("Credentials"), role="raised", icon=None)
      gui_credentials_button.tag.pmp = 1
      gui_credentials_button.background = "#28a745"
      self.tasks_flow_panel.add_component(gui_credentials_button)
      
      
      
      