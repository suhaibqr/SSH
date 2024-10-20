import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import jwt
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
SECRET_KEY = "your_jwt_secret_key"
if "anvil.app" in anvil.server.get_app_origin():
  my_anvil_app = "https://unbhgzjperrlwjls.anvil.app/FYD3OMOQS6VS7CF5UQ73MGJF"
else:
  my_anvil_app = "http://10.215.10.215:8002"

@anvil.server.route("/token/:token")
def process_jwt(token):
    if not jwt:
        return "Missing token"
    print(token)
    print(SECRET_KEY)
    try:
        # Decode and verify the JWT
    # token_bytes = token.encode('utf-8')
      decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], audience="site-a")
      user_id = decoded_token["sub"]
      print(anvil.server.request.remote_address)
      anvil.server.cookies.shared.set(1, name=user_id, ip=anvil.server.request.remote_address)
      existing_user = app_tables.users.get(email=user_id)
      if not existing_user:
        anvil.users.signup_with_email(user_id,"XXXXXasdjaskldjskdfjlgkjl3jh23k4j2kls;oldf[]asas03042ol",remember= True)
      user = app_tables.users.get(email=user_id)
      anvil.users.force_login(user, remember=True)
      print(f"Welcome {user['email']}, you have successfully logged in to Site-A!")
      # print(anvil.server.cookies.shared.get("ip", "Not Found"))
      # print(anvil.server.cookies.shared.get("name", "Not Found"))
      response = anvil.server.HttpResponse(302, "Redirecting to TDM-Platform...")
      response.headers['Location'] = f"{my_anvil_app}"
      return response
      # return anvil.server.FormResponse('SSH')
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

@anvil.server.callable
def get_cookies():
  return anvil.server.cookies.shared.get("name", "Not Found"), anvil.server.cookies.shared.get("ip", "Not Found")

@anvil.server.callable
def clear_cookies():
  anvil.server.cookies.shared.clear()