from ._anvil_designer import devicerowtemplateTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ...devices_filter import wssh_connect, manual_connect , device_table_test_connection





class devicerowtemplate(devicerowtemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.tasks_flow_panel.clear()
    self.init_components(**properties)
    # print(self.get_components())
   
    self.initialize_task_buttons()
    
   
    # 

    # Any code you write here will run before the form opens.


  def initialize_task_buttons(self):
    self.create_cli_button()
    self.create_gui_login()
    self.create_test_btn()
    
  def create_cli_button(self):
    is_pmp = self.item.get('account_list', None)
    if is_pmp:
      cli_button = anvil.Button(text=str("AutoLogin"), role="raised", icon=None)
      cli_button.tag.pmp = True
      cli_button.background = "#28a745"
      cli_button.tag.hostname = self.item["hostname"]
      cli_button.tag.address = self.item["address"]
      cli_button.set_event_handler('click',wssh_connect )
      self.tasks_flow_panel.add_component(cli_button)
    else:
      cli_button = anvil.Button(text=str("ManualLogin"), role="raised", icon=None)
      cli_button.tag.hostname = self.item["hostname"]
      cli_button.tag.address = self.item["address"]
      cli_button.tag.pmp = False
    
      cli_button.set_event_handler('click', manual_connect)
      self.tasks_flow_panel.add_component(cli_button)
  
  def create_gui_login(self):
    is_gui = self.item.get('type', None)
    if is_gui == "GUI":
      gui_button = anvil.Button(text=str("GUI"), role="raised", icon=None)
      gui_button.tag.pmp = 1
      gui_button.tag.name = self.item["hostname"]
      gui_button.tag.url = self.item["address"]
      gui_button.background = "#28a745"
      self.tasks_flow_panel.add_component(gui_button)


  def create_test_btn(self):
    test_btn = Button(text=str("Test"), role="raised", icon=None)
    test_btn.tag.hostname = self.item["hostname"]
    test_btn.tag.ip = self.item["address"]
    test_btn.tag.port = 22
    test_btn.background = "#25a945"
    test_btn.set_event_handler('click',device_table_test_connection)
    self.tasks_flow_panel.add_component(test_btn)
      
      