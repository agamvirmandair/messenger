""" This module is responsible for the GUI"""
# AGAMVIR SINGH MANDAIR
# mandaira@uci.edu
# 40141643
import tkinter as tk
import pathlib
from tkinter import ttk, filedialog
from typing import Text
from ds_messenger import DirectMessenger
from typing import Text
from Profile import Profile
from ds_client import send


class Body(tk.Frame):
    """Main class for the application's body."""

    def __init__(self, root, recipient_selected_callback=None):
        """Initialize the application's body."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        """Handle node selection events."""
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Insert a new contact."""
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """Insert a new contact into the tree view."""
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        """Insert a new user message."""
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """Insert a new contact message."""
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Get the current text entry."""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Set the current text entry."""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Draw the application's body."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A custom Tkinter Frame class. It serves as the footer of an application.
    """
    def __init__(self, root, send_callback=None, pub_callback=None):
        """
        Initialize the frame.

        :param root: The parent window.
        :param send_callback: The function to call
        when the Send button is clicked.
        :param pub_callback: The function to call
        when the Publish button is clicked.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._pub_callback = pub_callback
        self._draw()

    def send_click(self):
        """
        Call the send callback function if it's not None.
        """
        if self._send_callback is not None:
            self._send_callback()

    def pub_click(self):
        """
        Call the publish callback function if it's not None.
        """
        if self._pub_callback is not None:
            self._pub_callback()

    def _draw(self):
        """
        Draw the frame's widgets.
        """
        save_button = tk.Button(master=self,
        text="Send", width=20, command=self.send_click)
        pub_button = tk.Button(master=self, text="Publ\
ish", width=20, command=self.pub_click)

        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        pub_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=15, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """
    A custom Tkinter Dialog for entering new contact information.
    """
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """
        Initialize the dialog.

        :param root: The parent window.
        :param title: The title of the dialog window.
        :param user: The default username.
        :param pwd: The default password.
        :param server: The default server address.
        """
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """
        Draw the body of the dialog.

        :param frame: The frame to draw in.
        """
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

    def apply(self):
        """
        Apply the entered data.
        """
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """
    A custom Tkinter Frame class. It serves as the main application.
    """
    def __init__(self, root):
        """
        Initialize the frame.

        :param root: The parent window.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = 'Agamvir'
        self.password = 'dedi'
        self.server = '168.235.86.101'
        self.recipient = ''
        self.configure_server()
        self.direct_messenger = DirectMessenger(self.server, 
                                            self.username, self.password)

        try:
            p = Profile()
            p.load_profile('user_data.dsu')
            self.profile = p
            self.path = str(pathlib.Path('user_data.dsu').resolve())
        except Exception:
            self.profile = Profile(self.server, self.username, self.password)
            with open('user_data.dsu','w') as f:
                pass
            self.path = str(pathlib.Path('user_data.dsu').resolve())
            self.profile.save_profile(self.path)

        self._draw()
        for x in self.profile.friends:
            self.body.insert_contact(x)
        self.check_new()

    def send_message(self):
        """
        Send a message to the recipient.
        """
        msg = self.body.get_text_entry()
        self.direct_messenger.send(msg,self.recipient)
        self.profile.add_message({'message': msg, 'fro\
m': self.username, 'to':self.recipient})
        self.profile.save_profile(self.path)
        self.body.insert_user_message(msg)
        self.body.message_editor.delete(1.0, tk.END)

    def add_contact(self):
        """
        Add a new contact to the profile.
        """
        friend = tk.simpledialog.askstring(title='Add Contact', prompt='Ple\
ase Enter username of Friend').strip()
        if friend not in self.profile.friends and friend!="":
            self.profile.add_friend(friend)
            self.profile.save_profile(self.path)
            self.body.insert_contact(friend)

    def recipient_selected(self, recipient):
        """
        Handle the event when a recipient is selected.

        :param recipient: The selected recipient.
        """
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        for m in self.profile.messages:
            if m['from'] == recipient and m['to'] == self.username:
                self.body.insert_contact_message(m['message'])
            elif m['from'] == self.username and m['to'] == recipient:
                self.body.insert_user_message(m['message'])

    def configure_server(self):
        """
        Configure the server settings.
        """
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = DirectMessenger(self.server, 
self.username, self.password)

    def publish(self):
        """
        Publish a message to the server.
        """
        message = self.body.get_text_entry()
        send(self.server, 3021, self.username, self.password, message)

    def check_new(self):
        """
        Check for new messages.
        """
        new = self.direct_messenger.retrieve_new()
        for x in new:
            if x.recipient not in self.profile.friends:
                self.profile.add_friend(x.recipient)
                self.body.insert_contact(x.recipient)
            self.profile.add_message({'message': x.message, 'fro\
m': x.recipient, 'to':self.username})
            self.body.insert_contact_message(x.message)
        self.profile.save_profile(self.path)
        self.root.after(2000, self.check_new)

    def _draw(self):
        """
        Draw the frame's widgets.
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message, 
                            pub_callback=self.publish)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def main():
    '''contains the main starting point of the program'''
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()

if __name__ == "__main__":
    main()
