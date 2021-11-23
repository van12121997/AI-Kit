#!/usr/bin/env python3
# coding: utf-8

import os
import math
import pprint
import logging
import soundfile

import pyaudio as pa
import numpy as np

def AudioInput(wav=None, mic=None, sample_rate=16000, chunk_size=16000):
    """
    Create an audio input stream from wav file or microphone.
    Either the wav or mic argument needs to be specified.
    
    Parameters:
        wav (string) -- path to .wav file
        mic (int) -- microphone device index
        sample_rate (int) -- the desired sample rate in Hz
        chunk_size (int) -- the number of samples returned per next() iteration
        
    Returns AudioWavStream or AudioMicStream
    """
    if mic is not None and mic != '':
        return AudioMicStream(mic, sample_rate=sample_rate, chunk_size=chunk_size)
    else:
        raise ValueError('either wav or mic argument must be specified')
 
class AudioMicStream:
    """
    Live audio stream from microphone input device.
    """
    def __init__(self, device, sample_rate, chunk_size):
        self.stream = None
        self.interface = pa.PyAudio()
        self.device_info = find_audio_device(device, self.interface)
        self.device_id = self.device_info['index']
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        
        print('Audio Input Device:')
        pprint.pprint(self.device_info)
    
    def __del__(self):
        self.close()
        self.interface.terminate()
        
    def open(self):
        if self.stream:
            return
            
        self.stream = self.interface.open(format=pa.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        input_device_index=self.device_id,
                        frames_per_buffer=self.chunk_size)
 
        print(f"\naudio stream opened on device {self.device_id} ({self.device_info['name']})")
        print("you can begin speaking now... (press Ctrl+C to exit)\n")
            
    def close(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
       
    def next(self):
        self.open()
            
        samples = self.stream.read(self.chunk_size, exception_on_overflow=False)
        samples = np.frombuffer(samples, dtype=np.int16)
        
        return samples
        
    def __next__(self):
        samples = self.next()
        
        if samples is None:
            raise StopIteration
        else:
            return samples
        
    def __iter__(self):
        self.open()
        return self
              
#
# device enumeration
# 
_audio_device_info = None

def _get_audio_devices(audio_interface=None):
    global _audio_device_info
    
    if _audio_device_info:
        return _audio_device_info
        
    if audio_interface:
        interface = audio_interface
    else:
        interface = pa.PyAudio()
        
    info = interface.get_host_api_info_by_index(0)
    numDevices = info.get('deviceCount')
    
    _audio_device_info = []
    
    for i in range(0, numDevices):
        _audio_device_info.append(interface.get_device_info_by_host_api_device_index(0, i))
    
    if not audio_interface:
        interface.terminate()
        
    return _audio_device_info
     
     
def find_audio_device(device, audio_interface=None):
    """
    Find an audio device by it's name or ID number.
    """
    devices = _get_audio_devices(audio_interface)
    
    try:
        device_id = int(device)
    except ValueError:
        if not isinstance(device, str):
            raise ValueError("expected either a string or an int for 'device' parameter")
            
        found = False
        
        for id, dev in enumerate(devices):
            if device.lower() == dev['name'].lower():
                device_id = id
                found = True
                break
                
        if not found:
            raise ValueError(f"could not find audio device with name '{device}'")
            
    if device_id < 0 or device_id >= len(devices):
        raise ValueError(f"invalid audio device ID ({device_id})")
        
    return devices[device_id]
                
   
def list_audio_inputs():
    """
    Print out information about present audio input devices.
    """
    devices = _get_audio_devices()

    print('')
    print('----------------------------------------------------')
    print(f" Audio Input Devices")
    print('----------------------------------------------------')
        
    for i, dev_info in enumerate(devices):    
        if (dev_info.get('maxInputChannels')) > 0:
            print("Input Device ID {:d} - '{:s}' (inputs={:.0f}) (sample_rate={:.0f})".format(i,
                  dev_info.get('name'), dev_info.get('maxInputChannels'), dev_info.get('defaultSampleRate')))
                 
    print('')
    
    
def list_audio_outputs():
    """
    Print out information about present audio output devices.
    """
    devices = _get_audio_devices()
    
    print('')
    print('----------------------------------------------------')
    print(f" Audio Output Devices")
    print('----------------------------------------------------')
        
    for i, dev_info in enumerate(devices):  
        if (dev_info.get('maxOutputChannels')) > 0:
            print("Output Device ID {:d} - '{:s}' (outputs={:.0f}) (sample_rate={:.0f})".format(i,
                  dev_info.get('name'), dev_info.get('maxOutputChannels'), dev_info.get('defaultSampleRate')))
                  
    print('')
    
    
def list_audio_devices():
    """
    Print out information about present audio input and output devices.
    """
    list_audio_inputs()
    list_audio_outputs()

              

              
