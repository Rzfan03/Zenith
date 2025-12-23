import os
import sys
import asyncio
import shutil
from datetime import datetime
from pathlib import Path
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DirectoryTree, TextArea, Label, Input, RichLog
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import work, on
from textual.events import Click, Key

# Ohhh you got a power super power...
# --- MODAL RANGER MANAGER (Fungsi Open Folder) ---
class FolderPickerModal(ModalScreen):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.current_dir = os.getcwd()

    def compose(self) -> ComposeResult:
        with Vertical(id="ranger-container"):
            # Header dinamis yang menunjukkan lokasi fokus saat ini
            yield Label(f" \uf07b  LOCATION: {self.current_dir}", id="ranger-header")
            with Horizontal(id="ranger-columns"):
                yield DirectoryTree(str(Path(self.current_dir).parent), id="parent-col", classes="ranger-col")
                # Kolom Utama
                yield DirectoryTree(self.current_dir, id="current-col", classes="ranger-col focus-area")
                # Area Preview dengan styling khusus
                yield Static("Preview...", id="preview-col", classes="ranger-col")
            yield Label(" [←] Back | [→] In | [Enter] SELECT FOLDER | [Esc] Cancel ", id="ranger-footer")

    def on_mount(self):
        self.query_one("#current-col").focus()

    # Fitur Baru: Highlight otomatis dan update header saat kursor bergerak
    @on(DirectoryTree.NodeHighlighted, "#current-col")
    def on_node_highlight(self, event):
        if event.node.data:
            path = event.node.data.path
            # Update Header agar user tahu folder apa yang sedang disorot
            self.query_one("#ranger-header").update(f" \uf07c  FOCUS: {path}")
            
            # Logika Preview
            if path.is_dir():
                try:
                    items = os.listdir(path)
                    preview_content = f"[b][yellow]\uf07b {path.name}[/yellow][/b]\n"
                    preview_content += "─" * 20 + "\n"
                    preview_content += "\n".join([f" \uf15b {i}" for i in items[:12]])
                    self.query_one("#preview-col").update(preview_content)
                except:
                    self.query_one("#preview-col").update("[red]Access Denied[/red]")
            else:
                self.query_one("#preview-col").update(f"[cyan]\uf15b File Selected[/cyan]\n{path.name}")

    def on_key(self, event: Key):
        current_tree = self.query_one("#current-col", DirectoryTree)
        if event.key == "left":
            parent_path = str(Path(self.current_dir).parent)
            if os.path.exists(parent_path): self.update_ranger_path(parent_path)
        elif event.key == "right":
            if current_tree.cursor_node and current_tree.cursor_node.data:
                path = current_tree.cursor_node.data.path
                if path.is_dir(): self.update_ranger_path(str(path))
        elif event.key == "enter":
            selected_path = self.current_dir
            if current_tree.cursor_node and current_tree.cursor_node.data:
                node_path = current_tree.cursor_node.data.path
                if node_path.is_dir(): selected_path = str(node_path)
            self.callback(selected_path)
            self.dismiss()

    def update_ranger_path(self, new_path):
        self.current_dir = new_path
        self.query_one("#ranger-header").update(f" \uf07b  LOCATION: {self.current_dir}")
        self.query_one("#parent-col").path = str(Path(new_path).parent)
        self.query_one("#current-col").path = new_path

# --- MODAL INPUT (New File & Rename) ---
class InputModal(ModalScreen):
    def __init__(self, message: str, callback, default_text: str = ""):
        super().__init__()
        self.message = message
        self.callback = callback
        self.default_text = default_text

    def compose(self) -> ComposeResult:
        with Vertical(id="modal-dialog"):
            yield Label(self.message)
            yield Input(value=self.default_text, id="modal-input")
            yield Label("Press [Enter] to Confirm | [Esc] to Cancel", id="modal-help")

    def on_mount(self):
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def handle_submit(self, event):
        self.callback(event.value)
        self.dismiss()

# --- ICON & TREE LOGIC ---
# --- MEGA ICON MAP ZENITH v8.9 ---
ICON_MAP = {
    # Programming Languages
    ".py": "\ue235", ".pyc": "\ue235", ".js": "\ue718", ".ts": "\ue628", 
    ".go": "\ue627", ".rs": "\ue7a8", ".cpp": "\ue61d", ".c": "\ue61e", 
    ".h": "\ue601", ".hpp": "\ue61d", ".java": "\ue256", ".kt": "\ue634",
    ".php": "\ue73d", ".rb": "\ue739", ".swift": "\ue755", ".dart": "\ue74b",
    ".lua": "\ue620", ".r": "\uf25d", ".zig": "\ue6a9", ".nim": "\ue677",
    ".scala": "\ue737", ".cs": "\uf031b",

    # Web Frameworks & Technologies
    ".html": "\ue736", ".css": "\ue749", ".scss": "\ue749", ".sass": "\ue749",
    ".less": "\ue758", ".jsx": "\ue7ba", ".tsx": "\ue7ba", ".vue": "\uf0844",
    ".svelte": "\ue697", ".astro": "\ue6b3", ".elm": "\ue62c",

    # Data & Config
    ".json": "\ue60b", ".yaml": "\ue601", ".yml": "\ue601", ".toml": "\ue601",
    ".xml": "\ue796", ".csv": "\uf1c3", ".sql": "\ue706", ".db": "\ue706",
    ".sqlite": "\ue706", ".env": "\uf462", ".ini": "\ue615", ".conf": "\ue615",

    # Documentation & Tools
    ".md": "\uf48a", ".txt": "\uf15c", ".pdf": "\uf1c1", ".dockerfile": "\ue7b0",
    ".dockerignore": "\ue7b0", ".gitignore": "\ue612", ".gitconfig": "\ue612",
    ".sh": "\ue795", ".bash": "\ue795", ".zsh": "\ue795", ".fish": "\ue795",
    ".powershell": "\ue70f", ".ps1": "\ue70f", ".make": "\ue615",

    # Archives & Binaries
    ".zip": "\uf410", ".tar": "\uf410", ".gz": "\uf410", ".rar": "\uf410",
    ".exe": "\ueae9", ".bin": "\ueae9", ".iso": "\uf0a15",

    # Images
    ".png": "\uf1c5", ".jpg": "\uf1c5", ".jpeg": "\uf1c5", ".gif": "\uf1c5",
    ".svg": "\uf082a", ".ico": "\uf1c5",
}

def get_icon(path_str: str, is_dir: bool, is_expanded: bool = False) -> str:
    if is_dir: return "\uf115" if is_expanded else "\uf07b"
    _, ext = os.path.splitext(path_str.lower())
    return ICON_MAP.get(ext, "\uf15b")

class ZenithTree(DirectoryTree):
    def render_label(self, node, base_style, style):
        node_label = node.label.copy()
        node_label.stylize(style)
        path_obj = getattr(node.data, 'path', None)
        path_str = str(path_obj) if path_obj else ""
        is_directory = path_obj.is_dir() if path_obj and hasattr(path_obj, 'is_dir') else False
        icon = get_icon(path_str, is_directory, node.is_expanded)
        return Text.assemble((f"{icon} ", "yellow" if is_directory else "cyan"), node_label)

# --- MAIN APP ---
class Zenith(App):
    TITLE = "Zenith IDE v8.8 Pro"
    CSS_PATH = "theme.css" 

    BINDINGS = [
        Binding("ctrl+o", "open_folder", "Open Folder"),
        Binding("ctrl+n", "new_file", "New File"),
        Binding("f2", "rename_file", "Rename"),
        Binding("ctrl+d", "delete_file", "Delete"),
        Binding("ctrl+s", "save_file", "Save"),
        Binding("ctrl+t", "toggle_terminal", "Terminal"),
        Binding("f5", "run_code", "Run"),
        Binding("ctrl+b", "toggle_sidebar", "Sidebar"),
        Binding("i", "enter_insert", "Insert", show=True),
        Binding("escape", "exit_insert", "Normal", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.current_file = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-container"):
            yield ZenithTree(os.getcwd(), id="sidebar")
            with Vertical(id="editor-container"):
                yield Static(" \uf413  Zenith Workspace", id="path-header")
                yield TextArea(id="editor", show_line_numbers=True, theme="dracula")
                with Horizontal(id="info-bar"):
                    yield Label(" \uf431  Lines: 0", id="stats-label")
                    yield Label("--:--:--", id="clock-label")
                yield Static(" \uf058  MODE: NORMAL ", id="status-bar")
                with Vertical(id="terminal-panel", classes="hidden"):
                    yield RichLog(id="terminal-output", highlight=True, markup=True)
                    yield Input(placeholder="➜ Terminal...", id="terminal-input")
        
        with Vertical(id="context-menu", classes="hidden"): 
            yield Label(" \uf044  [F2] Rename ", id="menu-rename")
            yield Label(" \uf1f8  [Del] Delete ", id="menu-delete")
            yield Label(" \uf00d  [Esc] Close ", id="menu-cancel")
        yield Footer()

    def on_mount(self):
        self.editor = self.query_one("#editor", TextArea)
        self.editor.read_only = True
        self.set_interval(1, self.update_clock)

    def update_clock(self):
        self.query_one("#clock-label").update(f"\uf017  {datetime.now().strftime('%H:%M:%S')}")

    @on(DirectoryTree.FileSelected, "#sidebar")
    def handle_file(self, event: DirectoryTree.FileSelected):
        if event.path.is_file():
            self.load_path(str(event.path))

    def load_path(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.current_file = path
            ext = os.path.splitext(path)[1].lower()
            langs = {'.py': 'python', '.go': 'go', '.js': 'javascript', '.rs': 'rust', '.md': 'markdown'}
            self.editor.text = content
            self.editor.language = langs.get(ext)
            self.query_one("#path-header").update(f" \uf15b  {os.path.basename(path)}")
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")

    def action_open_folder(self):
        def do_open(path):
            os.chdir(path)
            sidebar = self.query_one("#sidebar", ZenithTree)
            sidebar.path = path
            sidebar.reload()
            self.notify(f"Switched to: {path}")
        self.push_screen(FolderPickerModal(do_open))

    def action_new_file(self):
        def do_create(name):
            if name:
                path = os.path.join(os.getcwd(), name)
                with open(path, "w") as f: f.write("")
                self.query_one("#sidebar").reload()
                self.load_path(path)
        self.push_screen(InputModal("New File Name:", do_create))

    def action_rename_file(self):
        sidebar = self.query_one("#sidebar", ZenithTree)
        if not sidebar.cursor_node or not sidebar.cursor_node.data: return
        old_path = str(sidebar.cursor_node.data.path)
        def do_rename(new_name):
            if new_name:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                sidebar.reload()
                self.notify(f"Renamed to {new_name}")
        self.push_screen(InputModal("Rename to:", do_rename, os.path.basename(old_path)))

    def action_delete_file(self):
        sidebar = self.query_one("#sidebar", ZenithTree)
        if not sidebar.cursor_node or not sidebar.cursor_node.data: return
        path = str(sidebar.cursor_node.data.path)
        try:
            if os.path.isdir(path): shutil.rmtree(path)
            else: os.remove(path)
            sidebar.reload()
            self.notify(f"Deleted: {os.path.basename(path)}")
        except Exception as e: self.notify(f"Error: {e}", severity="error")

    def action_save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.text)
            self.notify("File Saved!")

    def action_toggle_terminal(self):
        t = self.query_one("#terminal-panel")
        t.toggle_class("hidden")
        if not t.has_class("hidden"): self.query_one("#terminal-input").focus()

    @on(Input.Submitted, "#terminal-input")
    def terminal_command(self, event: Input.Submitted):
        cmd = event.value.strip()
        if cmd: self.execute_cmd(cmd)
        event.input.value = ""

    @work(exclusive=False)
    async def execute_cmd(self, cmd: str):
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stdout: self.query_one("#terminal-output", RichLog).write(stdout.decode())
        if stderr: self.query_one("#terminal-output", RichLog).write(f"[red]{stderr.decode()}[/]")

    def action_enter_insert(self):
        self.editor.read_only = False
        self.query_one("#status-bar").update(" \uf040  MODE: INSERT ")
        self.editor.focus()

    def action_exit_insert(self):
        self.editor.read_only = True
        self.query_one("#status-bar").update(" \uf058  MODE: NORMAL ")

    def action_toggle_sidebar(self):
        self.query_one("#sidebar").toggle_class("hidden")

if __name__ == "__main__":
    Zenith().run()