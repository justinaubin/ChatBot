# ChatBot

Unfinished project meant to allow users to speak to a chatbot about Corona Virus and have the bot respond intelligently to the user in spoken word.

required packages:

speech-to-text: @google-cloud/speech, request (npm install request)
text-to-speech: aws-sdk
bot.py (python script which interprets user input and replies appropriately):

Package           Version
----------------- ---------
astroid           2.4.2
beautifulsoup4    4.9.1
certifi           2020.6.20
chardet           3.0.4
click             7.1.2
colorama          0.4.3
Flask             1.1.2
future            0.18.2
idna              2.10
isort             4.3.21
joblib            0.16.0
lazy-object-proxy 1.4.3
lxml              4.5.2
mccabe            0.6.1
nltk              3.5
numpy             1.19.1
Pillow            7.2.0
pip               20.2.2
pylint            2.5.3
python-dotenv     0.14.0
regex             2020.7.14
requests          2.24.0
scikit-learn      0.23.2
scipy             1.5.2
setuptools        49.6.0
six               1.15.0
sklearn           0.0
soupsieve         2.0.1
threadpoolctl     2.1.0
toml              0.10.1
torch             1.5.0+cpu
torchvision       0.6.0+cpu
tqdm              4.48.2
typed-ast         1.4.1
urllib3           1.25.10
wheel             0.35.1
wikipedia         1.4.0
wrapt             1.12.1

As of now, users are able to record their questions/comments using their computer microphone, and the chatbot will automatically receive this data in text form and give a response also in text. chatbot.js uses the Google-cloud Speech-to-text API and SOX to record user audio, transcribes it to text, and then uses request to send that text to the local host http://127.0.0.1:5000/. Bot.py then retrieves this data using flask and returns an appropriate response in text. 

I have yet to implement text-to-speech/index.js yet, however, my goal is to have this file automatically receive the text response from bot.py, convert it to audio, and play it back for the user, thus completing the conversation cycle. 

Steps to Run:

1. Open a terminal and cd to the ChatBot directory
2. Run flask run
3. Open another terminal and cd to the speech-to-text directory
4. Run node chatbot.js. A message will appear saying 'Listening, press Ctrl+C to stop.' This will let you know that Sox is recording
5. Speak into your microphone, asking any number of questions about Corona Virus
6. Return to the flask terminal to see the text reponses in the terminal printed to sdout

Side Note about text-to-speech:
As of now users may 
1. Upload a text file containing words you wish to convert to text in speech-to-text/transcription.txt
2. Run node index.js
3. Listen to saved audio file in directory which appears as 'hello.mp3'
