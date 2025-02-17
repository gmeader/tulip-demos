# messagebox example within a UIScreen LVGL v 9.0

import tulip
from ui import UIElement, UILabel, lv, lv_depad

# callback fires when a button on the msgbox is clicked 
def button_cb(evt):
    code = evt.get_code() # what type of event 
    if code == lv.EVENT.CLICKED:
        obj = evt.get_target_obj() # button obj that fired the event 
        child = obj.get_child(0) # get the label or image which is the first child of the button
        child_class=child.get_class()

        if child_class.name=='label': # it's a text button
            label_text = child.get_text()
        elif child_class.name == 'image': # it's an image button
            label_text = 'image'
        else:
            label_text = child_class.name

        event_label.set_text('Clicked: ' + label_text)
        print(label_text+' BUTTON')



class MsgBoxView(UIElement):
    def __init__(self, title, text, btns=["OK", "Cancel",''], **kwargs):
        super().__init__(**kwargs)

        self.msgbox = lv.msgbox(self.group) # Create a message box
        self.msgbox.add_title(title) # Add a title in title bar
        self.msgbox.add_text(text) # Add some text in "footer""

        # add buttons to msgbox
        self.header_button = self.msgbox.add_header_button(lv.SYMBOL.SETTINGS) # Add a symbol button to header
        self.ok_button = self.msgbox.add_footer_button('OK') # Add a button to "footer"
        self.cancel_button = self.msgbox.add_footer_button('Cancel') # Add a button to footer
        self.close_button = self.msgbox.add_close_button() # hides msgbox when clicked
        # add callbacks for buttons
        self.header_button.add_event_cb(button_cb,lv.EVENT.CLICKED, None) 
        self.ok_button.add_event_cb(button_cb,lv.EVENT.CLICKED, None) 
        self.cancel_button.add_event_cb(button_cb,lv.EVENT.CLICKED, None) 
        
        #self.msgbox.set_btn_default(0) # Set the default button
        self.msgbox.set_size(350,130) # width, height
        self.msgbox.center() # Show the message box

        self.container_style = lv.style_t() # style to color the msgbox container
        self.container_style.init()
        self.container_style.set_bg_color(lv.color_hex3(0x666))
        self.container_style.set_border_color(lv.color_hex3(0x338))
        self.container_style.set_border_width(2)

        self.button_style = lv.style_t() # style to color the buttons
        self.button_style.init()
        self.button_style.set_bg_color(lv.color_hex3(0xF00))

		# apply the styles for the buttons and for the container
        self.msgbox.add_style(self.button_style, lv.PART.ITEMS) # ITEMS is not correct thing to refer to the buttons
        self.msgbox.add_style(self.container_style, lv.PART.MAIN)


    

# label to display when msgbox closes    
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
event_label= EventLabel(text='EVENTS')

message_box = MsgBoxView(title='My Message Box',text='What do you want to do?' )

# start the app
def run(screen):
    screen.add(tulip.UILabel(text='Msgbox Demo', fg_color=tulip.color(255,127,0), font=tulip.lv.font_montserrat_24), pad_x=150,x=400, y=35)
    screen.add(event_label, x=250, y=270)
    screen.add(message_box, x=250, y=60, pad_x=300)
    screen.present()

