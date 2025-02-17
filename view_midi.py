# view_MIDI displays incoming MIDI commands within a UIScreen LVGL v 9.0

import tulip, midi
from ui import UIElement, UILabel, lv, lv_depad

# label to display MIDI events - when MIDI commands are received     
class EventLabel(UIElement):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.label_obj = lv.label(self.group)
        self.label_obj.set_text(text)

        self.label_obj.set_height(25)
        # self.label_obj.set_width(150)
        # style the label
        self.label_style = lv.style_t()
        self.label_style.init()
        self.label_style.set_bg_color(lv.color_hex3(0xFFF)) # don't know why this does nothing?
        self.label_style.set_text_color(lv.color_hex3(0xFF0))
        self.label_style.set_border_color(lv.color_hex3(0x777))
        self.label_style.set_border_width(1)
        self.label_style.set_pad_top(2)
        self.label_style.set_pad_bottom(10)
        self.label_style.set_pad_right(6)
        self.label_style.set_pad_left(6)
        self.label_style.set_text_font(tulip.lv.font_montserrat_24)
        self.label_obj.add_style(self.label_style, lv.PART.MAIN)
        self.label_obj.set_width(700)

        
    def set_text(self, text):
        self.text = text
        self.label_obj.set_text(text)

# create the label as a global so we can change it from the callback                
event_label= EventLabel(text='EVENTS')

# MIDI receive
def midi_callback(midi_msg):
    cmd = midi_msg[0] >> 4
    channel = (midi_msg[0] & 0x0F) + 1

    if(cmd==9):
    	message = "Note on # %d velocity # %d channel: %d " % (midi_msg[1], midi_msg[2], channel)
        print(message)
        event_label.set_text(message)
    elif(cmd==8):
        message = "Note off # %d velocity # %d channel: %d " % (midi_msg[1], midi_msg[2],channel)
        print(message)
        event_label.set_text(message)
    elif(cmd == 14):
        message = "Pitchbend # %d # %d channel: %d " % (midi_msg[1], midi_msg[2],channel)
        print(message)
        event_label.set_text(message)
    elif(cmd == 11):
        message = "CC # %d value: %d channel: %d " % (midi_msg[1], midi_msg[2],channel)
        print(message)
        event_label.set_text(message)
    else:
        print(midi_msg,'CMD:',cmd,'CHAN:',channel)


# Stop the default MIDI callback that plays e.g. Juno notes, so we dont hear that 
#midi.stop_default_callback()

midi.add_callback(midi_callback)
midi.config.add_synth(channel=1, patch_number=256, num_voices=4) # switch to piano voice
# This gives error message: add_synth(patch_number=..) is deprecated and will be removed.  Use add_synth(PatchSynth(patch_number=..)) instead.
# Can't figure out how to use this newer function. Gives error: NameError: name 'PatchSynth' isn't defined.

# start the app
def run(screen):
    print("Listening on MIDI IN for messages...")
    screen.add(tulip.UILabel(text='MIDI View', fg_color=tulip.color(0,127,0), font=tulip.lv.font_montserrat_24), pad_x=150,x=400, y=35)
    screen.add(event_label, pad_x=800, x=90, y=80)
    screen.present()

    # Now play a MIDI note into Tulip. If you don't have a KB attached, use midi_local to send the message:
    print("Playing a sample note using midi_local()")
    tulip.midi_local((144, 40, 100))