from __future__ import with_statement #Required for live 9, has to be first line of the script
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.MixerComponent import MixerComponent
from _Framework.SliderElement import SliderElement

from consts import *

class MPK49pp(ControlSurface):
    __module__=__name__                  #name of the class
    __doc__="MPK49 extended script"           #documentation    

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():               #Required for live 9
            self.__c_instance = c_instance         #Required for live 9            
            self._init_transport_component()
            self._init_mixer_component()


    def _init_transport_component(self):
        is_momentary = True
        momentary_seek = False
        global_channel = 0
        transport = TransportComponent()
        transport.name = 'Transport'
        
        # rec 
        rec_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, REC_CC)
        rec_button.name = 'Record_Button'
        transport.set_record_button(rec_button)

        # play
        play_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, PLAY_CC)
        play_button.name = 'Play_Button'
        transport.set_play_button(play_button)

        # stop
        stop_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, STOP_CC)
        stop_button.name = 'Stop_Button'
        transport.set_stop_button(stop_button)
        
        # ffw
        ffwd_button = ButtonElement(momentary_seek, MIDI_CC_TYPE, global_channel, FFWD_CC)
        ffwd_button.name = 'FFwd_Button'

        # rwd
        rwd_button = ButtonElement(momentary_seek, MIDI_CC_TYPE, global_channel, RWD_CC)
        rwd_button.name = 'Rwd_Button'        

        transport.set_seek_buttons(ffwd_button, rwd_button)

    def _init_mixer_component(self):
        is_momentary = True
        mixer = MixerComponent(8)
        mixer.name = 'Mixer'

        for track in range(8):
            #self.log_message("Adding track " + str(track))
            strip = mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            volume_control = SliderElement(MIDI_CC_TYPE, track, 7)

            volume_control.name = str(track) + '_Volume_Control'

            strip.set_volume_control(volume_control)

        return mixer
