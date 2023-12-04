# Dependencies
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

# To be added after creating the database
from database import Database
# Initialize db instance
db = Database()


class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TRAIL FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# After creating the database.py
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        '''mark the trail as complete or unsaved'''
        if check.active == True:
            # the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            the_list_item.text = the_list_item.text
            db.mark_trail_as_saved(the_list_item.pk)  # here
        else:
            the_list_item.text = str(db.mark_trail_as_unsaved(the_list_item.pk))  # Here

    def delete_item(self, the_list_item):
        '''Delete the trail'''
        self.parent.remove_widget(the_list_item)
        db.delete_trail(the_list_item.pk)  # Here

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''

# Main App class
class MainApp(MDApp):
    trail_list_dialog = None
    
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Teal"

    # Showing the trail dialog to add trails
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
            saved_trails, unsaved_trails = db.get_trails()

            if saved_trails != []:
                for trail in saved_trails:
                    add_trail = ListItemWithCheckbox(pk=trail[0], name=trail[1])
                    self.root.ids.container.add_widget(add_trail)

            if unsaved_trails != []:
                for trail in unsaved_trails:
                    add_trail = ListItemWithCheckbox(pk=trail[0], name=trail[1])
                    add_trail.ids.check.active = True
                    self.root.ids.container.add_widget(add_trail)

        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        self.trail_list_dialog.dismiss()

    def add_trail(self, trail):
        '''Add trail to the list of trails'''
        created_trail = db.create_trail(trail.text)

        # return the created trail details and create a list item
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk=created_trail[0], name='[b]'+created_trail[1]+'[/b]'))
        trail.text = ''

if __name__ == '__main__':
    app = MainApp()
    app.run()