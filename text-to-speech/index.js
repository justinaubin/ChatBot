const AWS = require('aws-sdk')
const fs = require('fs')

const Polly = new AWS.Polly({
    region: 'us-east-2'
})

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