import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1hS4vtC7ekVef1fdf1KDb7DbemyOiqfgz3OZ62vxrTNM/edit#gid=0"
url = url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url)
