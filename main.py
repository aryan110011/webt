from flask import Flask, request, render_template_string, redirect
import uuid

app = Flask(__name__)

# In-memory convo storage
convo_data = {
    'started': {},
    'resumed': {},
    'stopped': {}
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Auto Messenger Tool</title>
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
      cursor: pointer;
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
    input, select {
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
  </style>
</head>
<body>
  <header>
    <h1>Auto Messenger Tool</h1>
  </header>
  <nav>
    <a onclick="showSection('home')">Home</a>
    <a onclick="requestPassword()">Servers</a>
    <a onclick="showSection('teams')">My Teams</a>
  </nav>

  <section id="home" class="active">
    <div class="card">
      <h2>View Convo</h2>
      {% for name, details in started.items() %}
        <p><strong>{{ name }}</strong>: Started for {{ details['target_id'] }} ({{ details['token_type'] }})</p>
      {% else %}
        <p>No started convos.</p>
      {% endfor %}
    </div>
    <div class="card">
      <h2>Resume Convo</h2>
      {% for name, details in resumed.items() %}
        <p><strong>{{ name }}</strong>: Resumed at {{ details['timestamp'] }}</p>
      {% else %}
        <p>No resumed convos.</p>
      {% endfor %}
    </div>
    <div class="card">
      <h2>Stop Convo</h2>
      {% for name, details in stopped.items() %}
        <p><strong>{{ name }}</strong>: Stopped at {{ details['timestamp'] }}</p>
      {% else %}
        <p>No stopped convos.</p>
      {% endfor %}
    </div>
  </section>

  <section id="servers">
    <form method="post" action="/start">
      <div class="card">
        <h2>Start Convo</h2>
        <select name="token_type">
          <option>Single Token</option>
          <option>Multi Token (File)</option>
        </select>
        <input type="text" name="target_id" placeholder="Target ID" required>
        <input type="text" name="hatter_name" placeholder="Hatter Name" required>
        <select name="msg_type">
          <option>Single Message</option>
          <option>File Message</option>
        </select>
        <input type="text" name="speed" placeholder="Message Speed" required>
        <input type="text" name="convo_name" placeholder="Convo Name" required>
        <button type="submit">Start</button>
      </div>
    </form>
    <form method="post" action="/resume">
      <div class="card">
        <h2>Resume Convo</h2>
        <input type="text" name="convo_name" placeholder="Enter convo name...">
        <button type="submit">Resume</button>
      </div>
    </form>
    <form method="post" action="/stop">
      <div class="card">
        <h2>Stop Convo</h2>
        <input type="text" name="convo_name" placeholder="Enter convo name...">
        <button type="submit">Stop</button>
      </div>
    </form>
  </section>

  <section id="teams">
    <div class="card">
      <h3>🩶 Aryan.x3</h3>
      <p>“Throw me to the wolves, I will return leading the pack.”</p>
    </div>
    <div class="card">
      <h3>🪼 Varun</h3>
      <p>“The Criminal Larkaa 💚”</p>
    </div>
  </section>

  <footer>
    Made by Aryan
  </footer>

  <script>
    function showSection(id) {
      document.querySelectorAll('section').forEach(sec => sec.classList.remove('active'));
      document.getElementById(id).classList.add('active');
    }

    function requestPassword() {
      let pass = prompt("Enter access password:");
      if (pass === "sarfurullex123") {
        showSection('servers');
      } else {
        alert("Wrong password!");
      }
    }
  </script>
</body>
</html>
'''

from datetime import datetime

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, started=convo_data['started'], resumed=convo_data['resumed'], stopped=convo_data['stopped'])

@app.route('/start', methods=['POST'])
def start():
    convo_name = request.form['convo_name']
    convo_data['started'][convo_name] = {
        'token_type': request.form['token_type'],
        'target_id': request.form['target_id'],
        'hatter': request.form['hatter_name'],
        'msg_type': request.form['msg_type'],
        'speed': request.form['speed']
    }
    return redirect('/')

@app.route('/resume', methods=['POST'])
def resume():
    convo_name = request.form['convo_name']
    convo_data['resumed'][convo_name] = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop():
    convo_name = request.form['convo_name']
    convo_data['stopped'][convo_name] = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
