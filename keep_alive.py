from flask import Flask
from threading import Thread

app=Flask('')

@app.route('/')
def home():
   return "Good to be alive"

def run():
  app.run(host='0.0.0.0',port=5599)

def keep_alive():
   t = Thread(target=run)
   t.start()