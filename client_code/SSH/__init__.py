from ._anvil_designer import SSHTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..devices_filter import FilterFactory, list_of_lists_to_dicts,filter_list_of_lists_by_strings, check_if_pmp, wssh_url
from anvil_extras.utils import auto_refreshing
import anvil.users
import anvil.js.window
import base64




def error_handler(err):
  n = Notification("Slow Down", title="Slow Down", timeout=2)
  n.show()
    

set_default_error_handling(error_handler)

all_inventory = anvil.server.call("inventory_from_database")
filter_factory = FilterFactory(all_inventory)


class SSH(SSHTemplate):
  def __init__(self, **properties):
    u , ip = anvil.server.call("get_cookies")
    if u != "Not Found" and u:
      anvil.server.call("anvil_force_auth", u)
      print("Cookies are:", u, ip)
    else:
      print("No Auth Cookies")
    
    
    # Set Form properties and Data Bindings.
    self.u_last_sessions = []
    self.ssh_manual_address_txt = "Address"
    # self.ssh_manual_password_txt = "Password"
    self.ssh_manual_username_txt = "Username"
    self.ssh_manual_port_txt = 22





    self.types, self.vendors, self.groups = filter_factory.get_available_values_for_indexes([3,4,10])
    # self.types = filter_factory.get_available_values(3)
    # self.vendors = filter_factory.get_available_values(4)
    # self.groups = filter_factory.get_available_values(10)



    
    self.keys = ["hostname", "address", "customer", "type","account_list"]
    self.indexes_of_interest = [0,2,10,3,11]
    self.devices_table = list_of_lists_to_dicts(self.keys,filter_factory.filtered_list,self.indexes_of_interest)
    
    
  
    self.init_components(**properties)

    # self.saml_user ="suhaib.alrabee@example.com"
    # anvil.server.call("anvil_force_auth", self.saml_user)
    self.u = anvil.users.get_user()
    if self.u:
      print(self.u["email"])
      print("Authenticated")
    else:
      print("UnAuthenticated")
    self.devices_repeatingpanel.items = self.devices_table
    self.paint_last_cli_connections(self.u)
    self.color_rows(self.devices_repeatingpanel)
    # self.refresh_data_bindings()
    # Any code you write here will run before the form opens.

      # self.sites = FilterFactory.available_options()
    pass

  def filter_dropdown(self):
    g = self.groups_multidropdown.selected
    t = self.types_multidropdown.selected
    v = self.vendors_multidropdown.selected
   
    self.types, self.vendors , self.groups = filter_factory.filter_and_get_available_values([{3:t}, {4:v}, {10:g}])
     
    # filter_factory.filter_list([{3:t}, {4:v}, {10:g}])
    # self.types = filter_factory.get_available_values(3)
    # self.vendors = filter_factory.get_available_values(4)
    # self.groups = filter_factory.get_available_values(10)
    
    if self.devices_table_search_text.text != "":
      filter_factory.filtered_list = filter_list_of_lists_by_strings(filter_factory.filtered_list, self.devices_table_search_text.text)
    self.devices_table = list_of_lists_to_dicts(self.keys,filter_factory.filtered_list,self.indexes_of_interest)
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)
 

  def RESET_FILTER_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.groups_multidropdown.selected = []
    self.types_multidropdown.selected = []
    self.vendors_multidropdown.selected = []
    self.devices_table_search_text.text = ""
    filter_factory.filtered_list = filter_factory.all_lists
    self.types = filter_factory.get_available_values(3)
    self.vendors = filter_factory.get_available_values(4)
    self.groups = filter_factory.get_available_values(10)
    self.devices_table = list_of_lists_to_dicts(self.keys,filter_factory.filtered_list,self.indexes_of_interest)
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)
    self.manual_hostname_label.text = ""
    

  def devices_table_search_text_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    
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

      for s in cli_session:
        self.u_last_sessions.append(s["host"])
        
     
      self.last_seessions_rep.items = self.u_last_sessions
      
    
        

  def active_sessions_btn_click(self, **event_args):
    ss = eval(anvil.server.call("get_current_active_sessions"))
    self.all_current_sessions = "Active Sessions:\n"
    for s in ss:
      u = s[0].split("@")[0]
      self.all_current_sessions = self.all_current_sessions + f"{u}:{s[2][0]}\n" 
    alert(content=self.all_current_sessions,
               title="Current Active Sessions",
               large=True,
               buttons=[
                 ("Fine", None)
               ],
             dismissible  = True,
             )
    pass



  def session_recordings_btn_click(self, **event_args):
    # with Notification("Loading", title="Getting Your Logs", timeout=10):
    file_names = anvil.server.call("get_sorted_filenames_by_time", self.u["email"])
    file_names.reverse()
    cp = ColumnPanel()
    for l in file_names:
      newlink = Link(text=l)
      newlink.set_event_handler('click', self.download_by_file_name)
      newlink.tag.name = l
      cp.add_component(newlink)

    
    alert(content=cp,title="Session Files", buttons=[("Fine", None)], large=True,dismissible=True)
    # file_media = anvil.server.call('get_file')



  def download_by_file_name(self, **args):
    print(args["sender"].tag, dir(args["sender"].tag))
    m = anvil.server.call("find_log_and_read_file", args["sender"].tag.name)
    print(args["sender"].tag.name)
    if m:
            # Trigger the download
            anvil.media.download(m)


    # def get_session_info(self):
    #   s = f'''
    #   Hello {self.u["email"]}
    #   Connected from: {anvil.server.call("get_ip")}
    #   Front API Server: {is_anvil_api()}
    #   Backend API Server": {is_api()}
    #   '''
  
  def ssh_btn_clicked(self, **args):
    print(args["sender"].tag.hostname)
    print(args["sender"].tag.pmp)
    pass



  def multidropdown_change(self, **event_args):
    
    self.filter_dropdown()
    pass




  def Authenticate_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.js.window.open(f"{wssh_url}/login/saml", "_blank")
    pass

  def manual_connect_btn_click(self, **event_args):
    byte_string = self.ssh_manual_password.text.encode('utf-8')


    base64_encoded = base64.b64encode(byte_string)
    base64_encoded_string = base64_encoded.decode('utf-8')
    url = f"{wssh_url}?hostname={self.ssh_manual_address.text}&username={self.ssh_manual_username.text}&password={base64_encoded_string}"
    anvil.js.window.open(url, "_blank")
    
   



