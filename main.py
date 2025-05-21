from flask import Flask, request, render_template_string, redirect
import requests
import re
import uuid
import datetime
import os

app = Flask(__name__)

# In-memory convo store
convos = {
    "active": {},
    "resumed": {},
    "stopped": {}
}

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Messenger Tool</title>
  <style>
    body { margin: 0; font-family: 'Segoe UI', sans-serif; background-color: #000; color: #fff; }
    header { background-image: url('https://i.ibb.co/nvzcqdh/481763241-970223151881676-1859266586914038652-n.jpg'); background-size: cover; background-position: center; height: 250px; display: flex; align-items: center; justify-content: center; text-shadow: 2px 2px 4px #000; }
    header h1 { font-size: 3em; color: yellow; }
    nav { display: flex; justify-content: center; gap: 40px; padding: 20px; background-color: #111; }
    nav a { text-decoration: none; color: red; font-weight: bold; font-size: 1.2em; transition: 0.3s; }
    nav a:hover { color: yellow; transform: scale(1.1); }
    section { padding: 30px; display: none; }
    section.active { display: block; }
    .card { background-color: #111; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 0 10px rgba(255, 0, 0, 0.4); }
    .card h2 { color: yellow; }
    input, select, textarea { width: 100%; padding: 10px; margin: 10px 0; border: none; border-radius: 5px; }
    button { background-color: red; color: #fff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; transition: 0.3s; }
    button:hover { background-color: yellow; color: black; }
    footer { text-align: center; padding: 20px; background-color: #111; color: yellow; }
  </style>
</head>
<body>
  <header><h1>Messenger Tool</h1></header>
  <nav>
    <a href="#" onclick="showSection('home')">Home</a>
    <a href="#" onclick="requestPassword()">Servers</a>
    <a href="#" onclick="showSection('teams')">My Teams</a>
  </nav>

  <section id="home" class="active">
    <div class="card">
      <h2>View Active Convos</h2>
      {% for name, detail in convos.active.items() %}
        <p><strong>{{ name }}</strong> → {{ detail }}</p>
      {% endfor %}
    </div>
    <div class="card">
      <h2>Resumed Convos</h2>
      {% for name, detail in convos.resumed.items() %}
        <p><strong>{{ name }}</strong> → {{ detail }}</p>
      {% endfor %}
    </div>
    <div class="card">
      <h2>Stopped Convos</h2>
      {% for name, detail in convos.stopped.items() %}
        <p><strong>{{ name }}</strong> → {{ detail }}</p>
      {% endfor %}
    </div>
  </section>

  <section id="servers">
    <div class="card">
      <h2>Start Convo</h2>
      <form method="POST" action="/start">
        <input name="token" placeholder="Token">
        <input name="target" placeholder="Target UID">
        <input name="hatter" placeholder="Hatter Name">
        <input name="message" placeholder="Message">
        <input name="speed" placeholder="Speed (sec)">
        <input name="convo_name" placeholder="Convo Name">
        <button type="submit">Start</button>
      </form>
    </div>
    <div class="card">
      <h2>Active Server Status</h2>
      <p style="color: lime">Online / Working</p>
    </div>
  </section>

 <section id="teams" class="teams">
    <div class="card">
      <img src="https://i.ibb.co/WWndrD0T/481767414-970935001810491-6220678936190020954-n.jpg" alt="Aryan" />
      <h3>

𓆤『٭❲ 𝐀𝐫̽͜ɣ𝐚͢͡ŋ — ː › 🩶 🪽</h3>
      <p>-3:) [[ Throw Me To The Wolves, And
I Will ReTurn Leagiing The Pack ]]=|
web <3 devlpor
User ExiT <3 B-)</p>
    </div>
    <div class="card">
      <img src="https://i.ibb.co/24Fvtws/481515098-1209863837225043-8730609104721614407-n.jpg" alt="Varun" />
      <h3>—⃨̽𝐅ʈ ː※ː†— Ɓ'i̤̚i̤̚ɭɑ X• ⸺̫ᷟ‣⃟'𓆩͙ 🪼 🪽</h3>
      <p>❤️ (y) ; (")> Thə ::[ Crımıınal ]> Larkaa'w :💚:
ՙՙ 𝗯𝝸𝝸ɭɭ𝝰💙💋 𝗢= Dowƞ̽ IInxııd'w =D:) (Y) ____Best Friend</p>
    </div>
  </section>

  <footer>
    Made by Aryan.x3
  </footer>

  <script>
    function showSection(id) {
      document.querySelectorAll('section').forEach(sec => sec.classList.remove('active'));
      document.getElementById(id).classList.add('active');
    }
    function requestPassword() {
      let pass = prompt("Enter access password:");
      if(pass === "sarfurullex123") {
        showSection('servers');
      } else {
        alert("Wrong password!");
      }
    }
  </script>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def home():
    return render_template_string(TEMPLATE, convos=convos)

@app.route("/start", methods=["POST"])
def start_convo():
    token = request.form.get("token")
    target = request.form.get("target")
    hatter = request.form.get("hatter")
    message = request.form.get("message")
    speed = int(request.form.get("speed"))
    convo_name = request.form.get("convo_name")

    # Save convo
    convos["active"][convo_name] = f"To: {target}, From: {hatter}, Msg: {message}, Delay: {speed}s"

    # Send the message instantly (for test)
    try:
        send_message(token, target, f"[{hatter}] {message}")
    except:
        return "Error sending message"

    return redirect("/")

def send_message(token, recipient_id, message):
    url = f"https://graph.facebook.com/v19.0/t_{recipient_id}/messages"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"messaging_type": "UPDATE", "message": {"text": message}}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
