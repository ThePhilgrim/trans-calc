import json
import tkinter
import math
from tkinter import ttk
from typing import Dict, Any


class TransCalcGui:
    def __init__(self) -> None:
        self.client_dict = self.get_clients()
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("Trans-Calc")
        self.root.geometry("550x700")

        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        self.header = ttk.Label(
            self.mainframe, text="Trans-Calc", font=("TkDefaultFont", 18), justify="center")

        self.clients_label = ttk.Label(
            self.mainframe, text="Client", font=("TkDefaultFont", 16))
        self.clients_dropdown = ttk.Combobox(
            self.mainframe, state="readonly")

        if self.client_dict:
            self.clients_dropdown["values"] = list(self.client_dict.keys())
        else:
            self.clients_dropdown["values"] = None

        if self.client_dict:
            self.clients_dropdown.set(list(self.client_dict.keys())[0])

        self.clients_dropdown.bind(
            "<<ComboboxSelected>>", self.create_matrix_rows)

        self.button_frame = ttk.Frame(self.mainframe)

        self.add_client_button = ttk.Button(
            self.button_frame, command=self.add_new_client, text="Add Client")
        self.edit_client_button = ttk.Button(
            self.button_frame, text="Edit Client")
        self.delete_client_button = ttk.Button(
            self.button_frame, text="Delete Client")

        self.matrix_rows_frame = ttk.Frame(self.mainframe)

        self.create_ui_grid()
        if self.client_dict:
            self.create_matrix_rows()

    def create_matrix_rows(self, event=None):
        self.matrix_rows_frame.grid(column=0, columnspan=3)

        tm_match_label = ttk.Label(
            self.matrix_rows_frame, text="TM Match", font=("TkDefaultFont", 16))
        word_count_label = ttk.Label(
            self.matrix_rows_frame, text="Word Count", font=("TkDefaultFont", 16))
        match_discount_label = ttk.Label(
            self.matrix_rows_frame, text="Match Discount", font=("TkDefaultFont", 16))

        tm_match_label.grid(column=0, row=0, padx=(20, 30), pady=(
            0, 30))
        word_count_label.grid(column=1, row=0, padx=(0, 30), pady=(
            0, 30))
        match_discount_label.grid(sticky="e", column=2, row=0, padx=(0, 30), pady=(
            0, 30))

        for enum, matrix_row in enumerate(self.client_dict[self.clients_dropdown.get()]["matrix"], start=1):
            discount_current_row = str(int(self.client_dict[self.clients_dropdown.get(
            )]["matrix"][matrix_row] * 100))
            row_percentage_label = ttk.Label(
                self.matrix_rows_frame, text=matrix_row + "%")
            row_word_count_input = ttk.Entry(self.matrix_rows_frame, width=25)
            row_match_discount_label = ttk.Label(
                self.matrix_rows_frame, text=f"({discount_current_row}% of full rate)")

            row_percentage_label.grid(
                sticky="nes", column=0, row=enum, padx=(0, 30), pady=(0, 20))
            row_word_count_input.grid(sticky="wn", column=1,
                                      row=enum, padx=(0, 30))
            row_match_discount_label.grid(sticky="nw", column=2,
                                          row=enum, padx=(0, 30))

    def create_ui_grid(self) -> None:
        self.mainframe.columnconfigure(3)
        self.header.grid(sticky="n", column=0, columnspan=3,
                         padx=(0, 0), pady=(30, 30))
        self.clients_label.grid(sticky="we", column=0, columnspan=1,
                                padx=(20, 0), pady=(30, 10))

        self.clients_dropdown.grid(sticky="we", column=0, columnspan=1,
                                   padx=(20, 0), pady=(0, 20))
        self.button_frame.grid(sticky="we", column=0, columnspan=3,
                               padx=(20, 20), pady=(0, 40))

        self.add_client_button.grid(column=0, row=0, padx=(5, 5))
        self.edit_client_button.grid(column=1, row=0, padx=(5, 5))
        self.delete_client_button.grid(column=2, row=0, padx=(5, 5))

    def add_new_client(self) -> None:
        add_client_window = tkinter.Toplevel()
        add_client_content = AddClient(add_client_window)
        add_client_content.mainframe.pack(fill="both", expand=True)

    def get_clients(self) -> Dict:
        try:
            with open("client-data.json", "r") as client_data:
                client_dict: Dict[Any] = json.load(client_data)["clients"]
            return client_dict
        except json.decoder.JSONDecodeError:
            print("JSON empty")
            return None


class AddClient:
    def __init__(self, add_client_window: tkinter.Toplevel) -> None:
        self.add_client_window = add_client_window
        self.add_client_window.resizable(False, False)
        self.add_client_window.title("Add Client")
        self.add_client_window.geometry("400x600")

        self.mainframe = ttk.Frame(self.add_client_window)

        self.header = ttk.Label(self.mainframe, text="Add Client",
                                font=("TkDefaultFont", 18))

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

        self.header.pack()
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
