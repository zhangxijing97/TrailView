# Dependencies
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.list import ThreeLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.chip import MDChip

from kivymd.toast import toast

# To be added after creating the database
from database import Database
# Initialize db instance
db = Database()

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# After creating the database.py
class ListItem(ThreeLineAvatarIconListItem):
    '''Custom list item'''
    
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        '''mark the trail as saved or unsaved'''
        if check.active == True:
            the_list_item.text = the_list_item.text
            db.mark_trail_as_saved(the_list_item.pk)# here
        else:
            the_list_item.text = str(db.mark_trail_as_unsaved(the_list_item.pk))# Here

    def toggle_saved(self):
        # Toggle the saved attribute of the trail based on the checkbox value
        if db.get_saved_status(self.pk):
            db.mark_trail_as_unsaved(self.pk)
            self.icon = 'bookmark'
        else:
            db.mark_trail_as_saved(self.pk)
            self.icon = 'bookmark'

    def get_saved_status(self):
        saved_status = db.get_saved_status(self.pk)
        return 0

    # def delete_item(self, the_list_item):
    #     '''Delete the task'''
    #     self.parent.remove_widget(the_list_item)
    #     db.delete_trail(the_list_item.pk)# Here

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom left container'''

# Main App class
class MainApp(MDApp):
    trail_list_dialog = None
    def build(self):
        # Setting theme to my favorite theme
        self.title = "TrailView"
        self.theme_cls.primary_palette = "Green"
        
    # Showing the trail dialog to add tasks 
    def show_trail_dialog(self):
        if not self.trail_list_dialog:
            self.trail_list_dialog = MDDialog(
                title="Create Trail",
                type="custom",
                content_cls=DialogContent(),
            )

        self.trail_list_dialog.open()

    def on_start(self):
        # Load the saved trails and add them to the MDList widget when the application starts
        try:
            trails = db.get_trails()
            if trails != []:
                for trail in trails:
                    add_trail = ListItem(pk=trail[0], text = trail[1], secondary_text = trail[2], tertiary_text = "Length: " + str(trail[5]) + "mi")
                    self.root.ids.container.add_widget(add_trail)

        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        self.trail_list_dialog.dismiss()

    def add_trail(self, trail, location):
        '''Add task to the list of tasks'''
        # created_trail = db.create_trail(trail.text, location.text, latitude, longitude, length, difficulty, duration, isKidFriendly)
        created_trail = db.create_trail(trail.text, location.text)

        # return the created task details and create a list item
        self.root.ids['container'].add_widget(ListItem(pk=created_trail[0], text='[b]'+created_trail[1]+'[/b]'))
        trail.text = ''

    def callback(self, instance, value):
        toast(value)

if __name__ == '__main__':
    app = MainApp()
    app.run()