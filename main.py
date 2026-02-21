"""
GUI Designer - A visual tool to design Tkinter GUIs
Similar to Tkinter Designer, this tool helps speed up GUI development in Python
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import json
from typing import Dict, List, Any


class GUIDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Designer - Visual Tkinter Builder")
        self.root.geometry("1400x800")
        
        # Store all widgets created in the designer
        self.widgets: List[Dict[str, Any]] = []
        self.selected_widget = None
        self.widget_counter = 0
        
        # Live preview
        self.live_preview_window = None
        self.live_preview_enabled = False
        self.live_preview_widgets = {}  # Maps widget_id to tkinter widget
        
        # Resize handles
        self.resize_handles = []
        self.current_resize_handle = None
        self.resize_start_x = 0
        self.resize_start_y = 0
        
        # Setup UI
        self.setup_menu()
        self.setup_main_layout()
        
    def setup_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Generate menu
        generate_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Generate", menu=generate_menu)
        generate_menu.add_command(label="Generate Python Code", command=self.generate_code)
        generate_menu.add_command(label="Preview GUI", command=self.preview_gui)
        generate_menu.add_separator()
        generate_menu.add_command(label="Toggle Live Preview", command=self.toggle_live_preview)
        
    def setup_main_layout(self):
        """Create the main layout with three panels"""
        # Left panel - Widget Palette
        left_panel = ttk.Frame(self.root, width=200, relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        ttk.Label(left_panel, text="Widget Palette", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Widget buttons
        widgets_info = [
            ("Button", "button"),
            ("Label", "label"),
            ("Entry", "entry"),
            ("Text", "text"),
            ("Checkbutton", "checkbutton"),
            ("Radiobutton", "radiobutton"),
            ("Listbox", "listbox"),
            ("Combobox", "combobox"),
            ("Frame", "frame"),
            ("Canvas", "canvas"),
        ]
        
        for widget_name, widget_type in widgets_info:
            btn = ttk.Button(
                left_panel, 
                text=f"Add {widget_name}",
                command=lambda wt=widget_type, wn=widget_name: self.add_widget(wt, wn)
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Center panel - Design Canvas
        center_panel = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(center_panel, text="Design Canvas", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Canvas with scrollbars
        canvas_frame = ttk.Frame(center_panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(
            canvas_frame, 
            bg="white", 
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Grid overlay for easier placement
        self.canvas.bind("<Configure>", lambda e: self.draw_grid())
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.draw_grid()
        
        # Right panel - Properties
        right_panel = ttk.Frame(self.root, width=300, relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        right_panel.pack_propagate(False)
        
        ttk.Label(right_panel, text="Properties", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Properties container with scrollbar
        props_canvas = tk.Canvas(right_panel)
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=props_canvas.yview)
        self.props_frame = ttk.Frame(props_canvas)
        
        self.props_frame.bind(
            "<Configure>",
            lambda e: props_canvas.configure(scrollregion=props_canvas.bbox("all"))
        )
        
        props_canvas.create_window((0, 0), window=self.props_frame, anchor="nw")
        props_canvas.configure(yscrollcommand=scrollbar.set)
        
        props_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.show_empty_properties()
        
    def draw_grid(self):
        """Draw grid on canvas for alignment"""
        self.canvas.delete("grid")
        
        # Get actual canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # If canvas hasn't been drawn yet, use default size
        if width <= 1:
            width = 800
        if height <= 1:
            height = 600
        
        # Draw vertical lines
        for i in range(0, width + 20, 20):
            self.canvas.create_line(i, 0, i, height, fill="lightgray", tags="grid")
        
        # Draw horizontal lines
        for i in range(0, height + 20, 20):
            self.canvas.create_line(0, i, width, i, fill="lightgray", tags="grid")
        
        self.canvas.tag_lower("grid")
    
    def canvas_click(self, event):
        """Handle clicks on canvas background to deselect widgets"""
        # Check if click is on a widget or resize handle
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in items:
            tags = self.canvas.gettags(item)
            if "widget" in tags or "widget_text" in tags or "resize_handle" in tags:
                return  # Click is on a widget or handle, don't deselect
        
        # Click is on empty canvas, deselect
        if self.selected_widget:
            self.canvas.itemconfig(self.selected_widget["canvas_id"], outline="gray", width=1)
            self.selected_widget = None
            self.show_empty_properties()
    
    def add_widget(self, widget_type: str, widget_name: str):
        """Add a widget to the canvas"""
        self.widget_counter += 1
        widget_id = f"{widget_type}_{self.widget_counter}"
        
        # Default position
        x, y = 100 + (self.widget_counter * 10), 100 + (self.widget_counter * 10)
        
        # Larger default size for containers and canvas
        if widget_type in ["canvas", "frame", "text"]:
            default_width = 200
            default_height = 150
        else:
            default_width = 100
            default_height = 30
        
        # Create widget data
        widget_data = {
            "id": widget_id,
            "type": widget_type,
            "name": widget_name,
            "x": x,
            "y": y,
            "width": default_width,
            "height": default_height,
            "text": f"{widget_name} {self.widget_counter}",
            "bg": "SystemButtonFace" if widget_type != "canvas" else "white",
            "fg": "black",
            "font": ("Arial", 10),
            "canvas_id": None
        }
        
        self.widgets.append(widget_data)
        self.draw_widget(widget_data)
        self.select_widget(widget_data)
        self.update_live_preview()
        
    def draw_widget(self, widget_data: Dict[str, Any]):
        """Draw a widget representation on the canvas"""
        x, y = widget_data["x"], widget_data["y"]
        w, h = widget_data["width"], widget_data["height"]
        
        # Track if this is first draw (for event binding)
        is_first_draw = widget_data["canvas_id"] is None
        
        # Delete old canvas items if re-drawing (using tag to delete all items for this widget)
        if not is_first_draw:
            self.canvas.delete(widget_data["id"])
        
        # Draw rectangle
        rect_id = self.canvas.create_rectangle(
            x, y, x+w, y+h,
            fill=widget_data["bg"],
            outline="gray",
            tags=("widget", widget_data["id"])
        )
        
        # Draw text (show widget type for canvas/frame for clarity)
        display_text = widget_data["text"]
        if widget_data["type"] in ["canvas", "frame"]:
            display_text = f"[{widget_data['name']}]"
        
        text_id = self.canvas.create_text(
            x + w/2, y + h/2,
            text=display_text,
            fill=widget_data["fg"] if widget_data["type"] != "canvas" else "gray",
            font=widget_data["font"],
            tags=("widget_text", widget_data["id"])
        )
        
        widget_data["canvas_id"] = rect_id
        widget_data["text_id"] = text_id
        
        # Bind events only on first draw to avoid duplicate bindings
        if is_first_draw:
            self.canvas.tag_bind(widget_data["id"], "<ButtonPress-1>", 
                                lambda e, wd=widget_data: self.start_drag(e, wd))
            self.canvas.tag_bind(widget_data["id"], "<B1-Motion>", 
                                lambda e, wd=widget_data: self.do_drag(e, wd))
            self.canvas.tag_bind(widget_data["id"], "<ButtonRelease-1>", 
                                lambda e, wd=widget_data: self.end_drag(e, wd))
    
    def start_drag(self, event, widget_data: Dict[str, Any]):
        """Start dragging a widget"""
        self.select_widget(widget_data)
        # Store starting position for delta calculation
        widget_data["drag_last_x"] = event.x
        widget_data["drag_last_y"] = event.y
    
    def do_drag(self, event, widget_data: Dict[str, Any]):
        """Handle widget dragging"""
        if "drag_last_x" not in widget_data:
            return
        
        # Calculate movement since last event
        dx = event.x - widget_data["drag_last_x"]
        dy = event.y - widget_data["drag_last_y"]
        
        if dx != 0 or dy != 0:
            # Update stored position
            widget_data["drag_last_x"] = event.x
            widget_data["drag_last_y"] = event.y
            widget_data["x"] += dx
            widget_data["y"] += dy
            
            # Move canvas items smoothly (no snapping during drag)
            self.canvas.move(widget_data["id"], dx, dy)
            
            # Update live preview during drag for real-time feedback
            self.update_live_preview()
    
    def end_drag(self, event, widget_data: Dict[str, Any]):
        """End dragging - snap to grid"""
        # Clean up drag variables
        widget_data.pop("drag_last_x", None)
        widget_data.pop("drag_last_y", None)
        
        # Snap to grid
        widget_data["x"] = round(widget_data["x"] / 20) * 20
        widget_data["y"] = round(widget_data["y"] / 20) * 20
        
        # Redraw at snapped position
        self.draw_widget(widget_data)
        
        # Redraw resize handles if this is the selected widget
        if self.selected_widget == widget_data:
            self.clear_resize_handles()
            self.draw_resize_handles(widget_data)
            self.show_properties(widget_data)
        
        # Update live preview after drag completes
        self.update_live_preview()
    
    def select_widget(self, widget_data: Dict[str, Any]):
        """Select a widget and show its properties"""
        # Remove resize handles from previously selected widget
        self.clear_resize_handles()
        
        # Highlight selected widget
        if self.selected_widget:
            self.canvas.itemconfig(self.selected_widget["canvas_id"], outline="gray", width=1)
        
        self.selected_widget = widget_data
        self.canvas.itemconfig(widget_data["canvas_id"], outline="blue", width=2)
        
        # Draw resize handles
        self.draw_resize_handles(widget_data)
        
        self.show_properties(widget_data)
    
    def clear_resize_handles(self):
        """Remove all resize handles from canvas"""
        # Unbind events from all handle tags before deleting
        for handle_type in ["nw", "ne", "se", "sw", "n", "e", "s", "w"]:
            tag = f"handle_{handle_type}"
            self.canvas.tag_unbind(tag, "<Enter>")
            self.canvas.tag_unbind(tag, "<Leave>")
            self.canvas.tag_unbind(tag, "<ButtonPress-1>")
            self.canvas.tag_unbind(tag, "<B1-Motion>")
            self.canvas.tag_unbind(tag, "<ButtonRelease-1>")
        
        # Delete all handle rectangles
        for handle_id in self.resize_handles:
            self.canvas.delete(handle_id)
        self.resize_handles.clear()
    
    def draw_resize_handles(self, widget_data: Dict[str, Any]):
        """Draw resize handles on the corners and edges of the selected widget"""
        x, y = widget_data["x"], widget_data["y"]
        w, h = widget_data["width"], widget_data["height"]
        
        handle_size = 8  # Increased from 6 for easier clicking
        handle_color = "blue"
        
        # Define handle positions: (x_pos, y_pos, cursor, type)
        # Types: nw, n, ne, e, se, s, sw, w
        handles = [
            # Corners
            (x - handle_size//2, y - handle_size//2, "size_nw_se", "nw"),  # Top-left
            (x + w - handle_size//2, y - handle_size//2, "size_ne_sw", "ne"),  # Top-right
            (x + w - handle_size//2, y + h - handle_size//2, "size_nw_se", "se"),  # Bottom-right
            (x - handle_size//2, y + h - handle_size//2, "size_ne_sw", "sw"),  # Bottom-left
            # Edges
            (x + w//2 - handle_size//2, y - handle_size//2, "size_ns", "n"),  # Top
            (x + w - handle_size//2, y + h//2 - handle_size//2, "size_we", "e"),  # Right
            (x + w//2 - handle_size//2, y + h - handle_size//2, "size_ns", "s"),  # Bottom
            (x - handle_size//2, y + h//2 - handle_size//2, "size_we", "w"),  # Left
        ]
        
        # Track which tags we've already bound
        bound_tags = set()
        
        for hx, hy, cursor, handle_type in handles:
            handle_id = self.canvas.create_rectangle(
                hx, hy, hx + handle_size, hy + handle_size,
                fill=handle_color,
                outline="white",
                width=2,
                tags=("resize_handle", f"handle_{handle_type}")
            )
            self.resize_handles.append(handle_id)
            
            # Raise handle to top so it's clickable
            self.canvas.tag_raise(handle_id)
            
            # Bind events only once per unique tag
            tag = f"handle_{handle_type}"
            if tag not in bound_tags:
                bound_tags.add(tag)
                # Use lambda with default arguments to capture values correctly
                self.canvas.tag_bind(tag, "<Enter>", 
                                    lambda e, c=cursor: self.canvas.config(cursor=c))
                self.canvas.tag_bind(tag, "<Leave>", 
                                    lambda e: self.canvas.config(cursor=""))
                self.canvas.tag_bind(tag, "<ButtonPress-1>", 
                                    lambda e, ht=handle_type: self.start_resize(e, ht))
                self.canvas.tag_bind(tag, "<B1-Motion>", 
                                    lambda e, ht=handle_type: self.do_resize(e, ht))
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", 
                                    lambda e: self.end_resize(e))
    
    def update_resize_handle_positions(self, widget_data: Dict[str, Any]):
        """Update the positions of resize handles without recreating them"""
        x, y = widget_data["x"], widget_data["y"]
        w, h = widget_data["width"], widget_data["height"]
        handle_size = 8
        
        # Define new handle positions
        positions = {
            "nw": (x - handle_size//2, y - handle_size//2),
            "ne": (x + w - handle_size//2, y - handle_size//2),
            "se": (x + w - handle_size//2, y + h - handle_size//2),
            "sw": (x - handle_size//2, y + h - handle_size//2),
            "n": (x + w//2 - handle_size//2, y - handle_size//2),
            "e": (x + w - handle_size//2, y + h//2 - handle_size//2),
            "s": (x + w//2 - handle_size//2, y + h - handle_size//2),
            "w": (x - handle_size//2, y + h//2 - handle_size//2),
        }
        
        # Update each handle's position
        for handle_id in self.resize_handles:
            tags = self.canvas.gettags(handle_id)
            # Find the handle type from tags
            for tag in tags:
                if tag.startswith("handle_"):
                    handle_type = tag.replace("handle_", "")
                    if handle_type in positions:
                        hx, hy = positions[handle_type]
                        self.canvas.coords(handle_id, hx, hy, hx + handle_size, hy + handle_size)
                        break
    
    def start_resize(self, event, handle_type: str):
        """Start resizing a widget"""
        self.current_resize_handle = handle_type
        self.resize_start_x = event.x
        self.resize_start_y = event.y
        
        if self.selected_widget:
            self.selected_widget["resize_start_width"] = self.selected_widget["width"]
            self.selected_widget["resize_start_height"] = self.selected_widget["height"]
            self.selected_widget["resize_start_x"] = self.selected_widget["x"]
            self.selected_widget["resize_start_y"] = self.selected_widget["y"]
    
    def do_resize(self, event, handle_type: str):
        """Handle widget resizing"""
        if not self.selected_widget or not self.current_resize_handle:
            return
        
        dx = event.x - self.resize_start_x
        dy = event.y - self.resize_start_y
        
        widget = self.selected_widget
        start_w = widget.get("resize_start_width", widget["width"])
        start_h = widget.get("resize_start_height", widget["height"])
        start_x = widget.get("resize_start_x", widget["x"])
        start_y = widget.get("resize_start_y", widget["y"])
        
        # Calculate new dimensions based on handle type
        new_x = start_x
        new_y = start_y
        new_w = start_w
        new_h = start_h
        
        if handle_type == "se":  # Bottom-right
            new_w = max(20, start_w + dx)
            new_h = max(20, start_h + dy)
        elif handle_type == "sw":  # Bottom-left
            new_w = max(20, start_w - dx)
            new_h = max(20, start_h + dy)
            new_x = start_x + (start_w - new_w)
        elif handle_type == "ne":  # Top-right
            new_w = max(20, start_w + dx)
            new_h = max(20, start_h - dy)
            new_y = start_y + (start_h - new_h)
        elif handle_type == "nw":  # Top-left
            new_w = max(20, start_w - dx)
            new_h = max(20, start_h - dy)
            new_x = start_x + (start_w - new_w)
            new_y = start_y + (start_h - new_h)
        elif handle_type == "n":  # Top
            new_h = max(20, start_h - dy)
            new_y = start_y + (start_h - new_h)
        elif handle_type == "s":  # Bottom
            new_h = max(20, start_h + dy)
        elif handle_type == "e":  # Right
            new_w = max(20, start_w + dx)
        elif handle_type == "w":  # Left
            new_w = max(20, start_w - dx)
            new_x = start_x + (start_w - new_w)
        
        # Update widget data
        widget["x"] = new_x
        widget["y"] = new_y
        widget["width"] = new_w
        widget["height"] = new_h
        
        # Update canvas items directly without redrawing handles
        self.canvas.coords(widget["canvas_id"], new_x, new_y, new_x + new_w, new_y + new_h)
        self.canvas.coords(widget["text_id"], new_x + new_w/2, new_y + new_h/2)
        
        # Move resize handles to new positions
        self.update_resize_handle_positions(widget)
        
        # Update live preview
        self.update_live_preview()
    
    def end_resize(self, event):
        """End resizing - snap to grid"""
        if not self.selected_widget:
            return
        
        widget = self.selected_widget
        
        # Snap to grid
        widget["x"] = round(widget["x"] / 20) * 20
        widget["y"] = round(widget["y"] / 20) * 20
        widget["width"] = round(widget["width"] / 20) * 20
        widget["height"] = round(widget["height"] / 20) * 20
        
        # Ensure minimum size
        widget["width"] = max(20, widget["width"])
        widget["height"] = max(20, widget["height"])
        
        # Clean up resize tracking
        widget.pop("resize_start_width", None)
        widget.pop("resize_start_height", None)
        widget.pop("resize_start_x", None)
        widget.pop("resize_start_y", None)
        self.current_resize_handle = None
        
        # Redraw at snapped position
        self.draw_widget(widget)
        self.clear_resize_handles()
        self.draw_resize_handles(widget)
        
        # Update properties display and live preview
        self.show_properties(widget)
        self.update_live_preview()
        
    def show_empty_properties(self):
        """Show message when no widget is selected"""
        self.clear_resize_handles()
        
        for widget in self.props_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.props_frame, 
            text="No widget selected.\nClick on a widget to edit properties.",
            justify=tk.CENTER
        ).pack(pady=20)
        
    def show_properties(self, widget_data: Dict[str, Any]):
        """Display properties panel for selected widget"""
        # Clear existing properties
        for widget in self.props_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(
            self.props_frame, 
            text=f"{widget_data['name']} Properties",
            font=("Arial", 11, "bold")
        ).pack(pady=10)
        
        # Text property
        self.add_property_field("Text:", widget_data, "text")
        
        # Position properties
        self.add_property_field("X Position:", widget_data, "x", is_number=True)
        self.add_property_field("Y Position:", widget_data, "y", is_number=True)
        
        # Size properties
        self.add_property_field("Width:", widget_data, "width", is_number=True)
        self.add_property_field("Height:", widget_data, "height", is_number=True)
        
        # Color properties
        self.add_color_picker("Background:", widget_data, "bg")
        self.add_color_picker("Foreground:", widget_data, "fg")
        
        # Delete button
        ttk.Button(
            self.props_frame,
            text="Delete Widget",
            command=lambda: self.delete_widget(widget_data)
        ).pack(pady=20)
        
    def add_property_field(self, label: str, widget_data: Dict[str, Any], 
                          key: str, is_number: bool = False):
        """Add a property input field"""
        frame = ttk.Frame(self.props_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=str(widget_data[key]))
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        def update_property(*args):
            value = var.get()
            if is_number:
                try:
                    value = int(value)
                except ValueError:
                    return
            widget_data[key] = value
            self.draw_widget(widget_data)
            # Redraw resize handles if this is the selected widget
            if self.selected_widget == widget_data:
                self.clear_resize_handles()
                self.draw_resize_handles(widget_data)
            self.update_live_preview()
        
        var.trace("w", update_property)
        
    def add_color_picker(self, label: str, widget_data: Dict[str, Any], key: str):
        """Add a color picker button"""
        frame = ttk.Frame(self.props_frame)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
        
        def pick_color():
            color = colorchooser.askcolor(title=f"Choose {label}")[1]
            if color:
                widget_data[key] = color
                color_btn.config(text=color)
                self.draw_widget(widget_data)
                # Redraw resize handles if this is the selected widget
                if self.selected_widget == widget_data:
                    self.clear_resize_handles()
                    self.draw_resize_handles(widget_data)
                self.update_live_preview()
        
        color_btn = ttk.Button(
            frame, 
            text=widget_data[key],
            command=pick_color
        )
        color_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def update_properties_display(self):
        """Refresh the properties panel"""
        if self.selected_widget:
            self.show_properties(self.selected_widget)
    
    def delete_widget(self, widget_data: Dict[str, Any]):
        """Delete a widget from the canvas"""
        if messagebox.askyesno("Delete Widget", "Are you sure you want to delete this widget?"):
            self.canvas.delete(widget_data["id"])
            self.widgets.remove(widget_data)
            self.selected_widget = None
            self.show_empty_properties()
            self.update_live_preview()
    
    def new_project(self):
        """Clear all widgets and start fresh"""
        if messagebox.askyesno("New Project", "This will clear all widgets. Continue?"):
            for widget_data in self.widgets:
                self.canvas.delete(widget_data["id"])
            self.widgets.clear()
            self.widget_counter = 0
            self.selected_widget = None
            self.show_empty_properties()
            self.draw_grid()
            self.update_live_preview()
    
    def save_project(self):
        """Save project to JSON file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            # Prepare data for saving (remove canvas_id)
            save_data = []
            for widget in self.widgets:
                widget_copy = widget.copy()
                widget_copy.pop("canvas_id", None)
                save_data.append(widget_copy)
            
            with open(filename, "w") as f:
                json.dump(save_data, f, indent=2)
            messagebox.showinfo("Success", "Project saved successfully!")
    
    def load_project(self):
        """Load project from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, "r") as f:
                loaded_widgets = json.load(f)
            
            # Clear current project
            for widget_data in self.widgets:
                self.canvas.delete(widget_data["id"])
            self.widgets.clear()
            
            # Load widgets
            for widget_data in loaded_widgets:
                widget_data["canvas_id"] = None
                self.widgets.append(widget_data)
                self.draw_widget(widget_data)
            
            # Update counter
            if self.widgets:
                max_counter = max(
                    int(w["id"].split("_")[1]) for w in self.widgets
                )
                self.widget_counter = max_counter
            
            self.update_live_preview()
            messagebox.showinfo("Success", "Project loaded successfully!")
    
    def generate_code(self):
        """Generate Python/Tkinter code from the design"""
        code = self._generate_tkinter_code()
        
        # Show code in a new window
        code_window = tk.Toplevel(self.root)
        code_window.title("Generated Python Code")
        code_window.geometry("800x600")
        
        # Add text widget with scrollbar
        frame = ttk.Frame(code_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(frame, wrap=tk.NONE)
        scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=text_widget.xview)
        text_widget.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        text_widget.insert("1.0", code)
        
        # Add buttons
        btn_frame = ttk.Frame(code_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Copy to Clipboard",
            command=lambda: self._copy_to_clipboard(code)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Save to File",
            command=lambda: self._save_code_to_file(code)
        ).pack(side=tk.LEFT, padx=5)
        
    def _generate_tkinter_code(self) -> str:
        """Generate the actual Tkinter code"""
        code = '"""Generated by GUI Designer"""\n\n'
        code += 'import tkinter as tk\n'
        code += 'from tkinter import ttk\n\n\n'
        code += 'def create_gui():\n'
        code += '    root = tk.Tk()\n'
        code += '    root.title("Generated GUI")\n'
        code += '    root.geometry("800x600")\n\n'
        
        for widget in self.widgets:
            widget_type = widget["type"]
            widget_id = widget["id"].replace("-", "_")
            
            # Generate widget creation code
            if widget_type == "button":
                code += f'    {widget_id} = tk.Button(\n'
                code += f'        root,\n'
                code += f'        text="{widget["text"]}",\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}"\n'
                code += f'    )\n'
            elif widget_type == "label":
                code += f'    {widget_id} = tk.Label(\n'
                code += f'        root,\n'
                code += f'        text="{widget["text"]}",\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}"\n'
                code += f'    )\n'
            elif widget_type == "entry":
                code += f'    {widget_id} = tk.Entry(\n'
                code += f'        root,\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}"\n'
                code += f'    )\n'
            elif widget_type == "text":
                code += f'    {widget_id} = tk.Text(\n'
                code += f'        root,\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}",\n'
                code += f'        width={widget["width"]//10},\n'
                code += f'        height={widget["height"]//20}\n'
                code += f'    )\n'
            elif widget_type == "checkbutton":
                code += f'    {widget_id} = tk.Checkbutton(\n'
                code += f'        root,\n'
                code += f'        text="{widget["text"]}",\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}"\n'
                code += f'    )\n'
            elif widget_type == "radiobutton":
                code += f'    {widget_id} = tk.Radiobutton(\n'
                code += f'        root,\n'
                code += f'        text="{widget["text"]}",\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}"\n'
                code += f'    )\n'
            elif widget_type == "listbox":
                code += f'    {widget_id} = tk.Listbox(\n'
                code += f'        root,\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        fg="{widget["fg"]}"\n'
                code += f'    )\n'
            elif widget_type == "combobox":
                code += f'    {widget_id} = ttk.Combobox(root)\n'
            elif widget_type == "frame":
                code += f'    {widget_id} = tk.Frame(\n'
                code += f'        root,\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        width={widget["width"]},\n'
                code += f'        height={widget["height"]}\n'
                code += f'    )\n'
            elif widget_type == "canvas":
                code += f'    {widget_id} = tk.Canvas(\n'
                code += f'        root,\n'
                code += f'        bg="{widget["bg"]}",\n'
                code += f'        width={widget["width"]},\n'
                code += f'        height={widget["height"]}\n'
                code += f'    )\n'
            
            # Place widget
            code += f'    {widget_id}.place(\n'
            code += f'        x={widget["x"]},\n'
            code += f'        y={widget["y"]},\n'
            code += f'        width={widget["width"]},\n'
            code += f'        height={widget["height"]}\n'
            code += f'    )\n\n'
        
        code += '    root.mainloop()\n\n\n'
        code += 'if __name__ == "__main__":\n'
        code += '    create_gui()\n'
        
        return code
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "Code copied to clipboard!")
    
    def _save_code_to_file(self, code: str):
        """Save generated code to a Python file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, "w") as f:
                f.write(code)
            messagebox.showinfo("Success", f"Code saved to {filename}!")
    
    def preview_gui(self):
        """Preview the generated GUI"""
        # Create a new window with the designed GUI
        preview_window = tk.Toplevel(self.root)
        preview_window.title("GUI Preview")
        preview_window.geometry("800x600")
        
        # Create all widgets in the preview window
        for widget_data in self.widgets:
            widget_type = widget_data["type"]
            x, y = widget_data["x"], widget_data["y"]
            w, h = widget_data["width"], widget_data["height"]
            
            try:
                if widget_type == "button":
                    widget = tk.Button(
                        preview_window,
                        text=widget_data["text"],
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "label":
                    widget = tk.Label(
                        preview_window,
                        text=widget_data["text"],
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "entry":
                    widget = tk.Entry(
                        preview_window,
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "text":
                    widget = tk.Text(
                        preview_window,
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "checkbutton":
                    widget = tk.Checkbutton(
                        preview_window,
                        text=widget_data["text"],
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "radiobutton":
                    widget = tk.Radiobutton(
                        preview_window,
                        text=widget_data["text"],
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "listbox":
                    widget = tk.Listbox(
                        preview_window,
                        bg=widget_data["bg"],
                        fg=widget_data["fg"]
                    )
                elif widget_type == "combobox":
                    widget = ttk.Combobox(preview_window)
                elif widget_type == "frame":
                    widget = tk.Frame(
                        preview_window,
                        bg=widget_data["bg"],
                        width=w,
                        height=h
                    )
                elif widget_type == "canvas":
                    widget = tk.Canvas(
                        preview_window,
                        bg=widget_data["bg"],
                        width=w,
                        height=h
                    )
                else:
                    continue
                
                widget.place(x=x, y=y, width=w, height=h)
            except Exception as e:
                print(f"Error creating widget {widget_data['id']}: {e}")
    
    def toggle_live_preview(self):
        """Toggle the live preview window"""
        if self.live_preview_enabled:
            # Disable live preview
            self.live_preview_enabled = False
            if self.live_preview_window:
                self.live_preview_window.destroy()
                self.live_preview_window = None
                self.live_preview_widgets.clear()
        else:
            # Enable live preview
            self.live_preview_enabled = True
            self.create_live_preview_window()
            self.update_live_preview()
    
    def create_live_preview_window(self):
        """Create the live preview window"""
        if self.live_preview_window:
            return
        
        self.live_preview_window = tk.Toplevel(self.root)
        self.live_preview_window.title("Live Preview - TkForge")
        self.live_preview_window.geometry("800x600")
        
        # Handle window close
        self.live_preview_window.protocol("WM_DELETE_WINDOW", self.toggle_live_preview)
        
        # Add label at top
        info_label = tk.Label(
            self.live_preview_window,
            text="Live Preview - Updates in real-time",
            bg="lightblue",
            fg="black",
            font=("Arial", 10, "bold"),
            pady=5
        )
        info_label.pack(side=tk.TOP, fill=tk.X)
    
    def update_live_preview(self):
        """Update the live preview with current widgets"""
        if not self.live_preview_enabled or not self.live_preview_window:
            return
        
        try:
            # Clear existing preview widgets
            for widget in self.live_preview_widgets.values():
                try:
                    widget.destroy()
                except:
                    pass
            self.live_preview_widgets.clear()
            
            # Create all widgets in the preview
            for widget_data in self.widgets:
                widget_type = widget_data["type"]
                x, y = widget_data["x"], widget_data["y"]
                w, h = widget_data["width"], widget_data["height"]
                
                try:
                    if widget_type == "button":
                        widget = tk.Button(
                            self.live_preview_window,
                            text=widget_data["text"],
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "label":
                        widget = tk.Label(
                            self.live_preview_window,
                            text=widget_data["text"],
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "entry":
                        widget = tk.Entry(
                            self.live_preview_window,
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "text":
                        widget = tk.Text(
                            self.live_preview_window,
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "checkbutton":
                        widget = tk.Checkbutton(
                            self.live_preview_window,
                            text=widget_data["text"],
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "radiobutton":
                        widget = tk.Radiobutton(
                            self.live_preview_window,
                            text=widget_data["text"],
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "listbox":
                        widget = tk.Listbox(
                            self.live_preview_window,
                            bg=widget_data["bg"],
                            fg=widget_data["fg"]
                        )
                    elif widget_type == "combobox":
                        widget = ttk.Combobox(self.live_preview_window)
                    elif widget_type == "frame":
                        widget = tk.Frame(
                            self.live_preview_window,
                            bg=widget_data["bg"],
                            width=w,
                            height=h
                        )
                    elif widget_type == "canvas":
                        widget = tk.Canvas(
                            self.live_preview_window,
                            bg=widget_data["bg"],
                            width=w,
                            height=h
                        )
                    else:
                        continue
                    
                    widget.place(x=x, y=y, width=w, height=h)
                    self.live_preview_widgets[widget_data["id"]] = widget
                    
                except Exception as e:
                    print(f"Error creating preview widget {widget_data['id']}: {e}")
        except Exception as e:
            print(f"Error updating live preview: {e}")


def main():
    root = tk.Tk()
    app = GUIDesigner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
