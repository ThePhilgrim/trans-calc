from pathlib import Path
import appdirs
import json
import tkinter
from tkinter import ttk
from typing import Dict, Any, TypedDict, Optional

ClientData = TypedDict("ClientData", {"full_rate": float, "currency": str, "matrix": Dict[str, float]})

# Main Window
class TransCalc:
    def __init__(self) -> None:
        self.client_dict = self.get_clients()
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("Trans-Calc")
        self.root.geometry("550x700")

        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        self.clients_label = ttk.Label(self.mainframe, text="Client", font=("TkDefaultFont", 14))
        self.clients_dropdown = ttk.Combobox(self.mainframe, state="readonly")

        if self.client_dict:
            self.update_client_dropdown()
        else:
            self.clients_dropdown["values"] = None

        self.clients_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_matrix_rows())

        self.button_frame = ttk.Frame(self.mainframe)

        self.add_client_button = ttk.Button(self.button_frame, command=self.add_new_client, text="Add Client")
        self.edit_client_button = ttk.Button(self.button_frame, command=self.edit_client, text="Edit Client")
        self.delete_client_button = ttk.Button(self.button_frame, command=self.delete_client, text="Delete Client")

        self.matrix_rows_frame = ttk.Frame(self.mainframe)
        self.matrix_stringvars = []
        self.matrix_entries = []

        self.full_price_sv = tkinter.StringVar()

        self.secondary_frame = ttk.Frame(self.mainframe)
        self.total_words_sv = tkinter.StringVar()
        self.total_word_label = ttk.Label(self.secondary_frame, text="Total words:")
        self.clear_button = ttk.Button(self.secondary_frame, command=self.clear_fields, text="Clear Fields")

        self.full_price_frame = ttk.Frame(self.mainframe)
        self.full_price_label = ttk.Label(self.full_price_frame, text="Full price:", font=("TkDefaultFont", 18))

        self.create_ui_grid()
        if self.client_dict:
            self.update_matrix_rows()

    def create_ui_grid(self) -> None:
        self.mainframe.columnconfigure(3)
        self.clients_label.grid(sticky="we", column=0, columnspan=1, padx=(23, 0), pady=(30, 0))

        self.clients_dropdown.grid(sticky="we", column=0, columnspan=1, padx=(20, 0), pady=(0, 20))
        self.button_frame.grid(sticky="we", column=0, columnspan=3, padx=(20, 20), pady=(0, 40))

        self.add_client_button.grid(column=0, row=0, padx=(5, 5))
        self.edit_client_button.grid(column=1, row=0, padx=(5, 5))
        self.delete_client_button.grid(column=2, row=0, padx=(5, 5))

    def update_matrix_rows(self) -> None:
        self.matrix_stringvars = []
        self.matrix_entries = []
        for row in self.matrix_rows_frame.grid_slaves():
            row.destroy()
        self.matrix_rows_frame.grid(column=0, columnspan=3)

        tm_match_label = ttk.Label(self.matrix_rows_frame, text="TM Match", font=("TkDefaultFont", 16))
        word_count_label = ttk.Label(self.matrix_rows_frame, text="Word Count", font=("TkDefaultFont", 16))
        match_discount_label = ttk.Label(self.matrix_rows_frame, text="Match Discount", font=("TkDefaultFont", 16))

        tm_match_label.grid(column=0, row=0, padx=(20, 30), pady=(0, 30))
        word_count_label.grid(column=1, row=0, padx=(0, 30), pady=(0, 30))
        match_discount_label.grid(sticky="e", column=2, row=0, padx=(0, 30), pady=(0, 30))

        try:
            for enum, matrix_row in enumerate(self.client_dict[self.clients_dropdown.get()]["matrix"], start=1):
                sv = tkinter.StringVar()
                # tkinter trace_add uses 3 useless arguments (*args)
                sv.trace_add("write", lambda *args: self.calculate_full_price())
                self.matrix_stringvars.append(sv)
                discount_current_row = str(
                    int(self.client_dict[self.clients_dropdown.get()]["matrix"][matrix_row] * 100)
                )
                if matrix_row[-1].isnumeric():
                    row_percentage_label = ttk.Label(self.matrix_rows_frame, text=matrix_row + "%")
                else:
                    row_percentage_label = ttk.Label(self.matrix_rows_frame, text=matrix_row)

                row_word_count_input = ttk.Entry(self.matrix_rows_frame, textvariable=sv, width=25)
                self.matrix_entries.append(row_word_count_input)

                row_match_discount_label = ttk.Label(
                    self.matrix_rows_frame, text=f"({discount_current_row}% of full rate)"
                )

                row_percentage_label.grid(sticky="nes", column=0, row=enum, padx=(0, 30), pady=(0, 20))
                row_word_count_input.grid(sticky="wn", column=1, row=enum, padx=(0, 30))
                row_match_discount_label.grid(sticky="nw", column=2, row=enum, padx=(0, 30))
        except KeyError:
            return

        self.secondary_frame.grid(sticky="we", column=0, columnspan=3)
        self.total_word_label.grid(column=0, row=0)
        self.clear_button.grid(padx=(200, 0))

        self.full_price_frame.grid(sticky="we", column=0, columnspan=4)
        self.full_price_label.grid(sticky="w", column=0, row=0, padx=(120, 0), pady=(40, 0))

        self.matrix_entries[0].focus_set()

    def add_new_client(self) -> None:
        add_client_window = tkinter.Toplevel()
        add_client_content = AddClientWindow(add_client_window, self.client_dict)
        add_client_content.mainframe.pack(fill="both", expand=True)
        add_client_window.transient(self.root)
        add_client_window.wait_window()
        self.update_client_dropdown()
        self.update_matrix_rows()

    def edit_client(self) -> None:
        if self.clients_dropdown.get() == None:
            return
        edit_client_window = tkinter.Toplevel()
        edit_client_content = EditClientWindow(edit_client_window, self.client_dict, self.clients_dropdown.get())
        edit_client_content.mainframe.pack(fill="both", expand=True)
        edit_client_window.transient(self.root)
        edit_client_window.wait_window()
        self.update_client_dropdown()
        self.update_matrix_rows()

    def delete_client(self) -> None:
        current_client = self.clients_dropdown.get()
        # TODO: show warning here
        del self.client_dict[current_client]
        save_client_data_to_json(self.client_dict)
        self.update_client_dropdown()
        self.update_matrix_rows()

    def get_clients(self) -> Optional[Dict[str, ClientData]]:
        config_dir = get_user_config_dir()
        try:
            with open(config_dir / "client-data.json", "r") as client_data:
                return json.load(client_data)["clients"]  # type: ignore
        except json.decoder.JSONDecodeError:
            return None
        except FileNotFoundError:
            return {}

    def update_client_dropdown(self):
        self.clients_dropdown["values"] = list(self.client_dict.keys())
        try:
            self.clients_dropdown.set(list(self.client_dict.keys())[0])
        except IndexError:
            self.clients_dropdown.set("")

    def calculate_full_price(self):
        client = self.client_dict[self.clients_dropdown.get()]

        tm_match_ranges = list(client["matrix"].keys())
        full_price = 0
        filled_in_entries = [stringvar for stringvar in self.matrix_stringvars if stringvar.get()]

        for entry in filled_in_entries:
            full_price += round(
                client["full_rate"]
                * client["matrix"][tm_match_ranges[self.matrix_stringvars.index(entry)]]
                * int(entry.get()),
                3,
            )

        if str(full_price).endswith(".0"):
            parsed_full_price = int(full_price)
        else:
            parsed_full_price = round(full_price, 2)

        self.full_price_sv.set(f'{client["currency"]} {str(parsed_full_price)}')
        calculated_full_price = ttk.Label(
            self.full_price_frame, textvariable=self.full_price_sv, font=("TkDefaultFont", 20)
        )
        calculated_full_price.grid(sticky="w", column=1, row=0, padx=(20, 0), pady=(40, 0))

        self.calculate_total_words()

    def calculate_total_words(self) -> None:
        total_words = 0
        for field in self.matrix_entries:
            if field.get():
                total_words += int(field.get())

        self.total_words_sv.set(total_words)
        calculated_total_words = ttk.Label(self.secondary_frame, textvariable=self.total_words_sv)
        calculated_total_words.grid(column=1, row=0)

    def clear_fields(self) -> None:
        for field in self.matrix_entries:
            field.delete(0, "end")

        self.matrix_entries[0].focus_set()


# Client Windows
class AddClientWindow:
    def __init__(self, window: tkinter.Toplevel, client_dict) -> None:
        self.window = window
        self.window.resizable(False, False)
        self.window.title("Add Client")
        self.window.geometry("400x700")
        self.client_dict = client_dict

        self.mainframe = ttk.Frame(self.window)

        self.header = ttk.Label(self.mainframe, text="Add Client", font=("TkDefaultFont", 18), justify="center")

        self.client_name_label = ttk.Label(self.mainframe, text="Client Name")
        self.client_name_entry = ttk.Entry(self.mainframe, width=25)

        self.client_currency_label = ttk.Label(self.mainframe, text="Currency")
        self.client_currency_entry = ttk.Entry(self.mainframe, width=8)
        self.client_currency_example = ttk.Label(self.mainframe, text='(ex. "EUR" or "USD")')

        self.client_full_rate_label = ttk.Label(self.mainframe, text="Full Rate\nper Word")
        self.client_full_rate_entry = ttk.Entry(self.mainframe, width=8)
        self.client_full_rate_example = ttk.Label(self.mainframe, text='(ex. "0.15")')

        self.tm_match_range_label = ttk.Label(self.mainframe, text="TM Match\nRanges")
        self.tm_match_discount_label = ttk.Label(self.mainframe, text="Discount\n(% of full price)")

        self.matrix_frame = ttk.Frame(self.mainframe)
        self.toast_message_frame = ttk.Frame(self.mainframe)

        self.save_client_button = ttk.Button(self.mainframe, command=self.save_client, text="Save Client")

        self.window.bind("<Return>", lambda e: self.save_client())

        self.create_ui_grid()

    def add_matrix_row(self) -> None:
        new_row_num = self.matrix_frame.grid_size()[1]
        if new_row_num >= 8:
            return
        new_row_tm_range = ttk.Entry(self.matrix_frame, width=8)
        new_row_tm_discount = ttk.Entry(self.matrix_frame, width=8)
        new_row_tm_range.grid(sticky="ne", column=1, row=new_row_num, padx=(0, 30), pady=(0, 5))
        new_row_tm_discount.grid(sticky="nw", column=2, row=new_row_num, padx=(0, 0), pady=(0, 5))

    def delete_matrix_row(self) -> None:
        pass

    def create_ui_grid(self) -> None:
        self.mainframe.rowconfigure(7, weight=1)
        self.header.grid(sticky="n", column=0, columnspan=3, padx=(0, 0), pady=(30, 30))
        self.client_name_label.grid(sticky="ne", column=0, row=1, padx=(10, 20), pady=(0, 20))
        self.client_name_entry.grid(sticky="nw", column=1, columnspan=2, row=1, padx=(0, 0), pady=(0, 20))
        self.client_currency_label.grid(sticky="ne", column=0, row=2, padx=(10, 20), pady=(0, 20))
        self.client_currency_entry.grid(sticky="nw", column=1, row=2, padx=(0, 0), pady=(0, 20))
        self.client_currency_example.grid(sticky="nw", column=2, row=2, padx=(0, 20), pady=(0, 20))
        self.client_full_rate_label.grid(sticky="ne", column=0, row=3, padx=(10, 20), pady=(0, 30))
        self.client_full_rate_entry.grid(sticky="nw", column=1, row=3, padx=(0, 0), pady=(0, 30))
        self.client_full_rate_example.grid(sticky="nw", column=2, row=3, padx=(0, 20), pady=(0, 30))

        self.tm_match_range_label.grid(sticky="nw", column=1, row=4, padx=(0, 50), pady=(0, 5))
        self.tm_match_discount_label.grid(sticky="nw", column=2, row=4, padx=(0, 0), pady=(0, 5))

        self.matrix_frame.grid(sticky="nw", column=1, columnspan=3, row=5, padx=(0, 0), pady=(0, 20))

        for i in range(8):
            tm_match_range = ttk.Entry(self.matrix_frame, width=8)
            tm_match_discount = ttk.Entry(self.matrix_frame, width=8)
            tm_match_range.grid(sticky="ne", column=1, row=i, padx=(0, 30), pady=(0, 5))
            tm_match_discount.grid(sticky="nw", column=2, row=i, padx=(0, 0), pady=(0, 5))

        self.toast_message_frame.grid(column=0, columnspan=3, row=7)

        self.save_client_button.grid(sticky="se", column=2, row=8, padx=(0, 0), pady=(0, 20))

        self.client_name_entry.focus()

    def save_client(self) -> None:
        # Not sure why grid_slaves is returned backwards. Had to use reversed()
        matrix_row_values = [value.get() for value in reversed(self.matrix_frame.grid_slaves()) if value.get()]

        ranges_and_discounts = {
            str(range): (int(discount) / 100)
            for range, discount in zip(matrix_row_values[::2], matrix_row_values[1::2])
        }

        client_name = self.client_name_entry.get()
        client_info = {
            "full_rate": float(self.client_full_rate_entry.get()),
            "currency": self.client_currency_entry.get(),
            "matrix": ranges_and_discounts,
        }
        self.client_dict[client_name] = client_info
        save_client_data_to_json(self.client_dict)
        self.clear_matrix_rows()
        self.display_success_message(client_name)

    def clear_matrix_rows(self):
        self.client_name_entry.delete(0, "end")
        self.client_name_entry.delete(0, "end")
        self.client_currency_entry.delete(0, "end")
        self.client_full_rate_entry.delete(0, "end")

        for value in self.matrix_frame.grid_slaves():
            value.delete(0, "end")

    def display_success_message(self, client_name):
        saved_success_label = ttk.Label(
            self.toast_message_frame,
            text=f"{client_name} was saved.",
            font=("TkDefaultFont", 16),
            style="Success.TLabel",
        )
        saved_success_label.tk.eval("ttk::style configure Success.TLabel -foreground green")
        saved_success_label.grid(sticky="se", column=0, row=0, padx=(0, 0), pady=(0, 0))


class EditClientWindow(AddClientWindow):
    def __init__(self, window, client_dict, currently_selected_client):
        super().__init__(window, client_dict)
        self.currently_selected_client = currently_selected_client
        self.window.title("Edit Client")
        self.header["text"] = "Edit Client"

        self.populate_data_fields()

    def populate_data_fields(self):
        self.client_name_entry.insert(0, self.currently_selected_client)
        self.client_currency_entry.insert(0, self.client_dict[self.currently_selected_client]["currency"])
        self.client_full_rate_entry.insert(0, self.client_dict[self.currently_selected_client]["full_rate"])

        range_discounts = [
            value for tuple in self.client_dict[self.currently_selected_client]["matrix"].items() for value in tuple
        ]

        matrix_entry_fields = [entry for entry in reversed(self.matrix_frame.grid_slaves())]

        for enum, value in enumerate(range_discounts):

            if isinstance(value, float):
                float_to_percentage = int(value * 100)
                matrix_entry_fields[enum].insert(0, float_to_percentage)
            else:
                matrix_entry_fields[enum].insert(0, value)


def get_user_config_dir():
    config_dir = Path(appdirs.user_config_dir("Trans-Calc", "ThePhilgrim"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def save_client_data_to_json(client_dict) -> None:
    config_dir = get_user_config_dir()
    client_data = {"clients": client_dict}
    try:
        with open(config_dir / "client-data.json", "w") as client_data_file:
            client_dict: Dict[Any] = json.dump(client_data, client_data_file, indent=4)
    except json.decoder.JSONDecodeError:
        return None


if __name__ == "__main__":
    transcalc = TransCalc()
    transcalc.root.mainloop()
