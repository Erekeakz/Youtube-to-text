def home(request):
    # checking whether request.method is post or not
    if request.method == 'POST':
        # getting link from frontend
        link = request.POST['link']
        down = "downtext/" + str(len(listdir("downtext")))

        transcribed_audio_file_name = down + "/transcribed_speech.wav"

        youtube_video_url = link

        yt_obj = YouTube(youtube_video_url)

        yt_obj.streams.get_audio_only().download(output_path=down, filename='file.mp3')

        zoom_video_file_name = down + "/file.mp3"

        audioclip = AudioFileClip(zoom_video_file_name)
        audioclip.write_audiofile(transcribed_audio_file_name)
        with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        total_duration = math.ceil(duration / 60)
        r = sr.Recognizer()
        for i in range(0, total_duration):
            with sr.AudioFile(transcribed_audio_file_name) as source:
                audio = r.record(source, offset=i * 60, duration=60)
            f = open(down + "/transcription.txt", "a")
            f.write(r.recognize_google(audio, language='ru'))
            f.write(" ")
            print('Текст успешно записан!')
        f.close()

        # returning HTML page
        return render(request, 'home.html')
    return render(request, 'home.html')
