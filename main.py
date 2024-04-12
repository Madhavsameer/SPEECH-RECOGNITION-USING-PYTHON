from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Madhav Sameer' #can give any sting as SECRET_KEY. It is for flash messages

#to upload file
@app.route("/", methods=['GET','POST'])
def base():
    transcripted_text = ""
    
    if request.method == 'POST':
        print("form data received")

        #for not submitting file and just clicking on transcribe button
        #request.FILES is a multivalue dictionary like object that keeps the files uploaded through an upload file button.
        if "file" not in request.files:
            flash("Please select a .wav file", category="error")
            return redirect(request.url)
                
        file = request.files["file"]
        #for if the file has no name
        if file.filename == "":
            flash("Please select a .wav file", category="error")
            return redirect(request.url)

        #for speech recognition if file exists
        if file:
            recognizer = sr.Recognizer() #to initialize speech recognition
            #to pass audio file to record function of Recognizer module
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)

            transcripted_text = recognizer.recognize_google(audio_data, key=None)
            flash("Your transcription is ready", category="success")

    return render_template("base.html", transcripted_text=transcripted_text)

#to speak
@app.route("/record/")
def record():
    text=""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            flash("Your transcription is ready", category="success")
        except:
            flash("Please speak something after clicking on mic", category="error")

    return render_template("base.html", transcripted_text=text)


if __name__ == "__main__":
    app.run(debug=True, threaded=True) #treaded is for uploading files
