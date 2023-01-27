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

#Let's put a pick list for Users to select their fruits and #Let's filter the list based on the user selection
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Mango','Orange'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the screen
streamlit.dataframe(fruits_to_show)
