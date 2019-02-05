# Text to Speech use open API: FPT Speech Synthesis
#==================#
# Code for Home Assistant
# Code in configuration.yaml
# tts_hass:
# Code in automation
# - alias: Example text2speech by fpt_api
  # trigger:
    # platform: state
    # entity_id: switch.light
    # to: 'on'
  # action:
    # service: tts_hass.fpt_say
    # data:
      # player_id: media_player.room_player
      # message: "Den vua duoc bat sang."
      # voice_type: 'nu_hue'
      # url_hassio: 'https://192.168.1.100:8123'
#==================#	  

DOMAIN = 'tts_hass'
import requests, json, os, time
REQUIREMENTS = ['requests==1.0.2']

def setup(hassio, config):

    def text_speech_fpt(fpt_say):
	
        # Change your OpenFPT_API key
        openfpt_api = '..dfa6fba1b627431cb95533f1ab82308c'
		
        # Declare variables in Home Assistant
        media_id = fpt_say.data.get('player_id')
        text_message = fpt_say.data.get('message')[0:500]
        voice_type = fpt_say.data.get('voice_type')
        url_hassio = fpt_say.data.get('url_hassio')
		
        # List voice of FPT Speech Synthesis
        voice_list = {'nam_mien_bac': 'male', 'nu_mien_bac': 'female', 'nu_mien_nam': 'hatieumai','nu_hue': 'ngoclam'}
        voice_type = voice_list.get(voice_type)	
        # HTTP Request
        url = 'http://api.openfpt.vn/text2speech/v4'
        # Header Parameters
        header_parameters = {'api_key': openfpt_api, 'speed': '2', 'prosody': '1', 'voice': voice_type}
        message_utf8 = str(text_message).encode('utf-8')
        res_response = requests.post(url, data = message_utf8, headers = header_parameters)
        json_data = res_response.json()['async']
		
        # Path of audio file
        file_path = '/config/www/tts/tts_hassio.mp3'	
        audio_path = '/local/tts/tts_hassio.mp3'
        # Delete if File exist
        if os.path.exists(file_path):
            os.remove(file_path)
        # Create new audio file from the text_message
        filesize = 1		
        while filesize < 2000:
            time.sleep(0.2)
            res_response = requests.get(json_data)
            # Open tts_hassio.mp3 and write binary mode
            with open(file_path, 'wb') as (audio_file): 
                audio_file.write(res_response.content)
            audio_file.close()
            filesize = int(os.path.getsize(file_path))
			
        ## Play audio file on media player ##	
        # media_content_id
        url_audio = url_hassio + audio_path
        # service data for 'CALL SERVICE' in Home Assistant
        service_data = {'entity_id': media_id, 'media_content_id': url_audio, 'media_content_type': 'music'}
        # Call service from Home Assistant
        hassio.services.call('media_player', 'turn_off')
        time.sleep(0.1)
        hassio.services.call('media_player', 'play_media', service_data)

    hassio.services.register(DOMAIN, 'fpt_say', text_speech_fpt)
    return True
