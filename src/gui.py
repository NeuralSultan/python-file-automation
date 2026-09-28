import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from organizer import organize_files, get_category


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Python File Organizer")
        self.root.geometry("760x560")
        self.root.resizable(False, False)

        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 10)
        )

    def create_widgets(self):

        main_frame = ttk.Frame(
            self.root,
            padding=30
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        title = ttk.Label(
            main_frame,
            text="Python File Organizer",
            style="Title.TLabel"
        )
        title.pack(pady=(5, 5))

        subtitle = ttk.Label(
            main_frame,
            text="Organize your files automatically by type",
            style="Subtitle.TLabel"
        )
        subtitle.pack(pady=(0, 25))

        folder_section = ttk.Label(
            main_frame,
            text="Source Folder",
            style="Section.TLabel"
        )
        folder_section.pack(anchor="w")

        path_frame = ttk.Frame(main_frame)
        path_frame.pack(
            fill="x",
            pady=(8, 20)
        )

        self.path_entry = ttk.Entry(
            path_frame,
            font=("Segoe UI", 10)
        )
        self.path_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6
        )

        browse_button = ttk.Button(
            path_frame,
            text="Browse",
            command=self.browse_folder
        )
        browse_button.pack(
            side="left",
            padx=(10, 0),
            ipadx=10
        )

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        preview_button = ttk.Button(
            button_frame,
            text="Preview Changes",
            command=self.preview_files,
            style="Action.TButton"
        )
        preview_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        organize_button = ttk.Button(
            button_frame,
            text="Organize Files",
            command=self.organize_files,
            style="Action.TButton"
        )
        organize_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0)
        )

        result_section = ttk.Label(
            main_frame,
            text="Activity",
            style="Section.TLabel"
        )
        result_section.pack(anchor="w")

        text_frame = ttk.Frame(main_frame)
        text_frame.pack(
            fill="both",
            expand=True,
            pady=(8, 10)
        )

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical"
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.output_text = tk.Text(
            text_frame,
            height=12,
            font=("Consolas", 10),
            wrap="word",
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10
        )
        self.output_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.output_text.yview
        )

        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            style="Status.TLabel"
        )
        self.status_label.pack(
            anchor="w",
            pady=(5, 0)
        )

    def browse_folder(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if folder:

            self.path_entry.delete(
                0,
                tk.END
            )

            self.path_entry.insert(
                0,
                folder
            )

            self.set_status(
                "Folder selected."
            )

            self.clear_output()

    def get_folder(self):

        folder = self.path_entry.get().strip()

        if not folder:

            messagebox.showwarning(
                "No Folder Selected",
                "Please select a folder first."
            )

            return None

        return Path(folder)

    def preview_files(self):

        folder = self.get_folder()

        if folder is None:
            return

        if not folder.exists():
            messagebox.showerror(
                "Error",
                "The selected folder does not exist."
            )
            return

        self.clear_output()

        files_found = 0

        for file_path in folder.iterdir():

            if not file_path.is_file():
                continue

            category = get_category(file_path)

            self.output_text.insert(
                tk.END,
                f"{file_path.name}  →  {category}/\n"
            )

            files_found += 1

        if files_found == 0:

            self.output_text.insert(
                tk.END,
                "No files found in this folder."
            )

        self.set_status(
            f"Preview completed — {files_found} files found."
        )

    def organize_files(self):

        folder = self.get_folder()

        if folder is None:
            return

        if not folder.exists():
            messagebox.showerror(
                "Error",
                "The selected folder does not exist."
            )
            return

        confirmation = messagebox.askyesno(
            "Confirm Organization",
            "Are you sure you want to organize the files?"
        )

        if not confirmation:
            return

        try:

            self.clear_output()

            moved_files = organize_files(
                folder,
                dry_run=False
            )

            for file_path in moved_files:

                self.output_text.insert(
                    tk.END,
                    f"Moved → {file_path}\n"
                )

            count = len(moved_files)

            self.set_status(
                f"Completed — {count} files organized."
            )

            messagebox.showinfo(
                "Completed",
                f"{count} files organized successfully!"
            )

        except (
            FileNotFoundError,
            NotADirectoryError
        ) as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    def clear_output(self):

        self.output_text.delete(
            "1.0",
            tk.END
        )

    def set_status(self, message):

        self.status_label.config(
            text=message
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = FileOrganizerGUI(root)

    root.mainloop()