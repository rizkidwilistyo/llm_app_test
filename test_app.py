import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Set up OpenAI API key
load_dotenv()  # Loads environment variables from .env file
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
os.environ["OPENAI_API_KEY"] = openai_key

# Initialize the ChatOpenAI language model
llm = ChatOpenAI(model="gpt-4o-mini")

# Zodiac sign mapping based on month and day
zodiac_dates = {
    "Aries": ((3, 21), (4, 19)),
    "Taurus": ((4, 20), (5, 20)),
    "Gemini": ((5, 21), (6, 20)),
    "Cancer": ((6, 21), (7, 22)),
    "Leo": ((7, 23), (8, 22)),
    "Virgo": ((8, 23), (9, 22)),
    "Libra": ((9, 23), (10, 22)),
    "Scorpio": ((10, 23), (11, 21)),
    "Sagittarius": ((11, 22), (12, 21)),
    "Capricorn": ((12, 22), (1, 19)),
    "Aquarius": ((1, 20), (2, 18)),
    "Pisces": ((2, 19), (3, 20)),
}

# Function to get zodiac and characteristics
def get_zodiac_and_characteristics(birthday, gender):
    zodiac_sign = get_zodiac_sign(birthday)
    if zodiac_sign == "Invalid Date":
        return zodiac_sign, "Please enter a valid date (MM-DD)."
    
    prompt = PromptTemplate(
        input_variables=["zodiac_sign", "gender"],
        template="You are a professional fortune teller. Describe the personality traits of a {zodiac_sign} {gender}."
    )
    response = llm.invoke(prompt.format(zodiac_sign=zodiac_sign, gender=gender))
    return zodiac_sign, response.content

# Function to get Zodiac Sign
def get_zodiac_sign(birthday):
    try:
        month, day = map(int, birthday.split('-'))
        for sign, (start, end) in zodiac_dates.items():
            if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
                return sign
    except ValueError:
        return "Invalid Date"
    return "Unknown"

# Function to get Recommended Movie
def fetch_movies(characteristics):
    prompt = PromptTemplate(
        input_variables=["characteristics"],
        template="Suggest some movies for a person with these characteristics: {characteristics}."
    )
    response = llm.invoke(prompt.format(characteristics=characteristics))
    return response.content

# Button for Get Recommendation Button
def on_submit():
    birthday = entry_birthday.get()
    gender = entry_gender.get()

    zodiac_sign, characteristics = get_zodiac_and_characteristics(birthday, gender)
    # Show error if date or gender is invalid
    if zodiac_sign == "Invalid Date":
        messagebox.showerror("Error", characteristics)
        return
    if not gender:
        messagebox.showerror("Error", "Please enter a valid gender.")
        return
    
    recommendations = fetch_movies(characteristics)
    messagebox.showinfo("Recommendations", f"Your zodiac sign is {zodiac_sign}.\nRecommended Movies:\n{recommendations}")

# GUI setup
root = tk.Tk()
root.title("Movie Recommendation App")

label_birthday = tk.Label(root, text="Enter your Birthday (MM-DD):")
label_birthday.pack()
entry_birthday = tk.Entry(root)
entry_birthday.pack()

label_gender = tk.Label(root, text="Enter your Gender:")
label_gender.pack()
entry_gender = tk.Entry(root)
entry_gender.pack()

submit_button = tk.Button(root, text="Get Movie Recommendations", command=on_submit)
submit_button.pack()

root.mainloop()