from ._anvil_designer import devicerowtemplateTemplate
from anvil import *
import anvil.server


class devicerowtemplate(devicerowtemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.item["hostname"] = item[]
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
