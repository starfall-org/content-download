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

    // Thực hiện kiểm tra khi trang được tải
    window.addEventListener('load', toggleDarkMode);

    // Thực hiện kiểm tra khi chế độ màu sắc thay đổi
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', toggleDarkMode);
  </script>
</head>
<body>
  <b>Hello, Welcome to <a href='https://t.me/contentdownload_bot' id='link'>Content Download!</a></b>.
</body>
</html>
"""