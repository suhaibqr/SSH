from ._anvil_designer import SSHTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..devices_filter import FilterFactory, list_of_lists_to_dicts,filter_list_of_lists_by_strings
from anvil_extras.utils import auto_refreshing
import anvil.users






class SSH(SSHTemplate):
  def __init__(self, **properties):
    
    # Set Form properties and Data Bindings.
    
    all_inventory = anvil.server.call("inventory_from_database")
    self.filter_factory = FilterFactory(all_inventory)
    self.types = self.filter_factory.get_available_values(3)
    self.vendors = self.filter_factory.get_available_values(4)
    self.groups = self.filter_factory.get_available_values(10)
    self.keys = ["hostname", "address", "customer", "type","account_list"]
    self.indexes_of_interest = [0,2,10,3,11]
    self.devices_table = list_of_lists_to_dicts(self.keys,self.filter_factory.filtered_list,self.indexes_of_interest)
    # self.get_last_cli_connections()
    # self.last_seessions = get_last_cli_connections(")
    # list_of_lists_to_dicts
    # self.sites = []
    
    
    self.init_components(**properties)
    # anvil.users.login_with_form()
    # anvil.users.login_with_form()
    self.saml_user ="suhaib.alrabee@example.com"
    anvil.server.call("anvil_force_auth", self.saml_user)
    self.u = anvil.users.get_user()
    if self.u:
      print(self.u["email"])
      print("Authenticated")
    else:
      print("UnAuthenticated")

    self.paint_last_cli_connections(self.u)


    

    self.color_rows(self.devices_repeatingpanel)
    # Any code you write here will run before the form opens.

  def multidropdown_change(self, **event_args):
    """This method is called when the selected values change"""
    self.filter_dropdown()

    # for g in self.group_multidropdown.selected:
    #   self.filter_factory.filter_by_index(10, g)

    
    # print(self.filter_factory.available_values_at_index(4))

    
      # self.sites = FilterFactory.available_options()
    pass

  def filter_dropdown(self):
    g = self.groups_multidropdown.selected
    t = self.types_multidropdown.selected
    v = self.vendors_multidropdown.selected
    # s = self.sites_multidropdownmulti.selected
    self.filter_factory.filter_list([{3:t}, {4:v}, {10:g}])
    self.types = self.filter_factory.get_available_values(3)
    self.vendors = self.filter_factory.get_available_values(4)
    self.groups = self.filter_factory.get_available_values(10)
    if self.devices_table_search_text.text != "":
      # print(self.devices_table_search_text.text)
      self.filter_factory.filtered_list = filter_list_of_lists_by_strings(self.filter_factory.filtered_list, self.devices_table_search_text.text)
    self.devices_table = list_of_lists_to_dicts(self.keys,self.filter_factory.filtered_list,self.indexes_of_interest)
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)
    # self.sites = self.filter_factory.get_available_values(x)
    return 

  def RESET_FILTER_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.groups_multidropdown.selected = []
    self.types_multidropdown.selected = []
    self.vendors_multidropdown.selected = []
    self.devices_table_search_text.text = ""
    self.filter_factory.filtered_list = self.filter_factory.all_lists
    self.types = self.filter_factory.get_available_values(3)
    self.vendors = self.filter_factory.get_available_values(4)
    self.groups = self.filter_factory.get_available_values(10)
    self.devices_table = list_of_lists_to_dicts(self.keys,self.filter_factory.filtered_list,self.indexes_of_interest)
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)
    # self.sites = self.filter_factory.get_available_values(x)
    pass

  def devices_table_search_text_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    # print(self.devices_table_search_text.text)
    self.filter_dropdown()
    pass



  def color_rows(self, rep):
    for i, r in enumerate(rep.get_components()):
      if not i%2:
        r.background='#e0f7fa'
      else:
        r.background = '#ffffff'

  def paint_last_cli_connections(self, u):
    if u:
      print(u["email"])
      cli_session = anvil.server.call("get_last_cli_connections", u["email"])
      print(cli_session)
      for s in cli_session:
        print(s)
      
      # self.last_seessions_rep.items = self.__init__()
      self.last_seessions_rep.visible = True