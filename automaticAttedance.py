import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import csv
from datetime import datetime  # Import datetime for timestamp

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        subject_dir = f"Attendance\\{Subject}"
        if os.path.exists(subject_dir):
            os.chdir(subject_dir)
        else:
            t = f"Directory for {Subject} not found."
            text_to_speech(t)
            return

        # Get the current date and timestamp for file naming
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")  # e.g., '2024-11-27'
        time_str = now.strftime("%H-%M-%S")  # e.g., '14-30-15'
        
        # The filenames should be like 'Subject_date_time.csv'
        filenames = glob(f"Attendance\\{Subject}\\{Subject}_{date_str}_{time_str}.csv")
        
        if not filenames:
            t = f"No CSV files found for subject: {Subject} with the timestamp."
            text_to_speech(t)
            return
        
        # Read and merge CSV files if multiple files exist with the same subject name
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)

        # Calculate Attendance
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf.loc[i, "Attendance"] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'

        try:
            newdf.to_csv(f"{Subject}_{date_str}_{time_str}.csv", index=False)
        except Exception as e:
            t = f"Error saving attendance: {e}"
            text_to_speech(t)
            return

        # Display the Attendance Sheet
        root = Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")
        cs = f"Attendance\\{Subject}\\{Subject}_{date_str}_{time_str}.csv"
        
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:
                    label = Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, "bold"),
                        bg="black",
                        text=row,
                        relief=RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1

        root.mainloop()

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    attf = Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
