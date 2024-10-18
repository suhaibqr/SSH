from ._anvil_designer import SSHTemplate
from anvil import *
import anvil.server
from ..devices_filter import FilterFactory
from anvil_extras.utils import auto_refreshing






@auto_refreshing
class SSH(SSHTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    all_inventory = anvil.server.call("inventory_from_database")
    self.filter_factory = FilterFactory(all_inventory)
    self.types = self.filter_factory.get_available_values(3)
    self.vendors = self.filter_factory.get_available_values(4)
    self.groups = self.filter_factory.get_available_values(10)
    # self.sites = []
    
    
    self.init_components(**properties)

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
    self.refresh_data_bindings()
    # self.sites = self.filter_factory.get_available_values(x)
    return 

  def RESET_FILTER_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.groups_multidropdown.selected = []
    self.types_multidropdown.selected = []
    self.vendors_multidropdown.selected = []
    self.filter_factory.filtered_list = self.filter_factory.all_lists
    self.types = self.filter_factory.get_available_values(3)
    self.vendors = self.filter_factory.get_available_values(4)
    self.groups = self.filter_factory.get_available_values(10)
    self.refresh_data_bindings()
    # self.sites = self.filter_factory.get_available_values(x)
    pass

