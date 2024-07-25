import streamlit as st
import json
from azure.cognitiveservices.speech import AudioDataStream, SpeechSynthesizer, SpeechConfig, SpeechSynthesisOutputFormat

# Azure TTS subscription key and region
subscription_key = 'f74fe7fc6f6a48879e486a5b33e1653d'
region = 'westus'

# Configure the speech synthesis
speech_config = SpeechConfig(subscription=subscription_key, region=region)
speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)

# Voice and supported styles dictionary
voices_and_styles = {
    'de-DE-ConradNeural': ['cheerful'],
    'en-GB-RyanNeural': ['chat', 'cheerful'],
    'en-GB-SoniaNeural': ['cheerful', 'sad'],
    'en-IN-NeerjaNeural': ['cheerful', 'empathetic', 'newscast'],
    'en-US-AriaNeural': ['angry', 'chat', 'cheerful', 'customerservice', 'empathetic', 'excited', 'friendly', 'hopeful', 'narration-professional', 'newscast-casual', 'newscast-formal', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-DavisNeural': ['angry', 'chat', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-GuyNeural': ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'newscast', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-JaneNeural': ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-JasonNeural': ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-JennyNeural': ['angry', 'assistant', 'chat', 'cheerful', 'customerservice', 'excited', 'friendly', 'hopeful', 'newscast', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-KaiNeural': ['conversation'],
    'en-US-LunaNeural': ['conversation'],
    'en-US-NancyNeural': ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-SaraNeural': ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering'],
    'en-US-TonyNeural': ['angry', 'cheerful', 'excited', 'friendly', 'hopeful', 'sad', 'shouting', 'terrified', 'unfriendly', 'whispering']
}

# Voices without styles
voices_without_styles = [
    'en-US-AvaMultilingualNeural',
    'en-US-AndrewMultilingualNeural',
    'en-US-EmmaMultilingualNeural',
    'en-US-BrianMultilingualNeural'
]

# Function to generate SSML
def generate_ssml(text, voice, style=None):
    if style:
        ssml = f'''
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="{voice}">
                <mstts:express-as style="{style}">
                    {text}
                </mstts:express-as>
            </voice>
        </speak>
        '''
    else:
        ssml = f'''
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="{voice}">
                {text}
            </voice>
        </speak>
        '''
    return ssml

# Function to synthesize speech from SSML
def synthesize_ssml_to_speech(ssml):
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_ssml_async(ssml).get()
    audio_stream = AudioDataStream(result)
    return audio_stream

# Streamlit UI
st.title('Text-to-Speech Generator')

# Dropdown menu for selecting voice type
voice_type = st.selectbox('Select Voice Type', ['Voices with Styles', 'Voices without Styles'])

if voice_type == 'Voices with Styles':
    # Dropdown menu for selecting voice
    selected_voice = st.selectbox('Select Voice', list(voices_and_styles.keys()))
    
    # Dropdown menu for selecting style based on selected voice
    selected_style = st.selectbox('Select Speaking Style', voices_and_styles[selected_voice])
else:
    # Dropdown menu for selecting voice without styles
    selected_voice = st.selectbox('Select Voice', voices_without_styles)
    selected_style = None  # No style for these voices

# Text area for entering text
text_input = st.text_area('Enter the text you want to convert to speech', height=200)

generate_button = st.button('Generate Speech')

# Generate speech if button is clicked
if generate_button:
    if text_input:
        ssml = generate_ssml(text_input, selected_voice, selected_style)
        audio_stream = synthesize_ssml_to_speech(ssml)
        audio_file = f'{int(time.time())}_speech.wav'  # Unique filename based on timestamp
        audio_stream.save_to_wav_file(audio_file)
        st.audio(audio_file, format='audio/wav')
        st.success(f'Generated speech saved to: {audio_file}')
    else:
        st.error('Please enter some text to convert to speech.')
