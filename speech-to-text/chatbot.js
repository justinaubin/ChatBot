const recorder = require('node-record-lpcm16');
const request = require('request');

// Imports the Google Cloud client library
const speech = require('@google-cloud/speech');
const fs = require('fs');

// Creates a client
const client = new speech.SpeechClient();

/**
 * TODO(developer): Uncomment the following lines before running the sample.
 */
const encoding = 'LINEAR16';
const sampleRateHertz = 22050;
const languageCode = 'en-US';

const requestAPI = {
  config: {
    encoding: encoding,
    sampleRateHertz: sampleRateHertz,
    languageCode: languageCode,
  },
  interimResults: false, // If you want interim results, set this to true
};

// Create a recognize stream
const recognizeStream = client
  .streamingRecognize(requestAPI)
  .on('error', console.error)
  .on('data', data => {
    let transcription = ""
    if (data != undefined) transcription = `${data.results[0].alternatives[0].transcript}`;
    else transcription = "first_message"; //console.log('\nReached transcription time limit, press Ctrl+C\n');

    request.post(
      'http://127.0.0.1:5000/',
      {json: {data: transcription}},
      function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log(body);
        }
      }
    );
  });


// Start recording and send the microphone input to the Speech API.
// Ensure SoX is installed, see https://www.npmjs.com/package/node-record-lpcm16#dependencies
recorder
  .record({
    sampleRateHertz: sampleRateHertz,
    threshold: 20,
    thresholdStart: 20,
    // Other options, see https://www.npmjs.com/package/node-record-lpcm16#options
    verbose: false,
    recordProgram: 'sox', // Try also "arecord" or "sox"
    silence: '10.0',
  })
  .stream()
  .on('error', console.error)
  .pipe(recognizeStream);

console.log('Listening, press Ctrl+C to stop.');