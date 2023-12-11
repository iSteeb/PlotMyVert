import imaplib
import email
import pandas as pd
from datetime import datetime as dt
import plotly.express as px
import numpy as np
import math
from .models import *
import json
import plotly.io as pio


def login_to_email(SSL, server, port, email, password):
  M = imaplib.IMAP4_SSL(server, int(port)) if SSL else imaplib.IMAP4(server, port)
  M.login(email, password)
  print("Email login successful.")
  return M

# returns a list of email ids
def select_session_emails(M, receiver):
  M.select()
  typ, data = M.search(None, 'SUBJECT', '"Session Data to Open in Excel"', "TO", receiver)
  if len(data) > 0 and data[0] != None:
    print("Found " + str(len(data[0].split())) + " emails with session data.")
    return data[0].split()
  else:
    print("No emails with session data found.")
    return []
  
def get_all_new_data_from_emails(M, mail_ids):
  files = []
  for mail_id in mail_ids:
    typ, mail_ids = M.fetch(mail_id, 'BODY[]')
    msg = email.message_from_bytes(mail_ids[0][1])   
    for part in msg.walk():
      if part.get_content_type() == "application/vnd.ms-excel":
        files.append(part)
  return files

def generate_dataframe_from_excel(excel_file, user_instance):
  print("Accessing Excel session data from file.")
  session_filename = excel_file.get_filename()
  filename_date = session_filename.split("_")[3].split("-")
  filename_time = session_filename.split("_")[4].split(".")[0].split("-")
  timestamp = dt(int(filename_date[2]), int(filename_date[1]), int(filename_date[0]), int(filename_time[0]), int(filename_time[1]))
  print("Processing " + session_filename + " (" + str(timestamp) + ") from email.")  
  if JumpSessionModel.objects.filter(user=user_instance, start_datetime=timestamp).exists():
    print("Data has already beed added.")
    return None
  else:
    print("Data has not been processed previously.")
    session_data = excel_file.get_payload(decode=True)
    session_dataframe = pd.DataFrame()
    session_dataframe["Timestamp"] = pd.read_xml(session_data, xpath="//ss:Worksheet[@ss:Name='Jumps']/ss:Table/ss:Row/*[@ss:StyleID='s2083']/*", namespaces={"ss": "urn:schemas-microsoft-com:office:spreadsheet"}).iloc[:, 1]
    session_dataframe["Timestamp"] = pd.to_datetime(session_dataframe["Timestamp"])
    session_dataframe["Jump Height (cm)"] = pd.read_xml(session_data, xpath="//ss:Worksheet[@ss:Name='Jumps']/ss:Table/ss:Row/*/*[@ss:Type='Number']", namespaces={"ss": "urn:schemas-microsoft-com:office:spreadsheet"}).iloc[:, 1]
    print("Session dataframe generated.")
    session_dataframe.start_datetime = timestamp
    session_dataframe.count = len(session_dataframe)
    session_dataframe.average_high = session_dataframe['Jump Height (cm)'].nlargest(math.ceil(len(session_dataframe) / 4)).median()
    session_dataframe.highest = session_dataframe["Jump Height (cm)"].max()
    print(session_dataframe)
    return session_dataframe
    
     
def generate_plot_from_dataframe(session_dataframe):
  start_datetime = session_dataframe.start_datetime
  average_high = session_dataframe.average_high
  highest = session_dataframe.highest
  print("Generating plot for your " + str(start_datetime) + " session (n = " + str(len(session_dataframe)) + " x̄ = " + str(round(average_high, 1)) + " ∨ = " + str(round(highest, 1)) + ").")
  # Scatter plot
  fig = px.scatter(session_dataframe, x="Timestamp", y="Jump Height (cm)", title="Jump Height (cm) vs. Time on " + str(start_datetime.date()) + " at " + str(start_datetime.time().strftime("%H:%M")), labels={"Timestamp": "Time", "Jump Height (cm)": "Jump Height (cm)"}, hover_data={"Timestamp": "|%H:%M|", "Jump Height (cm)": True})
  # Add a horizontal line at the average high height
  fig.add_hline(y=average_high, line_dash="dash", line_color="red", annotation_text="x̄ = " + str(round(average_high, 1)), annotation_position="bottom right")
  # Mark the highest jump in red
  fig.add_trace(px.scatter(session_dataframe[session_dataframe["Jump Height (cm)"] == highest], x="Timestamp", y="Jump Height (cm)", color_discrete_sequence=["red"], hover_data={"Timestamp": "|%H:%M|", "Jump Height (cm)": True}).data[0])
  # add a polynomial trendline with timestamp as the x-axis and jump height as the y-axis
  z = np.polyfit(session_dataframe["Timestamp"].astype(np.int64) // 10**9, session_dataframe["Jump Height (cm)"], 2)
  p = np.poly1d(z)
  fig.add_trace(px.line(x=session_dataframe["Timestamp"], y=p(session_dataframe["Timestamp"].astype(np.int64) // 10**9), color_discrete_sequence=["red"], ).data[0])
  plot_json_string = pio.to_json(fig)
  return plot_json_string

def save_jump_session_to_database(user_instance, session_dataframe,  plotly_json):
  database_entry = JumpSessionModel.objects.create(user=user_instance, start_datetime=session_dataframe.start_datetime, count=session_dataframe.count, average_high=session_dataframe.average_high, highest=session_dataframe.highest, plotly_json=plotly_json)
  print("Saved session dataframe and plot to database.")
  return database_entry

def save_jump_session_jumps_to_database(session_database_entry, session_dataframe):
  JumpSessionJumpsModel.objects.bulk_create([JumpSessionJumpsModel(session=session_database_entry, timestamp=row['Timestamp'], jump_height=row['Jump Height (cm)']) for _, row in session_dataframe.iterrows()])

def mark_emails_for_delete(M, mail_ids):
  for mail_id in mail_ids:
    print("Marking email " + str(mail_id) + " for deletion.")
    M.store(mail_id, '+FLAGS', '\\Deleted')
    
def logout_from_email(M):
  M.expunge()
  M.close()
  M.logout()
  print("Email logout successful.")

    


# today = datetime.date.today()
# startOfWeek = today - datetime.timedelta(days=today.weekday())
# endOfWeek = today + datetime.timedelta(days=(6 - today.weekday()))
# options = ["[THIS WEEK]", "[LAST WEEK]", "[LAST SIX WEEKS]", "[THIS SEASON]", "[CUSTOM DATE]"]
# option, index = pick.pick(options, "Select a Period to Graph", indicator='=>', default_index=0)
# startDate = ""
# if option == "[CUSTOM DATE]":
#     startDate = input("Enter a start date (YYYY-MM-DD): ")
#     startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
# elif option == "[LAST WEEK]":
#     startDate = startOfWeek - datetime.timedelta(weeks=1)
#     endOfWeek = endOfWeek - datetime.timedelta(weeks=1)
# elif option == "[LAST SIX WEEKS]":
#     startDate = startOfWeek - datetime.timedelta(weeks=5)
# elif option == "[THIS SEASON]":
#     startDate = datetime.date(2023, 6, 1)
# elif option == "[THIS WEEK]":
#     startDate = startOfWeek

# subCollection = collection[(collection["Datetime"].dt.date >= startDate) & (collection["Datetime"].dt.date <= endOfWeek)]
# subCollection["Date"] = subCollection["Datetime"].dt.date
# subAverageHigh = subCollection['Jump Height (cm)'].nlargest(math.ceil(len(subCollection) / 4)).median()
# highest = subCollection["Jump Height (cm)"].max()

# seasonPlot = subCollection.plot.scatter(x="Date", y="Jump Height (cm)")
# seasonPlot.set_title("Jump Height (cm) vs. Date from " + str(startDate) + " to " + str(endOfWeek))
# seasonPlot.set_xlabel("Date")
# seasonPlot.set_ylabel("Jump Height (cm)" + " n = " + str(len(subCollection)) + " x̄ = " + str(round(subAverageHigh, 1)))
# seasonPlot.set_xlim(startDate - datetime.timedelta(days=1), endOfWeek + datetime.timedelta(days=1))
# seasonPlot.set_xticks(pd.date_range(start=startDate - datetime.timedelta(days=1), end=endOfWeek + datetime.timedelta(days=1), freq='M'))
# seasonPlot.axhline(y=subAverageHigh, color='r', linestyle='-')
    
# plt.show()

# print("... done. Terminating.")