import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from deep_translator import GoogleTranslator
import threading

# Color scheme
BG_COLOR = "#1a1a2e"
FG_COLOR = "#eaeaea"
ACCENT_COLOR = "#16c784"
BUTTON_COLOR = "#0f3460"
BUTTON_HOVER = "#533483"
HEADER_COLOR = "#0f3460"

def translate_text():
    try:
        source_text = entry_text.get("1.0", tk.END).strip()
        if not source_text:
            messagebox.showwarning("Empty Input", "Please enter text to translate!")
            return
        
        target_lang = lang_map[lang_combo.get()]
        
        # Disable button and show loading
        translate_btn.config(state=tk.DISABLED, text="Translating...")
        root.update()
        
        # Translation logic
        translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
        
        # Display output
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", translated)
        output_text.config(state=tk.DISABLED)
        
        status_label.config(text=f"✓ Translated to {lang_combo.get()}", fg=ACCENT_COLOR)
        translate_btn.config(state=tk.NORMAL, text="🌐 Translate")
    except Exception as e:
        status_label.config(text=f"✗ Error: {str(e)}", fg="#ff6b6b")
        translate_btn.config(state=tk.NORMAL, text="🌐 Translate")
        messagebox.showerror("Translation Error", f"Could not translate:\n{str(e)}")

def copy_output():
    try:
        output = output_text.get("1.0", tk.END).strip()
        if output:
            root.clipboard_clear()
            root.clipboard_append(output)
            messagebox.showinfo("Copied", "Translation copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Copy Error", str(e))

def clear_all():
    entry_text.config(state=tk.NORMAL)
    entry_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    status_label.config(text="Ready", fg=FG_COLOR)

# Mapping display names to language codes
lang_map = {
    "Spanish": "es", 
    "French": "fr", 
    "German": "de", 
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it"
}

# GUI Setup
root = tk.Tk()
root.title("🌐 CodeAlpha Language Translation Tool")
root.geometry("700x600")
root.config(bg=BG_COLOR)

# Header
header = tk.Frame(root, bg=HEADER_COLOR, pady=15)
header.pack(fill=tk.X)
tk.Label(header, text="🌐 Language Translation Tool", font=("Helvetica", 18, "bold"), 
         bg=HEADER_COLOR, fg=ACCENT_COLOR).pack()
tk.Label(header, text="Powered by Google Translate", font=("Helvetica", 10), 
         bg=HEADER_COLOR, fg=FG_COLOR).pack()

# Main content frame
main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=15)
main_frame.pack(fill=tk.BOTH, expand=True)

# Language selection
lang_frame = tk.LabelFrame(main_frame, text="Target Language", bg=BG_COLOR, fg=ACCENT_COLOR, 
                           font=("Helvetica", 10, "bold"), padx=10, pady=10)
lang_frame.pack(fill=tk.X, pady=10)
lang_combo = ttk.Combobox(lang_frame, values=list(lang_map.keys()), font=("Helvetica", 11), width=30)
lang_combo.current(0)
lang_combo.pack(fill=tk.X)

# Input text area
input_frame = tk.LabelFrame(main_frame, text="Source Text", bg=BG_COLOR, fg=ACCENT_COLOR,
                            font=("Helvetica", 10, "bold"), padx=10, pady=10)
input_frame.pack(fill=tk.BOTH, expand=True, pady=10)
entry_text = scrolledtext.ScrolledText(input_frame, height=6, bg="#2a2a3e", fg=FG_COLOR,
                                       font=("Helvetica", 10), insertbackground=FG_COLOR, wrap=tk.WORD)
entry_text.pack(fill=tk.BOTH, expand=True)
entry_text.insert("1.0", "Enter text to translate...")

# Output text area
output_frame = tk.LabelFrame(main_frame, text="Translation Result", bg=BG_COLOR, fg=ACCENT_COLOR,
                             font=("Helvetica", 10, "bold"), padx=10, pady=10)
output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
output_text = scrolledtext.ScrolledText(output_frame, height=6, bg="#2a2a3e", fg=ACCENT_COLOR,
                                        font=("Helvetica", 10), insertbackground=FG_COLOR, 
                                        wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True)

# Button frame
button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.pack(fill=tk.X, pady=15)

translate_btn = tk.Button(button_frame, text="🌐 Translate", command=translate_text,
                          bg=ACCENT_COLOR, fg="black", font=("Helvetica", 11, "bold"),
                          relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
translate_btn.pack(side=tk.LEFT, padx=5)

copy_btn = tk.Button(button_frame, text="📋 Copy", command=copy_output,
                     bg=BUTTON_COLOR, fg=FG_COLOR, font=("Helvetica", 10),
                     relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
copy_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(button_frame, text="🗑️ Clear", command=clear_all,
                      bg="#e74c3c", fg=FG_COLOR, font=("Helvetica", 10),
                      relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
clear_btn.pack(side=tk.LEFT, padx=5)

# Status bar
status_label = tk.Label(main_frame, text="Ready", font=("Helvetica", 9), 
                        fg=FG_COLOR, bg=BG_COLOR, justify=tk.LEFT)
status_label.pack(fill=tk.X, pady=5)

root.mainloop()
