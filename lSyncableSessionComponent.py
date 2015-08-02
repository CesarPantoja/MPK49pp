# (c) 2014 Sigabort, Lee Huddleston, Isotonik Studios; admin@sigabort.co, http://sigabort.co, http://www.isotonikstudios.com

## TAKEN FROM THE TOUCHABLE SCRIPT FILES

import Live

from _Framework.SessionComponent import SessionComponent as SessionComponentBase
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SubjectSlot import subject_slot, subject_slot_group

class lSyncableSessionComponent(SessionComponentBase):
	def __init__(self, control_surface, num_tracks = 0, num_scenes = 0, *a, **k):
		SessionComponentBase.__init__(self, num_tracks, num_scenes, *a, **k)

		self.control_surface = control_surface
		self._logging = True
		
		self._lsync_relation = -1
		self._lsync_track_offset = 0
		self._lsync_scene_offset = 0
		self._lsync_w = 8;
		self._lsync_h = 8;
		self._control_surface_x = -1;
		self._control_surface_y = -1;
		self._control_surface_w = -1;
		self._control_surface_h = -1;

	def _log( self, msg, force = False ):
		if self._logging or force:
			self.contSurface.log_message( msg )
						
	def _set_lsync_offsets_from_control_surface( self, track_offset, scene_offset, w, h, force = False ):
		self._set_lsync_offsets( track_offset, scene_offset, w, h, force )
		
	def _set_lsync_offsets( self, track_offset, scene_offset, w, h, force = False ):
		self._log( "session: set_offsets: " + str( track_offset ) + ", " + str( scene_offset ) + ", w: " + str( w ) + ", h: " + str( h ) +", curr: " + str( self._track_offset.value ) + ", " + str( self._scene_offset.value ) )

		control_surface_changed = False
		
		if self._control_surface_w != w:
			self._control_surface_w = w
			control_surface_changed = True
			
		if self._control_surface_h != h:
			self._control_surface_h = h
			control_surface_changed = True

#		adjusted_track_offset = track_offset 
#		adjusted_scene_offset = scene_offset 
		
		# can't remember why this was commented, but without it, coords sent back to m4l aren't updated for relation
		adjusted_track_offset = track_offset + self._lsync_track_offset;
		adjusted_scene_offset = scene_offset + self._lsync_scene_offset;
		
		update_highlight = False
		
		if track_offset != -1 and scene_offset != -1:
			if hasattr( self, '_track_offset' ) and ( self._track_offset.value != track_offset or force ):
				self._log( "Sending track offset: " + str( adjusted_track_offset ) )
				self._track_offset.receive_value( adjusted_track_offset )
				self._track_offset.value = track_offset
				update_highlight = True
						
			if hasattr( self, '_scene_offset' ) and ( self._scene_offset.value != scene_offset or force ):
				self._log( "Sending scene offset: " + str( adjusted_scene_offset ) )
				self._scene_offset.receive_value( adjusted_scene_offset )
				self._scene_offset.value = scene_offset
				update_highlight = True

			if hasattr( self, '_session_width' ) and ( self._session_width.value != w or force ):
				self._log( "Sending session width: " + str( self._session_width ) )
				self._session_width.receive_value( w )
				self._session_width.value = w

			if hasattr( self, '_session_height' ) and ( self._session_height.value != w or force ):
				self._log( "Sending session height: " + str( self._session_height ) )
				self._session_height.receive_value( h )
				self._session_height.value = h

#		
		if update_highlight:
			self.set_highlight( track_offset, scene_offset, w, h )
    	
	def set_highlight( self, x, y, w = -1, h = -1 ):
		self._log( "set highlight: " + str( x ) + ", " + str( y ) + ", " + str( w ) + ", " + str( h ) )	

		if x < 0:
			x = 0
			
		if y < 0:
			y = 0
			
		if w == -1:
			w = self._control_surface_w
			
		if h == -1:
			h = self._control_surface_h
			
		self.control_surface._set_session_highlight( x, y, w, h, False )
					
	def set_launchsync_relation( self, val ):
		self._log( "set_launchsyc_relation: " + str( val ) )

		self._lsync_relation = val
		self._lsync_track_offset = self._control_surface_x
		self._lsync_scene_offset = self.control_surface_y
		
		if val == 1:
			self._lsync_track_offset = self._control_surface_x + self._control_surface_w
		elif val == 2:
			self._lsync_scene_offset = self._control_surface_y + self._control_surface_h
		elif val == 3:
			self._lsync_track_offset = self._control_surface_x - self._lsync_w
			
			if self._lsync_track_offset < 0:
				self._lsync_track_offset = 0
		elif val == 4:
			self._lsync_scene_offset = self._control_surface_y - self._lsync_h
			
			if self._lsync_scene_offset < 0:
				self._lsync_scene_offset = 0
			
		self._set_lsync_offsets( 0, 0, self._control_surface_w, self._control_surface_h, True )  
