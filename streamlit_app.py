import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#import streamlit
streamlit.title('My parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🍲Omega 3 and blueberry oatmeal')
streamlit.text('🍹Kale, Spinach and Rocket Smoothie')
streamlit.text('🥚Hard Boiled free range Eggs')
streamlit.text('🥑Avocado Toast')

streamlit.header('🍌🍍Build your own fruit smoothie🍓🍎')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list for Users to select their fruits and Let's filter the list based on the user selection
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index)) #,['Orange','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the screen
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response
#streamlit.header('FruityVice Fruit Advice!')
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)
#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) #Just writes the data to screen
#Take the json version of response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it on screen as table
#streamlit.dataframe(fruityvice_normalized)

#Rearranging new section to display fruityvice api response. Introducing this structure allows us 
#to separate the code that is loaded once from the code that should be repeated each time a new value is entered.
#streamlit.header('FruityVice Fruit Advice!')
#try:
  #fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #if not fruit_choice:
    #streamlit.error("please select a fruit to get information.")
  #else:
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #streamlit.dataframe(fruityvice_normalized)
#except URLError as e:
  #streamlit.error()
  
#Replacing the above code with function to make it more readable and reusable
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
#Section to display fruityvice api response
streamlit.header('FruityVice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#Dont run anything past here while we troubleshoot
#streamlit.stop()

#import snowflake.connector
#Lets display the secret information on screen
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

#Lets try displaying one fruit from fruit list
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * From fruit_load_list")
#my_data_row = my_cur.fetchone()
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row) 

#Lets try displaying one fruit from fruit list with formating anf in table form
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * From fruit_load_list")
#my_data_row = my_cur.fetchone()
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_row)

#Lets fetch all the fruits
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * From fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)

#Move the Fruit Load List Query and Load into a Button Action
streamlit.header("The fruit load list contains:")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("SELECT * From fruit_load_list")
       return my_cur.fetchall() 
      
#Add a button to load fruit
if streamlit.button('Get fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

#Allow the user to add a fruit of choice
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
#streamlit.write('The user entered ', add_my_fruit)
#streamlit.write('Thanks for adding', add_my_fruit)
#This will not work correctly but just go with it for now
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

#Use a Function and Button to Add the Fruit Name Submissions
#Allow end user to add fruit to list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
       return "Thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)
