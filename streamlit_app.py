import streamlit

streamlit.title('My parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🍲Omega 3 and blueberry oatmeal')
streamlit.text('🍹Kale, Spinach and Rocket Smoothie')
streamlit.text('🥚Hard Boiled free range Eggs')
streamlit.text('🥑Avocado Toast')

streamlit.header('🍌🍍Build your own fruit smoothie🍓🍎')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list for Users to select their fruits and Let's filter the list based on the user selection
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index)) #,['Orange','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the screen
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response
streamlit.header('FruityVice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json()) #Just writes the data to screen

#Take the json version of response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#output it on screen as table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

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
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * From fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#Allow the user to add a fruit of choice
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('The user entered ', add_my_fruit)
