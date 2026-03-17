import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import music21
import os
import threading
from ai_music_model import MusicAI

class MusicGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 AI Music Generator - CodeAlpha Project")
        self.root.geometry("600x700")
        self.root.configure(bg='#2C3E50')
        
        self.ai = MusicAI()
        self.is_training = False
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#34495E', pady=15)
        header_frame.pack(fill='x')
        tk.Label(
            header_frame, 
            text="🎵 AI Music Generator", 
            font=("Arial", 24, "bold"),
            bg='#34495E',
            fg='#ECF0F1'
        ).pack()
        tk.Label(
            header_frame,
            text="Powered by LSTM Neural Network",
            font=("Arial", 10),
            bg='#34495E',
            fg='#BDC3C7'
        ).pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#2C3E50', padx=20, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Status display
        status_frame = tk.LabelFrame(
            main_frame, 
            text="Status", 
            bg='#2C3E50', 
            fg='#ECF0F1',
            font=("Arial", 10, "bold")
        )
        status_frame.pack(fill='x', pady=10)
        
        self.status_text = tk.Text(
            status_frame, 
            height=5, 
            bg='#34495E', 
            fg='#ECF0F1',
            font=("Courier", 9)
        )
        self.status_text.pack(fill='x', padx=5, pady=5)
        self.log("Ready to generate music! 🎶")
        
        # Step 1: Data Preparation
        step1_frame = tk.LabelFrame(
            main_frame,
            text="Step 1: Prepare Training Data",
            bg='#2C3E50',
            fg='#ECF0F1',
            font=("Arial", 10, "bold")
        )
        step1_frame.pack(fill='x', pady=10)
        
        tk.Button(
            step1_frame,
            text="📝 Create Sample MIDI Files",
            command=self.create_sample,
            width=30,
            bg='#3498DB',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        ).pack(pady=5)
        
        tk.Button(
            step1_frame,
            text="📂 Import MIDI Files",
            command=self.import_midi,
            width=30,
            bg='#9B59B6',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        ).pack(pady=5)
        
        tk.Button(
            step1_frame,
            text="🎼 Extract Notes from MIDI",
            command=self.extract_notes,
            width=30,
            bg='#1ABC9C',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        ).pack(pady=5)
        
        # Step 2: Training
        step2_frame = tk.LabelFrame(
            main_frame,
            text="Step 2: Train AI Model",
            bg='#2C3E50',
            fg='#ECF0F1',
            font=("Arial", 10, "bold")
        )
        step2_frame.pack(fill='x', pady=10)
        
        # Training parameters
        param_frame = tk.Frame(step2_frame, bg='#2C3E50')
        param_frame.pack(pady=5)
        
        tk.Label(param_frame, text="Epochs:", bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=0, padx=5)
        self.epoch_entry = tk.Entry(param_frame, width=10)
        self.epoch_entry.insert(0, "50")
        self.epoch_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(param_frame, text="Batch Size:", bg='#2C3E50', fg='#ECF0F1').grid(row=0, column=2, padx=5)
        self.batch_entry = tk.Entry(param_frame, width=10)
        self.batch_entry.insert(0, "64")
        self.batch_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(param_frame, text="Sequence Length:", bg='#2C3E50', fg='#ECF0F1').grid(row=1, column=0, padx=5)
        self.sequence_entry = tk.Entry(param_frame, width=10)
        self.sequence_entry.insert(0, "100")
        self.sequence_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(param_frame, text="Output Length:", bg='#2C3E50', fg='#ECF0F1').grid(row=1, column=2, padx=5)
        self.output_length_entry = tk.Entry(param_frame, width=10)
        self.output_length_entry.insert(0, "200")
        self.output_length_entry.grid(row=1, column=3, padx=5)
        
        self.train_button = tk.Button(
            step2_frame,
            text="🚀 Train Model",
            command=self.train_model,
            width=30,
            bg='#E67E22',
            fg='white',
            font=("Arial", 10, "bold"),
            cursor='hand2'
        )
        self.train_button.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            step2_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=5)
        
        # Step 3: Generation
        step3_frame = tk.LabelFrame(
            main_frame,
            text="Step 3: Generate Music",
            bg='#2C3E50',
            fg='#ECF0F1',
            font=("Arial", 10, "bold")
        )
        step3_frame.pack(fill='x', pady=10)
        
        tk.Button(
            step3_frame,
            text="🎵 Generate AI Music",
            command=self.generate_music,
            width=30,
            bg='#27AE60',
            fg='white',
            font=("Arial", 12, "bold"),
            cursor='hand2',
            height=2
        ).pack(pady=10)
        
        # Model management
        model_frame = tk.Frame(step3_frame, bg='#2C3E50')
        model_frame.pack(pady=5)
        
        tk.Button(
            model_frame,
            text="💾 Save Model",
            command=self.save_model,
            width=14,
            bg='#16A085',
            fg='white',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            model_frame,
            text="📥 Load Model",
            command=self.load_model,
            width=14,
            bg='#8E44AD',
            fg='white',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            model_frame,
            text="📁 Open Output Folder",
            command=self.open_output_folder,
            width=14,
            bg='#2980B9',
            fg='white',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.update()
        
    def create_sample(self):
        """Create sample MIDI files for training"""
        try:
            self.log("Creating sample MIDI files...")
            if not os.path.exists('output'):
                os.makedirs('output')
            
            # Create multiple sample patterns
            patterns = [
                (['C4', 'E4', 'G4', 'C5', 'G4', 'E4'], 'sample_cmajor.mid'),
                (['D4', 'F#4', 'A4', 'D5', 'A4', 'F#4'], 'sample_dmajor.mid'),
                (['A3', 'C4', 'E4', 'A4', 'E4', 'C4'], 'sample_aminor.mid'),
                (['G3', 'B3', 'D4', 'G4', 'D4', 'B3'], 'sample_gmajor.mid'),
            ]
            
            for notes, filename in patterns:
                s = music21.stream.Stream()
                for p in notes:
                    s.append(music21.note.Note(p, quarterLength=1.0))
                s.write('midi', fp=f'output/{filename}')
            
            self.log(f"✅ Created {len(patterns)} sample MIDI files in 'output/' folder!")
            messagebox.showinfo("Success", f"Created {len(patterns)} sample MIDI files!")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def import_midi(self):
        """Import MIDI files for training"""
        try:
            files = filedialog.askopenfilenames(
                title="Select MIDI files",
                filetypes=[("MIDI files", "*.mid *.midi")]
            )
            
            if files:
                if not os.path.exists('output'):
                    os.makedirs('output')
                
                import shutil
                output_dir = os.path.abspath('output')
                for file in files:
                    try:
                        src = os.path.abspath(file)
                        dst = os.path.join(output_dir, os.path.basename(file))
                        if os.path.exists(dst) and os.path.samefile(src, dst):
                            continue
                        shutil.copy(src, output_dir)
                    except Exception as copy_error:
                        self.log(f"⚠️ Skipped {file}: {copy_error}")
                
                self.log(f"✅ Imported {len(files)} MIDI files!")
                messagebox.showinfo("Success", f"Imported {len(files)} MIDI files!")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def extract_notes(self):
        """Extract notes from MIDI files"""
        try:
            self.log("Extracting notes from MIDI files...")
            notes = self.ai.extract_notes_from_midi('output')
            unique_notes = len(set(notes))
            
            self.log(f"✅ Extracted {len(notes)} notes ({unique_notes} unique)!")
            messagebox.showinfo(
                "Success", 
                f"Extracted {len(notes)} notes!\nUnique notes: {unique_notes}"
            )
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def train_model(self):
        """Train the AI model"""
        if self.is_training:
            messagebox.showwarning("Training", "Model is already training!")
            return
        
        try:
            epochs = int(self.epoch_entry.get())
            batch_size = int(self.batch_entry.get())
            sequence_length = int(self.sequence_entry.get())
            
            self.is_training = True
            self.train_button.config(state='disabled', text="Training...")
            self.progress.start()
            
            # Run training in separate thread
            thread = threading.Thread(
                target=self._train_thread,
                args=(epochs, batch_size, sequence_length)
            )
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
            self.is_training = False
            self.train_button.config(state='normal', text="🚀 Train Model")
            self.progress.stop()
    
    def _train_thread(self, epochs, batch_size, sequence_length):
        """Training thread"""
        try:
            self.log(f"Preparing sequences (length={sequence_length})...")
            self.ai.prepare_sequences(sequence_length)
            
            self.log(f"Creating model...")
            self.ai.create_model(sequence_length)
            
            self.log(f"Training for {epochs} epochs with batch size {batch_size}...")
            self.ai.train(epochs=epochs, batch_size=batch_size)
            
            self.log("✅ Training complete!")
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Model trained successfully!\nEpochs: {epochs}"
            ))
        except Exception as e:
            self.log(f"❌ Training error: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.is_training = False
            self.root.after(0, lambda: self.train_button.config(
                state='normal',
                text="🚀 Train Model"
            ))
            self.root.after(0, self.progress.stop)
    
    def generate_music(self):
        """Generate music using trained model"""
        try:
            if self.ai.model is None:
                raise Exception("No trained model! Train or load a model first.")
            
            output_length = int(self.output_length_entry.get())
            
            self.log(f"Generating {output_length} notes...")
            generated_notes = self.ai.generate_notes(length=output_length)
            
            self.log("Creating MIDI file...")
            filename = self.ai.create_midi_from_notes(
                generated_notes,
                'output/ai_generated_music.mid'
            )
            
            self.log(f"✅ Music generated: {filename}")
            messagebox.showinfo(
                "Success",
                f"AI Music Generated!\n\nFile: {filename}\nNotes: {output_length}\n\nCheck the output folder!"
            )
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def save_model(self):
        """Save the trained model"""
        try:
            if self.ai.model is None:
                raise Exception("No model to save! Train a model first.")
            
            self.ai.save_model()
            self.log("✅ Model saved successfully!")
            messagebox.showinfo("Success", "Model saved to 'models/' folder!")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def load_model(self):
        """Load a trained model"""
        try:
            self.ai.load_model()
            self.log("✅ Model loaded successfully!")
            messagebox.showinfo("Success", "Model loaded from 'models/' folder!")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def open_output_folder(self):
        """Open the output folder"""
        try:
            import subprocess
            import platform
            
            if not os.path.exists('output'):
                os.makedirs('output')
            
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', 'output'])
            elif platform.system() == 'Windows':
                os.startfile('output')
            else:  # Linux
                subprocess.run(['xdg-open', 'output'])
            
            self.log("✅ Opened output folder!")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicGeneratorApp(root)
    root.mainloop()