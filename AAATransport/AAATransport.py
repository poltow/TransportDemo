#This is a stripped-down script, which uses the Framework classes to assign MIDI notes to play, stop and record.
from __future__ import with_statement
import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time # We will be using time functions for time-stamping our log file outputs
from consts import *

""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.InputControlElement import MIDI_CC_TYPE  # Base class for all classes representing control elements on a controller
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from ShiftableTransportComponent import ShiftableTransportComponent

class AAATransport(ControlSurface):
    __module__ = __name__
    __doc__ = " AAATransport keyboard controller script "
    
    def __init__(self, c_instance):
        Live.Base.log("LOG: AAATransport __init__ start")
        """everything except the '_on_selected_track_changed' override and 'disconnect' runs from here"""
        ControlSurface.__init__(self, c_instance)
        Live.Base.log(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= AAATransport log opened =--------------") # Writes message into Live's main log file. This is a ControlSurface method.
        with self.component_guard():
            self._set_suppress_features(True) # Turn off rebuild MIDI map until after we're done setting up
            self._setup_transport_control() # Run the transport setup part of the script

            """ Here is some Live API stuff just for fun """
            app = Live.Application.get_application() # get a handle to the App
            maj_v = app.get_major_version() # get the major version from the App
            min_v = app.get_minor_version() # get the minor version from the App
            bug = app.get_bugfix_version() # get the bugfix version from the App
            self.show_message(str(maj_v) + "." + str(min_v) + "." + str(bug)) #put them together and use the ControlSurface show_message method to output version info to console
            self._set_suppress_features(False) #Turn rebuild back on, now that we're done setting up
        Live.Base.log("LOG: AAATransport __init__ end")

    def _set_suppress_features(self, state):
        self.log_message("LOG: AAATransport _set_suppress_features - state="+str(state))
        self._suppress_session_highlight = state
        self._suppress_send_midi = state
        self._set_suppress_rebuild_requests(state)        
        
    def _setup_transport_control(self):
        Live.Base.log("LOG: AAATransport _setup_transport_control start")
        is_momentary = True # We'll only be using momentary buttons here
        transport = ShiftableTransportComponent() #Instantiate a AAATransport Component
        
        """set up the buttons"""
        transport.set_loop_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, CYCLE)) #OK
        transport.set_nudge_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, FF), ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, RWD)) #(up_button, down_button) #OK
        transport.set_punch_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, ARM[1]), ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, ARM[0])) #(in_button, out_button) #OK
        transport.set_seek_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, MUTE[1]), ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, MUTE[0])) # (ffwd_button, rwd_button)  #OK

        transport.set_stop_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, STOP)) #OK
        transport.set_play_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, PLAY)) #ButtonElement(is_momentary, msg_type, channel, identifier) Note that the MIDI_CC_TYPE constant is defined in the InputControlElement module #OK
        transport.set_record_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, REC)) #OK
        
        transport.set_tap_tempo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[0])) #OK
        transport.set_metronome_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[1])) #For some reason, in Ver 7.x.x this method's name has no trailing "e" , and must be called as "set_metronom_button()"... #OK
        transport.set_arrangement_overdub_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[2])) #OK
        transport.set_overdub_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[3])) #OK
        #transport.set_session_overdub_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, 35)) #OK
        
        """set up the sliders"""
        transport.set_tempo_control(SliderElement(MIDI_CC_TYPE, CHANNEL, FADER[0]), SliderElement(MIDI_CC_TYPE, CHANNEL, PAN[0])) #(control, fine_control)#OK
        transport.set_song_position_control(SliderElement(MIDI_CC_TYPE, CHANNEL, PAN[1]))#OK
        
        #REDO, UNDO, SHIFT, BTS
        transport.set_transport_shift_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SET)) #OK
        transport.set_undo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, MARKER_LEFT))
        transport.set_redo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, MARKER_RIGHT))
        transport.set_bts_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[4]))
        transport.set_back_to_arranger_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[5]))
        transport.set_follow_button(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, SOLO[6]))
        
        transport.set_tempo_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, TRACK_LEFT), ButtonElement(is_momentary, MIDI_CC_TYPE, CHANNEL, TRACK_RIGHT)) #(in_button, out_button)
        
        transport.set_launch_quant_slider(SliderElement(MIDI_CC_TYPE, CHANNEL, PAN[2]))
        transport.set_record_quant_slider(SliderElement(MIDI_CC_TYPE, CHANNEL, PAN[3]))
        
        Live.Base.log("LOG: AAATransport _setup_transport_control end")


    def disconnect(self):
        """clean things up on disconnect"""
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= AAATransport log closed =--------------") #Create entry in log file
        ControlSurface.disconnect(self)
        return None
