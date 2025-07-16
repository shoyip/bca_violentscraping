from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import json
import pytz
from datetime import datetime, timedelta

def geocode(s):
  r = requests.get(f"http://photon.komoot.io/api/?q={s}")
  data = json.loads(r.text)
  try:
    first_coords = data['features'][0]['geometry']['coordinates']
  except:
    first_coords = None
  return first_coords

def get_start_time(s):
  try:
    ore = str(s.split("ore")[1][1:3]) + str(s.split("ore")[1][4:6])
    try:
      ore_tipo = type(int(ore))
      return str(ore)
    except ValueError:
      return "0000"
  except:
    return "0000"

def parse_tz_string(s):
  tzid = s.split("=")[1].split("T")[0].split(":")[0]
  dt_str = s.split("=")[1].split("T")[0].split(":")[1] + s.split("B")[1]
  try:
    dt = pd.to_datetime(dt_str, format="%Y%m%d%H%S")
  except:
    dt = pd.to_datetime(dt_str, format="%Y%m%d")
  return dt.tz_localize(pytz.timezone(tzid))

def estrattoreF(regione, date_str):
  r = requests.get("https://iltaccodibacco.it/"+regione+"/eventi/"+date_str+"/")
  html_doc = r.text
  soup = BeautifulSoup(html_doc, 'html.parser')
  listadieventi=[]
  for evento in soup.find_all('div', class_="titolo blocco-locali"):
    id_evento=str(evento.h2.a.get('name'))
    r1=requests.get("https://iltaccodibacco.it/index.php?reg=puglia&md=evt&id_evento="+id_evento+"&az=ics")
    listadieventi.append(r1.text)
  calendario_ics="\n".join(listadieventi)

  contatore=0
  in_evento=0
  lista_categorie=[]
  datainizio=[]
  datafine=[]
  summary=[]
  description=[]
  location=[]
  url=[]
  categories=[]
  for line in calendario_ics.split("\n"):
    if line=="BEGIN:VEVENT":
      in_evento=1
      contatore=contatore+1
    if line=="END:VEVENT":
      in_evento=0

    if in_evento==1 :
      if line.startswith("DTSTART"):
        if ";" in line :
          datainizio.append(line.split(";",1)[1])
      if line.startswith("DTEND"):
        if ";" in line :
          datafine.append(line.split(";",1)[1])
      if line.startswith("SUMMARY"):
        summary.append(line.split(":",1)[1])
      if line.startswith("DESCRIPTION"):
        description.append(line.split(":",1)[1])
      if line.startswith("LOCATION"):
        location.append(line.split(":",1)[1])
      if line.startswith("URL"):
        url.append(line.split(":",1)[1])

  df = pd.DataFrame(list(zip(datainizio, datafine, summary, description, location, url)), columns=["Data Inizio", "Data Fine", "Titolo", "Descrizione"  , "Luogo", "URL"])

  ora_inizio_raw = df['Descrizione'].apply(get_start_time)
  df['Data Inizio'] = df['Data Inizio'] + "B" + ora_inizio_raw
  df['Data Inizio'] = df['Data Inizio'].apply(parse_tz_string)
  df['Data Fine'] = df['Data Fine'] + "B0000"
  df['Data Fine'] = df['Data Fine'].apply(parse_tz_string)

  return df
  
if __name__ == '__main__':
  today = datetime.today()
  next_week_dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(28)]
  dfs_days = []
  for date_str in next_week_dates:
      df_day = estrattoreF("bari",date_str)
      dfs_days.append(df_day)
      print('fatto data', date_str)
      
  df_all = pd.concat(dfs_days)
  df_all.to_csv('tdb_month.csv')
