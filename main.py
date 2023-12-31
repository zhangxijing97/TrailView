# Dependencies
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.list import ThreeLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

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

        # init the IconRightWidget
        saved_status = db.get_saved_status(self.pk)
        if saved_status:
            self.ids.icon_right_widget.icon = "bookmark"
        else:
            self.ids.icon_right_widget.icon = "bookmark-outline"

    def get_save_status(self):
        saved_status = db.get_saved_status(self.pk)
        return  saved_status

    def mark(self, check, the_list_item):
        '''mark the trail as saved or unsaved'''
        if check.active == True:
            the_list_item.text = the_list_item.text
            db.mark_trail_as_saved(the_list_item.pk)# here
        else:
            the_list_item.text = str(db.mark_trail_as_unsaved(the_list_item.pk))# Here

    def toggle_saved(self):
        if db.get_saved_status(self.pk):
            db.mark_trail_as_unsaved(self.pk)
        else:
            db.mark_trail_as_saved(self.pk)

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom left container'''

# Main App class
class MainApp(MDApp):
    trail_list_dialog = None

    def build(self):
        # Setting theme to my favorite theme
        self.title = "TrailView"
        self.theme_cls.primary_palette = "Green"
        self.active_filters = set()
        
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
        # Load the all trails and add them to the MDList widget when the application starts
        try:
            # Clear all existing trails from the container
            self.root.ids.container.clear_widgets()

            trails = db.get_trails()
            if trails != []:
                for trail in trails:

                    # for element in trail:
                    #     print(element)
                    trail_name = f"[size=36][b]{trail[1]}[/b][/size]"
                    add_trail = ListItem(pk=trail[0], text = trail_name, secondary_text = trail[2], tertiary_text = "Length: " + str(trail[5]) + "mi")
                    self.root.ids.container.add_widget(add_trail)

        except Exception as e:
            print(e)
            pass

    def load_saved_trails(self):
        # Load the saved trails only
        try:
            # Clear all existing trails from the container
            self.root.ids.container.clear_widgets()

            trails = db.get_saved_trails()
            if trails != []:
                for trail in trails:
                    add_trail = ListItem(pk=trail[0], text = trail[1], secondary_text = trail[2], tertiary_text = "Length: " + str(trail[5]) + "mi")
                    self.root.ids.container.add_widget(add_trail)

            self.saved_trails_loaded = True

        except Exception as e:
            print(e)
            pass

    def load_petFriendly_trails(self):
        # Load the saved trails only
        try:
            # Clear all existing trails from the container
            self.root.ids.container.clear_widgets()

            trails = db.get_petFriendly_trails()
            if trails != []:
                for trail in trails:
                    add_trail = ListItem(pk=trail[0], text = trail[1], secondary_text = trail[2], tertiary_text = "Length: " + str(trail[5]) + "mi")
                    self.root.ids.container.add_widget(add_trail)

            self.petFriendly_loaded = True

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

    def toggle_filter(self, filter_name):
        if filter_name in self.active_filters:
            self.active_filters.remove(filter_name)
        else:
            self.active_filters.add(filter_name)

        # Update the displayed trails based on active filters
        self.update_displayed_trails()

    def update_displayed_trails(self):
        # Construct the SQL query based on active filters
        query = "SELECT id, trail, location, latitude, longitude, length, difficulty, duration, isKidFriendly, isPetFriendly, saved FROM trails WHERE "
        conditions = []

        if "length_button_1" in self.active_filters:
            conditions.append("length <= 3")

        if "length_button_2" in self.active_filters:
            conditions.append("length > 3 AND length <= 8")

        if "length_button_3" in self.active_filters:
            conditions.append("length > 8")

        if "easy" in self.active_filters:
            conditions.append("difficulty = 'Easy'")

        if "moderate" in self.active_filters:
            conditions.append("difficulty = 'Moderate'")

        if "hard" in self.active_filters:
            conditions.append("difficulty = 'Hard'")

        if "duration_button_1" in self.active_filters:
            conditions.append("duration <= 60")

        if "duration_button_2" in self.active_filters:
            conditions.append("duration <= 180")

        if "duration_button_3" in self.active_filters:
            conditions.append("duration <= 360")

        if "kid_friendly" in self.active_filters:
            conditions.append("isKidFriendly = 1")

        if "pet_friendly" in self.active_filters:
            conditions.append("isPetFriendly = 1")

        if "saved" in self.active_filters:
            conditions.append("saved = 1")

        if conditions:
            query += " AND ".join(conditions)

        if "length_button_1" not in self.active_filters and "length_button_2" not in self.active_filters and "length_button_3" not in self.active_filters and "easy" not in self.active_filters and "moderate" not in self.active_filters and "hard" not in self.active_filters and "duration_button_1" not in self.active_filters and "duration_button_2" not in self.active_filters and "duration_button_3" not in self.active_filters and "kid_friendly" not in self.active_filters and "pet_friendly" not in self.active_filters and "saved" not in self.active_filters:
            query = "SELECT id, trail, location, latitude, longitude, length, difficulty, duration, isKidFriendly, isPetFriendly, saved FROM trails"

        try:
            # Clear all existing trails from the container
            self.root.ids.container.clear_widgets()

            trails = db.get_filter_trails(query)
            # trails = self.cursor.execute(query).fetchall()
            if trails:
                for trail in trails:
                    trail_name = f"[size=36][b]{trail[1]}[/b][/size]"
                    add_trail = ListItem(
                        pk=trail[0],
                        # text=trail[1],
                        text=trail_name,
                        secondary_text=trail[2],
                        tertiary_text="Length: " + str(trail[5]) + "mi",
                    )
                    self.root.ids.container.add_widget(add_trail)

        except Exception as e:
            print(e)
            pass

    def toggle_button_pressed(self, button):
        if button.icon == "circle":
            button.icon = "circle-outline"
        else:
            button.icon = "circle"

    # IconRightWidget
    def toggle_saved_button(self, button):
        if button.icon == "bookmark-outline":
            button.icon = "bookmark"
        else:
            button.icon = "bookmark-outline"

if __name__ == '__main__':
    app = MainApp()
    app.run()