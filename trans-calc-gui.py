import json
import tkinter
from tkinter import ttk
from typing import Dict, Any


class TransCalcGui:
    def __init__(self) -> None:
        self.client_dict = self.get_clients()
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("Trans-Calc")
        self.root.geometry("600x700")

        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        self.header = ttk.Label(
            self.mainframe, text="Welcome to Trans-Calc", font=("TkDefaultFont", 18))

        self.clients_label = ttk.Label(self.mainframe, text="Client")
        self.clients_dropdown = ttk.Combobox(
            self.mainframe, state="readonly")

        self.clients_dropdown["values"] = list(self.client_dict.keys())

        if self.client_dict:
            self.clients_dropdown.set(list(self.client_dict.keys())[0])

        self.button_frame = ttk.Frame(self.mainframe)

        self.add_client_button = ttk.Button(
            self.button_frame, command=self.add_new_client, text="Add Client")
        self.edit_client_button = ttk.Button(
            self.button_frame, text="Edit Client")
        self.delete_client_button = ttk.Button(
            self.button_frame, text="Delete Client")

        self.create_ui_grid()

    def create_ui_grid(self) -> None:
        self.mainframe.columnconfigure(3)
        self.header.grid(sticky="n", column=1, columnspan=1,
                         padx=(0, 0), pady=(30, 30))
        self.clients_label.grid(sticky="we", column=0, columnspan=1,
                                padx=(20, 0), pady=(30, 0))

        self.clients_dropdown.grid(sticky="we", column=0, columnspan=1,
                                   padx=(20, 0), pady=(0, 10))
        self.button_frame.grid(sticky="we", column=0, columnspan=3,
                               padx=(20, 20), pady=(0, 30))

        self.add_client_button.grid(column=0, row=0)
        self.edit_client_button.grid(column=1, row=0)
        self.delete_client_button.grid(column=2, row=0)

    def add_new_client(self) -> None:
        add_client_window = tkinter.Toplevel()
        add_client_content = AddClient(add_client_window)
        add_client_content.mainframe.pack(fill="both", expand=True)

    def get_clients(self) -> Dict:
        with open("client-data.json", "r") as client_data:
            client_dict: Dict[Any] = json.load(client_data)["clients"]
        return client_dict


class AddClient:
    def __init__(self, add_client_window: tkinter.Toplevel) -> None:
        self.add_client_window = add_client_window
        self.add_client_window.resizable(False, False)
        self.add_client_window.title("Add Client")
        self.add_client_window.geometry("400x600")

        self.mainframe = ttk.Frame(self.add_client_window)

        header = ttk.Label(self.mainframe, text="Add Client",
                           font=("TkDefaultFont", 18))
        header.pack()

        self.client_name_label = ttk.Label(self.mainframe, text="Client Name")
        self.client_name_entry = ttk.Entry(
            self.mainframe, width=25)

        self.client_currency_label = ttk.Label(
            self.mainframe, text="Currency")
        self.client_currency_entry = ttk.Entry(
            self.mainframe, width=10)

        self.tm_matches_label = ttk.Label(
            self.mainframe, text="TM Match Ranges & Discounts")
        self.matrix_row = ttk.Frame(self.mainframe)
        self.tm_match_range = ttk.Entry(self.matrix_row, width=20)
        self.tm_match_discount = ttk.Entry(self.matrix_row, width=5)

        self.add_row = ttk.Button(self.mainframe, text="Add Row")
        self.delete_row = ttk.Button(self.mainframe, text="Delete Row")

        self.client_name_label.pack()
        self.client_name_entry.pack()
        self.client_name_entry.focus()
        self.client_currency_label.pack()
        self.client_currency_entry.pack()
        self.tm_matches_label.pack()
        self.matrix_row.pack()
        self.tm_match_range.pack()
        self.tm_match_discount.pack()
        self.add_row.pack()
        self.delete_row.pack()


if __name__ == "__main__":
    transcalc_gui = TransCalcGui()
    transcalc_gui.root.mainloop()
