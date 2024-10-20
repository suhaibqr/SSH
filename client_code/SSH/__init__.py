from ._anvil_designer import SSHTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..devices_filter import FilterFactory , list_of_lists_to_dicts,filter_list_of_lists_by_strings, check_if_pmp, wssh_url
from anvil_extras.utils import auto_refreshing
import anvil.users
import anvil.js.window



all_inventory = []

def error_handler(err):
  n = Notification("Please inform Suhaib about this", title="Server issue", timeout=2)
  n.show()
    

set_default_error_handling(error_handler)




class SSH(SSHTemplate):
  global all_inventory
  def __init__(self, **properties):
    
    # Set Form properties and Data Bindings.
    self.rich_session_details = ""
    self.u_last_sessions = []
    self.ssh_manual_address_txt = "Address"
    # self.ssh_manual_password_txt = "Password"
    self.ssh_manual_username_txt = "Username"
    self.ssh_manual_port_txt = 22
    self.cookie_auth = False
    self.keys = ["hostname", "address", "customer", "type","account_list"]
    self.indexes_of_interest = [0,2,10,3,11]
    self.logout_btn.enabled = False
    
    self.devices_table = []
    self.types = []
    self.vendors = []
    self.groups = []


    
    
    self.init_components(**properties)
    
    
    # self.saml_user ="suhaib.alrabee@example.com"
    # anvil.server.call("anvil_force_auth", self.saml_user)

    
    self.devices_repeatingpanel.items = self.devices_table

    is_auth = self.check_auth()
    
    
    # Any code you write here will run before the form opens.

    
    self.update_session_info()
    
    
    
    if is_auth:
      all_inventory = anvil.server.call("inventory_from_database")
      self.filter_factory = FilterFactory(all_inventory)
      all_inventory = self.filter_factory.all_lists
      self.devices_table = list_of_lists_to_dicts(self.keys,self.filter_factory.filtered_list,self.indexes_of_interest)
      self.types, self.vendors, self.groups = self.filter_factory.get_available_values_for_indexes([3,4,10])
    
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)
    pass

  def filter_dropdown(self):
    g = self.groups_multidropdown.selected
    t = self.types_multidropdown.selected
    v = self.vendors_multidropdown.selected
   
    self.types, self.vendors , self.groups = self.filter_factory.filter_and_get_available_values([{3:t}, {4:v}, {10:g}])
     
    
    if self.devices_table_search_text.text != "":
      self.filter_factory.filtered_list = filter_list_of_lists_by_strings(self.filter_factory.filtered_list, self.devices_table_search_text.text)
    self.devices_table = list_of_lists_to_dicts(self.keys,self.filter_factory.filtered_list,self.indexes_of_interest)

    
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)

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
    
    
    self.manual_hostname_label.text = ""
    self.refresh_data_bindings()
    self.color_rows(self.devices_repeatingpanel)
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
      # print(u["email"])
      cli_session = anvil.server.call("get_last_cli_connections",u)

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
    file_names = anvil.server.call("get_sorted_filenames_by_time", anvil.users.get_user()["email"])
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
    anvil.js.window.open(f"{wssh_url}login/saml", "_blank")
    pass

  def manual_connect_btn_click(self, **event_args):
    byte_string = self.ssh_manual_password.text.encode('utf-8')


    base64_encoded = base64.b64encode(byte_string)
    base64_encoded_string = base64_encoded.decode('utf-8')
    url = f"{wssh_url}?hostname={self.ssh_manual_address.text}&username={self.ssh_manual_username.text}&password={base64_encoded_string}"
    anvil.js.window.open(url, "_blank")

  def test_ping_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    r = anvil.server.call("ping_host", self.test_address_box.text)
    alert(r, title="Ping Result", large=True)
    # print(r)
    # if pingable:
    #   msg = "Reacahble"
    # else:
    #   msgb = "Not Reachable"

  def check_port_status(self, **event_args):
    """This method is called when the button is clicked"""
    r = anvil.server.call("check_port_status", self.test_address_box.text, self.test_port_box.text)
    if r == "open":
      m = "Port is Open" 
    elif r == "closed":
      m = "Port is closed"
    else:
      m = "Port is Not Reachable"
    
    
    alert(m, title="Port Status", large=True)


  def check_auth(self):
    u , ip = anvil.server.call("get_cookies")
    if u != "Not Found" and u:
      anvil.server.call("anvil_force_auth", u)
      print("Cookies are:", u, ip)
      self.cookie_auth = True
      self.logout_btn.enabled = True
      return True
    else:
      self.cookie_auth = False
      print("No Auth Cookies")
      return False

  def update_session_info(self):
    u_cookie , ip = anvil.server.call("get_cookies")
    u = anvil.users.get_user()
    if u:
      u = u["email"]
      auth_status = "True"
    else:
      auth_status = "False"
    # self.rich_session_details = f'''
    # User in Cookies: {u_cookie}
    # User in webserver: {u}
    # IP in Cookies: {ip}
    # Authenticated: {auth_status}
    # '''
    self.rich_session_details = f'''
    Built with <3 by Network Team,
    You can greatly help by providing
    feedbacks, Please, report any issues 
    or ideas to the team.
    Logged in as: {u_cookie}
    Logged in from: {ip}
    '''
    

  def refresh_binding_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_session_info()
    self.refresh_data_bindings()
    pass

  def get_last_session(self, **event_args):
    self.last_seessions_rep.items = []
    self.u_last_sessions = []
    self.paint_last_cli_connections(anvil.users.get_user()["email"])

  def logout_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('clear_cookies')
    anvil.users.logout()
    self.logout_btn.enabled = False
    self.refresh_data_bindings()
    anvil.open_form('SSH')
    pass

  def automater_btn_click(self, **event_args):
    
    """This method is called when the button is clicked"""
    pass

  def NSlookup_click(self, **event_args):
    """This method is called when the button is clicked"""
    r = anvil.server.call("nslookup", self.test_address_box.text,self.test_dns_box.text)
    alert(r, title="Nslookup Result", large=True)
   

 
  
      


def check_another_function(external_function):
    def decorator(decorated_function):
        def wrapper(*args, **kwargs):
            # Call the external function with the same arguments
            # Assuming the same args are used for both external_function and decorated_function
            condition_result = external_function(*args, **kwargs)

            # If the external function returns True, proceed with the decorated function
            if condition_result:
                print("Condition is True, proceeding with the function...")
                return decorated_function(*args, **kwargs)
            else:
                # If the external function returns False, execute alternative logic
                print("Condition is False, executing alternative logic...")
                return "Alternative logic because the condition was False"
        
        return wrapper
    return decorator




    
   



