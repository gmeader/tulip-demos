# demo of button matrix inside a UIScreen LVGL v 9.0

import tulip
from ui import UIElement, UILabel, lv, lv_depad

class ButtonMatrixView(UIElement):
    def __init__(self, map, callback, **kwargs):
        super().__init__(**kwargs)
        # map is a list of button names/labels
        self.map = map
        # style to color the buttons
        self.button_style = lv.style_t()
        self.button_style.init()
        self.button_style.set_bg_color(lv.color_hex3(0x044))
        # style to color the button matrix container
        self.container_style = lv.style_t()
        self.container_style.init()
        self.container_style.set_bg_color(lv.color_hex3(0x888))
        # create the buttonmatrix object
        self.bmatrix = lv.buttonmatrix(self.group)
        self.bmatrix.set_map(self.map)
        self.bmatrix.set_height(225)
        # set some attributes of the buttonmatrix
        self.bmatrix.set_button_ctrl_all(lv.buttonmatrix.CTRL.CHECKABLE) # make buttons toggle on/off
        self.bmatrix.set_one_checked(True) # only let one button be toggled on at a time
        # self.bmatrix.align(lv.ALIGN.CENTER,0,0) # maybe this is the default?
        self.bmatrix.add_event_cb(callback,lv.EVENT.ALL, None)
        # apply the styles for the buttons and for the container
        self.bmatrix.add_style(self.button_style, lv.PART.ITEMS)
        self.bmatrix.add_style(self.container_style, lv.PART.MAIN)

                                      
# callback fires when a button is clicked 
def bmatrix_cb(e):
    obj = e.get_target_obj() # obj that fired the event 
    code = e.get_code() # what type of event


    if code == lv.EVENT.VALUE_CHANGED:
        button_id = obj.get_selected_button()
        text = obj.get_button_text(button_id)
        print('Changed BUTTON:',button_id,'TEXT:',text)
        event_label.set_text('Clicked: ' + text)


# label to display events - when buttons are clicked     
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
        self.label_style.set_border_color(lv.color_hex3(0xF0F))
        self.label_style.set_border_width(1)
        self.label_style.set_pad_top(2)
        self.label_style.set_pad_bottom(10)
        self.label_style.set_pad_right(6)
        self.label_style.set_pad_left(6)
        self.label_obj.add_style(self.label_style, lv.PART.MAIN)
        
    def set_text(self, text):
        self.text = text
        self.label_obj.set_text(text)

# create the label as a global so we can change it from the callback                
event_label = EventLabel(text='EVENTS')

# start the app
def run(screen):
    button_map = ['1','2','3',"\n",
    			  '4','5','6',"\n",
                  '7','8','9',"\n",
                  '0','Action','']
    screen.add(tulip.UILabel(text='ButtonMatrix Demo', fg_color=tulip.color(255,127,0), font=tulip.lv.font_montserrat_24), pad_x=150,x=400, y=35)
    screen.add(ButtonMatrixView(button_map, bmatrix_cb), pad_x=150,x=20, y=20) # need to add pad_x or the container is clipped
    screen.add(event_label, x=90, y=270)
    screen.present()