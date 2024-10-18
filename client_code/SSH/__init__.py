from ._anvil_designer import SSHTemplate
from anvil import *
import anvil.server
from ..devices_filter import FilterFactory
from anvil_extras.utils import auto_refreshing


all_inventory = anvil.server.call("inventory_from_database")
FilterFactory.set_shared_list(all_inventory)


@auto_refreshing
class SSH(SSHTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.types = FilterFactory.available_options(3)
    self.vendors = FilterFactory.available_options(4)
    self.groups = FilterFactory.available_options(10)
    self.sites = []
    
    
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def group_multidropdown_change(self, **event_args):
    """This method is called when the selected values change"""
    for g in self.group_multidropdown.selected:
      print(g)
      FilterFactory.apply_filter(filter_index =10, filter_value=g)
    print(FilterFactory.available_options(4))

      
    # self.types = FilterFactory.available_options(3)
    # self.vendors = FilterFactory.available_options(4)
    # self.groups = FilterFactory.available_options(10)
    # print(self.vendors)
    
      # self.sites = FilterFactory.available_options()
    pass
