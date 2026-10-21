
import json
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ---------- COLOURS ----------
BG = "#F3F7FC"
WHITE = "#FFFFFF"
NAVY = "#15345B"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
PALE_BLUE = "#EAF2FF"
TEXT = "#203047"
MUTED = "#64748B"
BORDER = "#D9E4F2"
GREEN = "#13805B"
MODEL = "gemini-2.5-flash"


# ---------- STORY GENERATION ----------
def basic_story(data, story_format, perspective):
    name = data["name"] or "The participant"
    role = data["role"] or "the programme"
    duration = data["duration"] or "Not specified"

    intro = (
        f"I participated in {role}."
        if perspective == "First person"
        else f"{name} participated in {role}."
    )

    activities = data["activities"] or "I took part in programme activities and learning."
    skills = data["skills"] or "I developed useful knowledge and practical skills."
    challenges = data["challenges"] or "I worked through challenges during the experience."
    achievements = data["achievements"] or "I completed the planned activities."
    reflection = data["reflection"] or "The experience gave me an opportunity to learn and grow."

    if perspective == "Third person":
        # Keep the participant's supplied wording rather than inventing
        # a rewritten version of their experience.
        pass

    if story_format == "Social Media Post":
        return (
            "✨ MY IMPACT STORY\n\n"
            f"{intro}\n\n"
            f"During {duration}, I explored new ideas and worked on practical activities.\n\n"
            f"🌱 WHAT I LEARNED\n{skills}\n\n"
            f"💡 CHALLENGES\n{challenges}\n\n"
            f"🏆 ACHIEVEMENTS\n{achievements}\n\n"
            f"💙 REFLECTION\n{reflection}\n\n"
            "#LearningJourney #ImpactStory"
        )

    if story_format == "Partner or Grant Report":
        return (
            "PARTICIPANT IMPACT SUMMARY\n\n"
            f"Participant: {name}\n"
            f"Programme: {role}\n"
            f"Duration: {duration}\n\n"
            f"ACTIVITIES AND LEARNING\n{activities}\n\n"
            f"SKILLS DEVELOPED\n{skills}\n\n"
            f"CHALLENGES\n{challenges}\n\n"
            f"ACHIEVEMENTS AND OUTCOMES\n{achievements}\n\n"
            f"PARTICIPANT REFLECTION\n{reflection}\n\n"
            "Review note: Check all statements and obtain approval before publication."
        )

    return (
        "MY IMPACT STORY\n\n"
        f"Introduction\n{intro}\n\n"
        f"Internship Duration\n{duration}\n\n"
        f"Activities and Learning\n{activities}\n\n"
        f"Skills and Knowledge Gained\n{skills}\n\n"
        f"Challenges\n{challenges}\n\n"
        f"Achievements\n{achievements}\n\n"
        f"Personal Reflection\n{reflection}\n\n"
        "Review note: Please check this draft for accuracy and obtain participant "
        "approval before sharing."
    )


def gemini_story(data, story_format, perspective, api_key):
    prompt = f"""
Create a clear and respectful participant impact story using ONLY the
information provided below. Do not invent facts, statistics or outcomes.
Use readable headings and natural language.
Format: {story_format}
Point of view: {perspective}
Participant: {data['name']}
Programme: {data['role']}
Duration: {data['duration']}
Activities: {data['activities']}
Skills gained: {data['skills']}
Challenges: {data['challenges']}
Achievements: {data['achievements']}
Reflection: {data['reflection']}
End with a brief reminder to review the story before publication.
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODEL}:generateContent?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 1400
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))

        candidates = result.get("candidates", [])
        if not candidates:
            raise RuntimeError("Gemini did not return a story.")

        parts = candidates[0].get("content", {}).get("parts", [])
        story = "\n".join(p.get("text", "") for p in parts).strip()

        if not story:
            raise RuntimeError("Gemini returned an empty response.")

        return story

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gemini API error {error.code}. Check your API key, "
            f"quota and model access.\n{details[:350]}"
        )
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to Gemini. Check your internet connection.\n{error}"
        )


# ---------- APPLICATION ----------
class ImpactStoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IAC Impact Story Generator")
        self.root.geometry("1120x820")
        self.root.minsize(800, 600)
        self.root.configure(bg=BG)

        self.entries = {}
        self.text_boxes = {}

        self.build_header()
        self.build_scrollable_page()

        self.root.bind("<Control-s>", lambda event: self.save_story())
        self.root.bind("<Control-Return>", lambda event: self.generate_story())

    def build_header(self):
        header = tk.Frame(self.root, bg=NAVY, height=95)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="✦", bg=BLUE, fg=WHITE,
            font=("Segoe UI", 24, "bold"), width=3
        ).pack(side="left", padx=(22, 14), pady=20)

        titles = tk.Frame(header, bg=NAVY)
        titles.pack(side="left", pady=18)

        tk.Label(
            titles, text="IAC Impact Story Generator",
            bg=NAVY, fg=WHITE, font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")

        tk.Label(
            titles, text="Turn participant experiences into meaningful stories",
            bg=NAVY, fg="#D7E6FF", font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(3, 0))

        tk.Label(
            header, text="GENERATIVE AI",
            bg="#25466F", fg="#D7E6FF",
            font=("Segoe UI", 9, "bold"), padx=12, pady=8
        ).pack(side="right", padx=22, pady=28)

    def build_scrollable_page(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            outer, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.page = tk.Frame(self.canvas, bg=BG)
        self.page_window = self.canvas.create_window(
            (0, 0), window=self.page, anchor="nw"
        )

        self.page.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.page_window, width=event.width
            )
        )
        self.canvas.bind_all("<MouseWheel>", self.mousewheel)

        tk.Label(
            self.page, text="Create an impact story",
            bg=BG, fg=TEXT, font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=26, pady=(22, 4))

        tk.Label(
            self.page,
            text="Add participant details, generate a story, review it and save.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", padx=26, pady=(0, 16))

        columns = tk.Frame(self.page, bg=BG)
        columns.pack(fill="both", expand=True, padx=26, pady=(0, 22))
        columns.grid_columnconfigure(0, weight=1, uniform="column")
        columns.grid_columnconfigure(1, weight=1, uniform="column")

        self.left = tk.Frame(columns, bg=BG)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 9))

        self.right = tk.Frame(columns, bg=BG)
        self.right.grid(row=0, column=1, sticky="nsew", padx=(9, 0))

        self.build_input_cards()
        self.build_output_cards()

        tk.Label(
            self.page,
            text="IAC Impact Story Generator  •  Review stories before publishing",
            bg=BG, fg=MUTED, font=("Segoe UI", 8)
        ).pack(pady=(0, 16))

    def card(self, parent, title, subtitle):
        frame = tk.Frame(
            parent, bg=WHITE, highlightthickness=1,
            highlightbackground=BORDER
        )
        frame.pack(fill="x", pady=(0, 14))

        tk.Label(
            frame, text=title, bg=WHITE, fg=NAVY,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=15, pady=(14, 3))

        tk.Label(
            frame, text=subtitle, bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8), wraplength=420, justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 7))

        return frame

    def add_entry(self, parent, label, hint):
        tk.Label(
            parent, text=label, bg=WHITE, fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=15, pady=(8, 4))

        entry = tk.Entry(
            parent, font=("Segoe UI", 10), bg="#F8FAFD", fg=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=BLUE,
            insertbackground=TEXT
        )
        entry.pack(fill="x", padx=15, ipady=9, pady=(0, 4))

        # Show a hint without treating it as actual participant data.
        entry.insert(0, hint)
        entry.configure(fg="#94A3B8")
        entry.bind(
            "<FocusIn>",
            lambda event, w=entry, h=hint: self.clear_entry_hint(w, h)
        )
        entry.bind(
            "<FocusOut>",
            lambda event, w=entry, h=hint: self.restore_entry_hint(w, h)
        )
        self.entries[label] = (entry, hint)

    def clear_entry_hint(self, widget, hint):
        if widget.get() == hint and widget.cget("fg") == "#94A3B8":
            widget.delete(0, "end")
            widget.configure(fg=TEXT)

    def restore_entry_hint(self, widget, hint):
        if not widget.get().strip():
            widget.insert(0, hint)
            widget.configure(fg="#94A3B8")

    def add_text(self, parent, label, hint, height=4):
        tk.Label(
            parent, text=label, bg=WHITE, fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=15, pady=(9, 4))

        box = tk.Frame(parent, bg=WHITE)
        box.pack(fill="x", padx=15, pady=(0, 4))

        widget = tk.Text(
            box, height=height, wrap="word", font=("Segoe UI", 9),
            bg="#F8FAFD", fg=TEXT, relief="flat", bd=0,
            padx=9, pady=8, insertbackground=TEXT,
            highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=BLUE
        )
        scroll = ttk.Scrollbar(
            box, orient="vertical", command=widget.yview
        )
        widget.configure(yscrollcommand=scroll.set)
        widget.pack(side="left", fill="x", expand=True)
        scroll.pack(side="right", fill="y")

        widget.insert("1.0", hint)
        widget.configure(fg="#94A3B8")
        widget.bind(
            "<FocusIn>",
            lambda event, w=widget, h=hint: self.clear_text_hint(w, h)
        )
        widget.bind(
            "<FocusOut>",
            lambda event, w=widget, h=hint: self.restore_text_hint(w, h)
        )
        self.text_boxes[label] = (widget, hint)

    def clear_text_hint(self, widget, hint):
        if (
            widget.get("1.0", "end-1c") == hint
            and widget.cget("fg") == "#94A3B8"
        ):
            widget.delete("1.0", "end")
            widget.configure(fg=TEXT)

    def restore_text_hint(self, widget, hint):
        if not widget.get("1.0", "end-1c").strip():
            widget.insert("1.0", hint)
            widget.configure(fg="#94A3B8")

    def build_input_cards(self):
        card = self.card(
            self.left, "01  Participant details",
            "Basic information about the participant"
        )
        self.add_entry(card, "Participant name", "e.g. Priya Sharma")
        self.add_entry(card, "Internship role or programme",
                       "e.g. Generative AI Internship")
        self.add_entry(card, "Duration", "e.g. 4 weeks")

        card = self.card(
            self.left, "02  Experience and learning",
            "Describe the participant's experience"
        )
        self.add_text(card, "Activities completed",
                      "Describe activities, tasks and learning.", 4)
        self.add_text(card, "Skills and knowledge gained",
                      "What skills or knowledge were gained?", 4)
        self.add_text(card, "Challenges faced",
                      "Describe challenges faced during the experience.", 3)

        card = self.card(
            self.left, "03  Outcomes and reflection",
            "Capture achievements and takeaways"
        )
        self.add_text(card, "Achievements or outcomes",
                      "What was completed or achieved?", 4)
        self.add_text(card, "Personal reflection",
                      "What did the participant learn?", 3)

    def build_output_cards(self):
        settings = self.card(
            self.right, "04  Story settings",
            "Choose the style for your story"
        )

        tk.Label(
            settings, text="STORY FORMAT", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=15, pady=(7, 4))

        self.format_var = tk.StringVar(value="Detailed Impact Story")
        ttk.Combobox(
            settings, textvariable=self.format_var, state="readonly",
            values=(
                "Detailed Impact Story",
                "Social Media Post",
                "Partner or Grant Report"
            )
        ).pack(fill="x", padx=15, pady=(0, 12))

        tk.Label(
            settings, text="POINT OF VIEW", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=15, pady=(0, 4))

        self.perspective_var = tk.StringVar(value="First person")
        ttk.Combobox(
            settings, textvariable=self.perspective_var, state="readonly",
            values=("First person", "Third person")
        ).pack(fill="x", padx=15, pady=(0, 12))

        tk.Label(
            settings, text="GEMINI API KEY (OPTIONAL)", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=15, pady=(0, 4))

        self.api_key = tk.StringVar()
        tk.Entry(
            settings, textvariable=self.api_key, show="*",
            font=("Segoe UI", 10), bg="#F8FAFD", fg=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=BLUE
        ).pack(fill="x", padx=15, ipady=9, pady=(0, 5))

        tk.Label(
            settings, text="Leave blank to use the basic fallback generator.",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 8), wraplength=350
        ).pack(anchor="w", padx=15, pady=(0, 12))

        self.make_button(
            settings, "✦  Generate Impact Story",
            self.generate_story, BLUE, WHITE
        )
        self.make_button(
            settings, "Use Basic Fallback",
            self.use_fallback, PALE_BLUE, BLUE_DARK
        )
        self.make_button(
            settings, "Clear Form",
            self.clear_form, "#F1F5F9", TEXT
        )

        self.status_frame = tk.Frame(
            self.right, bg=PALE_BLUE,
            highlightthickness=1, highlightbackground="#CFE0FF"
        )
        self.status_frame.pack(fill="x", pady=(0, 14))

        self.status = tk.Label(
            self.status_frame,
            text="Ready! Add details to create your story.",
            bg=PALE_BLUE, fg=BLUE_DARK, wraplength=430,
            justify="left", font=("Segoe UI", 9),
            padx=12, pady=11
        )
        self.status.pack(fill="x")

        preview = self.card(
            self.right, "05  Story preview",
            "Review and edit the generated story before saving"
        )

        toolbar = tk.Frame(preview, bg=WHITE)
        toolbar.pack(fill="x", padx=15, pady=(4, 8))

        tk.Label(
            toolbar, text="GENERATED OUTPUT", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        tk.Label(
            toolbar, text="EDITABLE", bg="#E7F8F0", fg=GREEN,
            font=("Segoe UI", 8, "bold"), padx=8, pady=4
        ).pack(side="right")

        story_frame = tk.Frame(preview, bg=WHITE)
        story_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))

        self.story = tk.Text(
            story_frame, height=24, wrap="word", undo=True,
            font=("Segoe UI", 10), bg="#F8FAFD", fg=TEXT,
            relief="flat", bd=0, padx=12, pady=12,
            insertbackground=TEXT, highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=BLUE
        )
        story_scroll = ttk.Scrollbar(
            story_frame, orient="vertical", command=self.story.yview
        )
        self.story.configure(yscrollcommand=story_scroll.set)
        self.story.pack(side="left", fill="both", expand=True)
        story_scroll.pack(side="right", fill="y")

        buttons = tk.Frame(preview, bg=WHITE)
        buttons.pack(fill="x", padx=15, pady=(0, 15))

        self.make_button(
            buttons, "↓  Save Story to File",
            self.save_story, NAVY, WHITE, side="left", expand=True
        )
        self.make_button(
            buttons, "Copy Story",
            self.copy_story, "#F1F5F9", TEXT, side="left"
        )

    def make_button(self, parent, label, command, bg, fg,
                    side="top", expand=False):
        button = tk.Button(
            parent, text=label, command=command,
            bg=bg, fg=fg, activebackground=BLUE_DARK if bg == BLUE else bg,
            activeforeground=WHITE if bg == BLUE else fg,
            font=("Segoe UI", 9, "bold"), relief="flat", bd=0,
            cursor="hand2", padx=12, pady=10
        )
        if side == "left":
            button.pack(
                side="left", fill="x" if expand else None,
                expand=expand, padx=(0, 7) if expand else (0, 0),
                pady=(0, 8)
            )
        else:
            button.pack(fill="x", padx=15, pady=(0, 8))
        return button

    def mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
        except tk.TclError:
            pass

    def collect_data(self):
        data = {}
        for label, (widget, hint) in self.entries.items():
            value = widget.get().strip()
            if value == hint and widget.cget("fg") == "#94A3B8":
                value = ""
            key = {
                "Participant name": "name",
                "Internship role or programme": "role",
                "Duration": "duration"
            }[label]
            data[key] = value

        for label, (widget, hint) in self.text_boxes.items():
            value = widget.get("1.0", "end-1c").strip()
            if value == hint and widget.cget("fg") == "#94A3B8":
                value = ""
            key = {
                "Activities completed": "activities",
                "Skills and knowledge gained": "skills",
                "Challenges faced": "challenges",
                "Achievements or outcomes": "achievements",
                "Personal reflection": "reflection"
            }[label]
            data[key] = value

        return data

    def set_status(self, message, mode="info"):
        colours = {
            "info": (PALE_BLUE, BLUE_DARK, "#CFE0FF"),
            "success": ("#E7F8F0", GREEN, "#B7E8D2"),
            "warning": ("#FFF7E6", "#925F00", "#F3D79B"),
            "error": ("#FFF0F0", "#B42318", "#F2C5C5")
        }
        bg, fg, border = colours[mode]
        self.status_frame.configure(bg=bg, highlightbackground=border)
        self.status.configure(bg=bg, fg=fg, text=message)

    def show_story(self, text):
        self.story.delete("1.0", "end")
        self.story.insert("1.0", text)
        self.story.see("1.0")

    def generate_story(self):
        data = self.collect_data()
        if not any(data.values()):
            messagebox.showinfo(
                "Participant details",
                "Please enter at least some participant information first."
            )
            return

        key = self.api_key.get().strip()
        if not key:
            self.use_fallback()
            return

        self.set_status("Connecting to Gemini...", "info")
        self.root.update_idletasks()

        try:
            result = gemini_story(
                data, self.format_var.get(),
                self.perspective_var.get(), key
            )
            self.show_story(result)
            self.set_status(
                "Story generated with Gemini. Review it before sharing.",
                "success"
            )
        except Exception as error:
            self.show_story(
                basic_story(data, self.format_var.get(),
                            self.perspective_var.get())
            )
            self.set_status(
                "Gemini was unavailable, so the basic fallback was used. "
                + str(error), "warning"
            )

    def use_fallback(self):
        data = self.collect_data()
        if not any(data.values()):
            messagebox.showinfo(
                "Participant details",
                "Please enter at least some participant information first."
            )
            return

        self.show_story(
            basic_story(data, self.format_var.get(),
                        self.perspective_var.get())
        )
        self.set_status(
            "Basic fallback generator used. No external AI service was called.",
            "warning"
        )

    def save_story(self):
        content = self.story.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showinfo("No story", "Generate or type a story first.")
            return

        path = filedialog.asksaveasfilename(
            title="Save Impact Story",
            defaultextension=".txt",
            initialfile="IAC_Impact_Story.txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            self.set_status("Story saved successfully.", "success")
            messagebox.showinfo("Saved", "Your story has been saved.")
        except OSError as error:
            messagebox.showerror("Save failed", str(error))

    def copy_story(self):
        content = self.story.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showinfo("No story", "Generate or type a story first.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.set_status("Story copied to clipboard.", "success")

    def clear_form(self):
        if not messagebox.askyesno(
            "Clear form",
            "Clear all participant details and the generated story?"
        ):
            return

        for widget, hint in self.entries.values():
            widget.delete(0, "end")
            widget.insert(0, hint)
            widget.configure(fg="#94A3B8")

        for widget, hint in self.text_boxes.values():
            widget.delete("1.0", "end")
            widget.insert("1.0", hint)
            widget.configure(fg="#94A3B8")

        self.story.delete("1.0", "end")
        self.api_key.set("")
        self.format_var.set("Detailed Impact Story")
        self.perspective_var.set("First person")
        self.set_status("Form cleared. Add details to begin again.", "info")


def main():
    root = tk.Tk()
    ImpactStoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
