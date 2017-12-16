#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/TransportComponent.py
from _Framework.TransportComponent import TransportComponent as TransportComponentBase
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.SubjectSlot import subject_slot
from _Framework.Control import ButtonControl
from _Framework.EncoderElement import EncoderElement
import Live 

TEMPO_TOP = 167.0
TEMPO_BOTTOM = 40.0
TEMPO_FINE_RANGE = 12.7
SONG_TIME_MULT = 5

class ShiftableTransportComponent(TransportComponentBase):

    rec_quantization_button = ButtonControl()


    def __init__(self, *a, **k):
        super(ShiftableTransportComponent, self).__init__(*a, **k)
        
        #Fix for Punch In/Out bug (momentary behavior)
        self._punch_in_toggle.is_momentary = False
        self._punch_out_toggle.is_momentary = False
        
        self._shift_button = None
        self._shift_pressed = False
        self._undo_button = None
        self._redo_button = None
        self._bts_button = None #BackTo Start
     
        #Quantize functions????
#         Self._last_quant_value = Live.Song.RecordingQuantization.rec_q_eight
#         Self._on_quantization_changed.subject = Self.song()
#         Self._update_quantization_state()
#         Self.set_quant_toggle_button = Self.rec_quantization_button.set_control_element
        
        #Quneao
        self._tempo_encoder_control = None
        self._tempo_down_button = None
        self._tempo_up_button = None
        self._tempo_session_value = self.song().tempo

        #LiveControl
        self._launch_quant_slider = None
        self._record_quant_slider = None
        self._back_to_arranger_button = None
        self._follow_button = None
        self._tempo_up_button = None
        self._tempo_down_button = None

        self.song().add_midi_recording_quantization_listener(self._on_record_quantisation_changed)
        self.song().add_clip_trigger_quantization_listener(self._on_launch_quantisation_changed)
        self.song().add_back_to_arranger_listener(self._on_back_to_arranger_changed)
        self.song().view.add_follow_song_listener(self._on_follow_changed)
        self.send_init()
        
    def send_init(self):
        self._on_record_quantisation_changed()
        self._on_launch_quantisation_changed()
        self._on_back_to_arranger_changed()
        self._on_follow_changed()        

    def disconnect(self):
        self.song().remove_midi_recording_quantization_listener(self._on_record_quantisation_changed)
        self.song().remove_clip_trigger_quantization_listener(self._on_launch_quantisation_changed)
        self.song().remove_back_to_arranger_listener(self._on_back_to_arranger_changed)
        self.song().view.remove_follow_song_listener(self._on_follow_changed)


        if self._record_quant_slider != None:
            self._record_quant_slider.remove_value_listener(self._record_quant_value)
            self._record_quant_slider = None
        if self._launch_quant_slider != None:
            self._launch_quant_slider.remove_value_listener(self._launch_quant_value)
            self._launch_quant_slider = None
        if self._back_to_arranger_button != None:
            self._back_to_arranger_button.remove_value_listener(self._back_to_arranger_value)
            self._back_to_arranger_button = None
        if self._follow_button != None:
            self._follow_button.remove_value_listener(self._follow_value)        
            self._follow_button = None


        if self._undo_button != None:
            self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = None
        if self._redo_button != None:
            self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = None
        if self._bts_button != None:
            self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = None           
            
        if self._tempo_encoder_control != None:
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
            self._tempo_encoder_control = None
        if self._tempo_down_button != None:
            self._tempo_down_button.remove_value_listener(self._tempo_down_value)
            self._tempo_down_button = None
        if self._tempo_up_button != None:
            self._tempo_up_button.remove_value_listener(self._tempo_up_value)
            self._tempo_up_button = None            
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None             
        TransportComponentBase.disconnect(self)

    #PARENT FIX
        
    def set_arrangement_overdub_button(self, button):
        self.arrangement_overdub_toggle.set_toggle_button(button)
        
    def set_session_overdub_button(self, button):
        pass 
    
    @subject_slot('value')
    def _tempo_value(self, value):
        assert (self._tempo_control != None)
        assert (value in range(128))
        fraction = self.is_enabled() and (TEMPO_TOP - TEMPO_BOTTOM) / 127.0
        self.song().tempo = fraction * value + TEMPO_BOTTOM
        
    @subject_slot('value')
    def _song_position_value(self, value):
        assert (self._tempo_control != None)
        assert (value in range(128))
        self.song().current_song_time = max(0.0, value * SONG_TIME_MULT)

        #SHIFT, REDO, UNDO, BACK TO START
        
    def set_transport_shift_button(self, button):
        assert (isinstance(button, (ButtonElement, type(None))))
        assert (button.is_momentary())
        if self._shift_button != button:
            if self._shift_button != None:
                self._shift_button.remove_value_listener(self._shift_value)
                self._shift_pressed = False
            self._shift_button = button
            if (self._shift_button != None): 
                self._shift_button.add_value_listener(self._shift_value)        

    def set_undo_button(self, undo_button):
        assert (isinstance(undo_button, (ButtonElement, type(None))))
        if undo_button != self._undo_button:
            if self._undo_button != None:
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = undo_button
            if self._undo_button != None: 
                self._undo_button.add_value_listener(self._undo_value)
        self.update()

    def set_redo_button(self, redo_button):
        assert (isinstance(redo_button, (ButtonElement, type(None))))
        if redo_button != self._redo_button:
            if self._redo_button != None:
                self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = redo_button
            if self._redo_button != None: 
                self._redo_button.add_value_listener(self._redo_value)
        self.update()

    def set_bts_button(self, bts_button):
        assert (isinstance(bts_button, (ButtonElement, type(None))))
        if bts_button != self._bts_button:
            if self._bts_button != None:
                self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = bts_button
            if self._bts_button != None: 
                self._bts_button.add_value_listener(self._bts_value)
        self.update()

    def _undo_value(self, value):
        assert (self._undo_button != None)
        assert (value in range(128))
        if self.is_enabled() and self.song().can_undo and (value != 0 or not self._undo_button.is_momentary()):
            self.song().undo()
            
    def _shift_value(self, value):
        assert (self._shift_button != None)
        assert (value in range(128))
        self._shift_pressed = self.is_enabled() and value > 0            

    def _redo_value(self, value):
        assert (self._redo_button != None)
        assert (value in range(128))
        if self.is_enabled() and self.song().can_redo and (value != 0 or not self._undo_button.is_momentary()):
            self.song().redo()

    def _bts_value(self, value):
        assert (self._bts_button != None)
        assert (value in range(128))
        if self.is_enabled() and (value != 0 or not self._undo_button.is_momentary()):        
            self.song().current_song_time = 0.0

    def _ffwd_value(self, value):
        assert (self._ffwd_button != None)
        assert (value in range(128))
        if self._shift_pressed:
            self.song().current_song_time = self.song().last_event_time
        else:
            TransportComponentBase._ffwd_value(self, value)

    def _rwd_value(self, value):
        assert (self._rwd_value != None)
        assert (value in range(128))
        if self._shift_pressed:
            self.song().current_song_time = 0.0
        else:
            TransportComponentBase._rwd_value(self, value)
           
#     @rec_quantization_button.pressed
#     def rec_quantization_button(self, value):
#         if not self._last_quant_value != Live.Song.RecordingQuantization.rec_q_no_q:
#             raise AssertionError
#             quant_value = self.song().midi_recording_quantization
#             self._last_quant_value = quant_value != Live.Song.RecordingQuantization.rec_q_no_q and quant_value
#             self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
#         else:
#             self.song().midi_recording_quantization = self._last_quant_value
# 
#     @subject_slot('midi_recording_quantization')
#     def _on_quantization_changed(self):
#         if self.is_enabled():
#             self._update_quantization_state()
# 
#     def _update_quantization_state(self):
#         quant_value = self.song().midi_recording_quantization
#         quant_on = quant_value != Live.Song.RecordingQuantization.rec_q_no_q
#         if quant_on:
#             self._last_quant_value = quant_value
#         self.rec_quantization_button.color = 'DefaultButton.On' if quant_on else 'DefaultButton.Off'        
#         
#         #self._metronome_toggle.view_transform = lambda v: ('Metronome.On' if v else 'Metronome.Off')
                   
    #QUNEO
    
    def set_tempo_buttons(self, up_button, down_button):
        assert (isinstance(up_button, (ButtonElement, type(None))))        
        assert (isinstance(down_button, (ButtonElement, type(None))))        
        
        if self._tempo_up_button != None:
            self._tempo_up_button.remove_value_listener(self._tempo_up_value)
        self._tempo_up_button = up_button
        if self._tempo_up_button != None:
            self._tempo_up_button.add_value_listener(self._tempo_up_value)

        if( self._tempo_down_button != None):
            self._tempo_down_button.remove_value_listener(self._tempo_down_value)
        self._tempo_down_button = down_button
        if( self._tempo_down_button != None):
            self._tempo_down_button.add_value_listener(self._tempo_down_value)
    
        self.update()

    def set_tempo_encoder(self, control):
        assert (isinstance(control, (EncoderElement, type(None))))
        assert (control.message_map_mode() is Live.MidiMap.MapMode.relative1_two_compliment)
        
        if self._tempo_encoder_control != None:
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
        self._tempo_encoder_control = control
        if(self._tempo_encoder_control != None):
            self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
        
        self.update()
    
    def _tempo_up_value(self, value):
        assert (self._tempo_up_button != None)
        assert (value in range(128))
        if self.is_enabled():
            if value != 0:
                new_tempo =  1.0
                real_tempo = new_tempo + self.song().tempo
                if real_tempo < 20.0:
                    real_tempo =  20.0
                self.update_tempo(real_tempo)

    def _tempo_down_value(self, value):
        assert (self._tempo_down_button != None)
        assert (value in range(128))
        if self.is_enabled():
            if value != 0:
                new_tempo =  -1.0
                real_tempo = new_tempo + self.song().tempo
                if real_tempo > 200.0:
                    real_tempo =  200.0
                self.update_tempo(real_tempo)

    def _tempo_encoder_value(self, value):
        if not self._tempo_encoder_control != None:
            raise AssertionError
            raise value in range(128) or AssertionError
            backwards = value >= 64
            step = 0.1
            amount = backwards and value - 128
        else:
            amount = value
        tempo = max(20, min(999, self.song().tempo + amount * step))
        self.song().tempo = tempo

    def update_tempo(self, value):
        if value != None:
            new_tempo = value
            self.song().tempo = new_tempo

#LIVE Control
    def set_launch_quant_slider(self, slider):
        assert (isinstance(slider, (SliderElement, type(None))))
        if slider != self._launch_quant_slider:
           
            if self._launch_quant_slider != None:
                self._launch_quant_slider.remove_value_listener(self._launch_quant_value)
            self._launch_quant_slider = slider
            if self._launch_quant_slider != None: 
                self._launch_quant_slider.add_value_listener(self._launch_quant_value)
        
        self.update()

    def set_record_quant_slider(self, button):
        assert (isinstance(button, (SliderElement, type(None))))
        if button != self._record_quant_slider:
            
            if self._record_quant_slider != None:
                self._record_quant_slider.remove_value_listener(self._record_quant_value)
            self._record_quant_slider = button
            if self._record_quant_slider != None: 
                self._record_quant_slider.add_value_listener(self._record_quant_value)
        
        self.update()

    def set_follow_button(self, button):
        assert (isinstance(button, (ButtonElement, type(None))))
        if self._follow_button != button:
            
            if self._follow_button != None:
                self._follow_button.remove_value_listener(self._follow_value)
            self._follow_button = button
            if (self._follow_button != None): 
                self._follow_button.add_value_listener(self._follow_value)        

    def set_back_to_arranger_button(self, button):
        assert (isinstance(button, (ButtonElement, type(None))))
        if self._back_to_arranger_button != button:
            
            if self._back_to_arranger_button != None:
                self._back_to_arranger_button.remove_value_listener(self._back_to_arranger_value)
            self._back_to_arranger_button = button
            if (self._back_to_arranger_button != None): 
                self._back_to_arranger_button.add_value_listener(self._back_to_arranger_value)      

    def _launch_quant_value(self, value):
        assert (self._launch_quant_slider != None)
        assert (value in range(128))
        launch_quant_value  = value // 14   
        if self.is_enabled():
            self.song().clip_trigger_quantization = Live.Song.Quantization.values[launch_quant_value]

    def _record_quant_value(self, value):
        assert (self._record_quant_slider != None)
        assert (value in range(128))
        record_quant_value = value // 14         
        if self.is_enabled():
            self.song().midi_recording_quantization = Live.Song.RecordingQuantization.values[record_quant_value]
        
    def _follow_value(self, value):
        assert (self._follow_button != None)
        assert (value in range(128))        
        if self.is_enabled():
            if (not self._follow_button.is_momentary()) or (value != 0):
                self.song().view.follow_song = not self.song().view.follow_song

    def _back_to_arranger_value(self, value):
        assert (self._back_to_arranger_button != None)
        assert (value in range(128))          
        if self.is_enabled():
            if (not self._back_to_arranger_button.is_momentary()) or (value != 0):
                self.song().back_to_arranger = not self.song().back_to_arranger

    def _on_launch_quantisation_changed(self):
        if self.is_enabled():
            if self._launch_quant_slider is not None:
                self._launch_quant_slider.send_value(list(Live.Song.Quantization.values).index(self.song().clip_trigger_quantization)*15)
                
    def _on_record_quantisation_changed(self):
        if self.is_enabled():
            if self._record_quant_slider is not None:
                self._record_quant_slider.send_value(list(Live.Song.RecordingQuantization.values).index(self.song().midi_recording_quantization)*9)
                    
    def _on_follow_changed(self):
        if self.is_enabled():
            if self._follow_button is not None:
                self._follow_button.send_value(self.song().view.follow_song)

    def _on_back_to_arranger_changed(self):
        if self.is_enabled():
            if self._back_to_arranger_button is not None:
                self._back_to_arranger_button.send_value(self.song().back_to_arranger)

