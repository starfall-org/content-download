from flask import Flask

app = Flask('app')


@app.route('/')
def hello_world():
  return html

html = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      background-color: white;
      color: black;
    }
    a {
      color: blue;
    }
    body.dark-mode {
      background-color: black;
      color: white;
    }
    body.dark-mode a {
      color: orange;
    }
    #link {
      color: green;
    }
    body.dark-mode #link {
      color: orange;
    }
  </style>
  <script>
    function toggleDarkMode() {
      const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.body.classList.toggle('dark-mode', isDarkMode);
    }
    window.addEventListener('load', toggleDarkMode);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', toggleDarkMode);
  </script>
</head>
<body>
  <b>Content Download</b>
</body>
</html>
"""