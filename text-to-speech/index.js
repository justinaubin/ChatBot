const AWS = require('aws-sdk')
const fs = require('fs')

const Polly = new AWS.Polly({
    region: 'us-east-2'
})


// TEST CODE IN PROGRESS TO AUTOMATE THE RETRIEVAL OF THE TEXT RESPONSE FROM THE BOT
// AND OUTPUTTING IT AS SPEECH
// MAYBE JUST WRITE IT IN PYTHON AND HAVE IT IN SAME FILE?


// const request = require('request');

// let url = "http://127.0.0.1:5000/";

// let options = {json: true};

// request(url, options, (error, res, body) => {
//     if (error) {
//         return  console.log(error)
//     };

//     if (!error && res.statusCode == 200) {
//         console.log(body);
//     };
// });

fs.readFile('../speech-to-text/transcription.txt', 'utf8', function(err, data) {
    if (err) throw err;

    const input = {
        Text: data,
        OutputFormat: "mp3",
        VoiceId: "Joanna"
    }
    
    Polly.synthesizeSpeech(input, (err, data) => {
        if (err) {
            console.log(err)
            return
        }
        if (data.AudioStream instanceof Buffer) {
            fs.writeFile('hello.mp3', data.AudioStream, (fsErr) => {
                if (fsErr) {
                    console.log(err)
                    return
                }
                console.log('Success')
            })
        }
    })
});

// const input = {
//     Text: text,
//     OutputFormat: "mp3",
//     VoiceId: "Joanna"
// }

// Polly.synthesizeSpeech(input, (err, data) => {
//     if (err) {
//         console.log(err)
//         return
//     }
//     if (data.AudioStream instanceof Buffer) {
//         fs.writeFile('hello.mp3', data.AudioStream, (fsErr) => {
//             if (fsErr) {
//                 console.log(err)
//                 return
//             }
//             console.log('Success')
//         })
//     }
// })