"""
SeoulAI October Hackaton Checkers Board Arena
Emilio Coronado, emilio.mobile@gmail.com
seoulai.com
2018
"""

from  server import create_server

if __name__ == '__main__':
    app = create_server()
    app.run(debug=True)