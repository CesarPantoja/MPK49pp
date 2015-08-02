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
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SubjectSlot import subject_slot
from lSyncableSessionComponent import lSyncableSessionComponent

from consts import *

class MPK49pp(ControlSurface):
    __module__=__name__                  #name of the class
    __doc__="MPK49++ extended script"           #documentation    

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():               #Required for live 9
            self.__c_instance = c_instance         #Required for live 9            
            #self.set_suppress_rebuild_requests(True) # Turn off rebuild MIDI map until after we're done setting up

            self._init_transport_component()
            self._init_mixer_component()
            self._setup_session_control()
            
            #self.set_suppress_rebuild_requests(False) #Turn rebuild back on, now that we're done setting up


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
        #ffwd_button = ButtonElement(momentary_seek, MIDI_CC_TYPE, global_channel, FFWD_CC)
        #ffwd_button.name = 'FFwd_Button'

        # rwd
        #rwd_button = ButtonElement(momentary_seek, MIDI_CC_TYPE, global_channel, RWD_CC)
        #rwd_button.name = 'Rwd_Button'        

        #transport.set_seek_buttons(ffwd_button, rwd_button)

    def _init_mixer_component(self):
        is_momentary = True
        global mixer
        mixer = MixerComponent(8)
        mixer.name = 'Mixer'
        mixer.set_track_offset(0)
        self.song().view.selected_track = mixer.channel_strip(0)._track

        for track in range(8):
            #self.log_message("Adding track " + str(track))
            strip = mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            volume_control = SliderElement(MIDI_CC_TYPE, track, 7)

            volume_control.name = str(track) + '_Volume_Control'

            strip.set_volume_control(volume_control)

        return mixer

    def _setup_session_control(self):
        is_momentary = False
        global_channel = 0
        num_tracks = 8 #eight tracks
        num_scenes = 1 #one row
        global session #We want to instantiate the global session as a SessionComponent object (it was a global "None" type up until now...)
        #session = SessionComponent(num_tracks, num_scenes) #(num_tracks, num_scenes) A session highlight ("red box") will appear with any two non-zero values
        session = lSyncableSessionComponent(control_surface = self, name = 'Session', num_tracks = 8, num_scenes = 1, is_enabled=True, auto_name=True, enable_skinning=True)
        session.set_show_highlight( True )

        session.set_offsets(0, 0) #(track_offset, scene_offset) Sets the initial offset of the "red box" from top left
        """set up the session navigation buttons"""

        session.set_track_bank_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, FFWD_CC), ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, RWD_CC)) # (right_button, left_button) This moves the "red box" selection set left & right. 

        session.set_mixer(mixer) #Bind the mixer to the session so that they move together

        self._set_session_highlight(0, 0, 8, 1, False)
        self._on_session_offset_changed.subject = session
        return session

    def set_lsync_offsets(self,x,y,w,h):
        self._log( "set_lsync_offsets: " + str( x ) + ", " + str( y ) + ", " + str( w ) + ", " + str( h ) )
        self.session._set_lsync_offsets( x, y, w, h )

    @subject_slot('offset')
    def _on_session_offset_changed(self):
        session = self._on_session_offset_changed.subject
        self._show_controlled_tracks_message(session)

    def _show_controlled_tracks_message(self, session):
        start = session.track_offset() + 1
        end = min(start + 7, len(session.tracks_to_use()))
        if start < end:
            self.show_message('Controlling Track %d to %d' % (start, end))
        else:
            self.show_message('Controlling Track %d' % start)
        self._set_session_highlight(session.track_offset(), session.scene_offset(), 8, 1, False)
    

