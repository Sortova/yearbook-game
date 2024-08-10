These are simple games built with Amazon Q that asks the player to match a picture with a name. It is written in Python using Flask.

To run it, download the files. 

1) Create a Python virtual environment by running "python3 -m venv venv"
2) Activate the environment by running "source venv/bin/activate"
3) Run "pip install -r requirements.txt"

There are two games. 

game-no-1 will display a picture and offer up three names as choices.

game-no-2 will display a name and offer up four pictures from which to choose.

To run the game, cd into the proper directory and run "python3 app.py". This will start a Flask session on localhost port 5000, and you can access it via http://localhost:5000.

To run it in the background, do "nohup python3 app.py &"

To run it on all the interfaces on the machine and not just localhost, edit the last line in app.py and change it to:

app.run(host='0.0.0.0')
