#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from happymimi_msgs.srv import StrTrg
from google.cloud import texttospeech
import wave
import pyaudio

#Filename = 'output.wav'
file_path="home/kouya/humble_ws/src/happymimi_voice2/config/wave_data/"

class WavePlay(Node):
    
    def __init__(self):
        super().__init__('waveplay_service')
        self.srv = self.create_service(StrTrg,'/waveplay_srv', self.PlayWaveFile)
        

    def PlayWaveFile(self,request, response):
        print(file_path + request.data)
        try:
            wf = wave.open(file_path+request.data, "rb")
            print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
        except FileNotFoundError:
            print("[Error 404] No such file or directory: " + request.data)
            return StrTrg.Response(result=False)

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        chunk = 1024
        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        return StrTrg.Response(result=True)

def waveMake(sentence,file_name):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=sentence)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-F',
        #ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(file_path+file_name, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + file_name)

def PlayWaveFile(file_name):
    try:
        wf = wave.open(file_path+file_name, "rb")
        print("Time[s]:", float(wf.getnframes()) / wf.getframerate())
    except FileNotFoundError:
        print("[Error 404] No such file or directory: " + file_name)
        return

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    chunk = 1024
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return

def main():
    rclpy.init()
    waveplay_srv = WavePlay()
    rclpy.spin(waveplay_srv)
    rclpy.shutdown()

if __name__ == '__main__':
    main()