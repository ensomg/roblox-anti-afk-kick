import customtkinter as ctk
import pydirectinput
import threading
import time
import random

ctk.set_appearance_mode("dark")

class FullscreenSplash(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Make fullscreen and borderless
        self.overrideredirect(True)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.configure(fg_color="black")
        self.attributes("-topmost", True)
        
        # Start completely invisible
        self.attributes("-alpha", 0.0) 
        
        self.center_frame = ctk.CTkFrame(self, fg_color="black")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # ENSOMG Text
        self.title_text = "ENSOMG"
        self.current_text = ""
        self.title_label = ctk.CTkLabel(self.center_frame, text="", 
                                        font=ctk.CTkFont(family="Courier", size=80, weight="bold"), 
                                        text_color="white")
        self.title_label.pack(pady=(0, 20))
        
        # Loading Bar
        self.progress_bar = ctk.CTkProgressBar(self.center_frame, width=300, height=8, 
                                               progress_color="white", fg_color="#222")
        self.progress_bar.pack()
        self.progress_bar.set(0)

        # Start animation sequence
        self.fade_in()

    def fade_in(self, alpha=0.0):
        # Smooth fade-in
        alpha += 0.05
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(20, lambda: self.fade_in(alpha))
        else:
            self.typewriter_text()

    def typewriter_text(self, index=0):
        # Typing out ENSOMG with glitchy delay
        if index < len(self.title_text):
            self.current_text += self.title_text[index]
            self.title_label.configure(text=self.current_text)
            self.after(random.randint(100, 300), lambda: self.typewriter_text(index + 1))
        else:
            self.progress = 0
            self.load_bar()

    def load_bar(self):
        # Fill Loading Bar
        if self.progress < 1.0:
            self.progress += 0.02
            self.progress_bar.set(self.progress)
            
            # Subliminal glitch jump
            if random.random() > 0.9:
                self.title_label.configure(text_color=random.choice(["#ff0055", "#00ffcc", "white"]))
                self.title_label.place(x=random.randint(-10, 10), y=random.randint(-10, 10))
            else:
                self.title_label.configure(text_color="white")
                self.title_label.place(x=0, y=0)
                
            self.after(30, self.load_bar)
        else:
            # Add a small pause, then fade out
            self.after(500, self.fade_out)
            
    def fade_out(self, alpha=1.0):
        # Smooth fade-out before showing overlay
        alpha -= 0.05
        self.attributes("-alpha", alpha)
        if alpha > 0.0:
            self.after(20, lambda: self.fade_out(alpha))
        else:
            self.destroy()
            self.parent.attributes("-alpha", 0.0)
            self.parent.deiconify() # Show main overlay window
            self.fade_in_overlay() # Smoothly reveal overlay

    def fade_in_overlay(self, alpha=0.0):
        # Fade in the actual overlay to 90% opacity
        if alpha < 0.90:
            alpha += 0.05
            self.parent.attributes("-alpha", alpha)
            self.after(20, lambda: self.fade_in_overlay(alpha))

class OverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.withdraw() # Hide overlay initially for the splash screen
        
        self.title("ENS'S ROBLOX ANTI KICK")
        self.geometry("260x100")
        
        # Overlay mode: borderless, always on top, slightly transparent
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.90) # 90% opacity to look like glass
        
        # Initial position (Top Right Corner)
        screen_width = self.winfo_screenwidth()
        self.geometry(f"+{screen_width - 290}+30")
        
        self.configure(fg_color="#0d0d12") # Sleek matte dark background
        
        # Variables for Dragging the borderless window anywhere on game screen
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        
        self.is_running = False
        
        # --- UI Elements ---
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        self.title_lbl = ctk.CTkLabel(self.header_frame, text="ENS ANTI-AFK", 
                                      font=ctk.CTkFont(family="Arial", size=13, weight="bold"), 
                                      text_color="#00ffcc")
        self.title_lbl.pack(side="left")
        
        # Minimalist Close Button
        self.close_btn = ctk.CTkButton(self.header_frame, text="✕", width=22, height=22, 
                                       fg_color="transparent", hover_color="#ff1a40",
                                       text_color="#888888", command=self.destroy)
        self.close_btn.pack(side="right")
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Status Dot
        self.status_dot = ctk.CTkLabel(self.main_frame, text="●", 
                                       font=ctk.CTkFont(size=18), text_color="#ff3366")
        self.status_dot.pack(side="left", padx=(0, 5))
        
        # Status Text
        self.status_text = ctk.CTkLabel(self.main_frame, text="IDLE", 
                                        font=ctk.CTkFont(family="Arial", size=11, weight="bold"), 
                                        text_color="#888888")
        self.status_text.pack(side="left")
        
        # Sleek Action Button
        self.toggle_btn = ctk.CTkButton(self.main_frame, text="START", width=70, height=26,
                                        fg_color="#00ffcc", hover_color="#00cca3",
                                        text_color="#000000", font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
                                        command=self.toggle)
        self.toggle_btn.pack(side="right")
        
        # Launch Splash Screen
        self.splash = FullscreenSplash(self)

    # --- Mouse Drag logic ---
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        try:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f"+{x}+{y}")
        except:
            pass

    # --- Macro Logic ---
    def toggle(self):
        if not self.is_running:
            self.is_running = True
            self.toggle_btn.configure(text="STOP", fg_color="#ff3366", hover_color="#cc0033", text_color="white")
            self.status_dot.configure(text_color="#00ffcc")
            self.status_text.configure(text="ACTIVE", text_color="#bbbbbb")
            threading.Thread(target=self.afk_loop, daemon=True).start()
        else:
            self.is_running = False
            self.toggle_btn.configure(text="START", fg_color="#00ffcc", hover_color="#00cca3", text_color="black")
            self.status_dot.configure(text_color="#ff3366")
            self.status_text.configure(text="IDLE", text_color="#888888")

    def afk_loop(self):
        while self.is_running:
            wait_time = random.uniform(600, 720) # 10-12 mins
            elapsed = 0
            while elapsed < wait_time and self.is_running:
                time.sleep(1)
                elapsed += 1
                
            if not self.is_running:
                break
                
            # Perform action UI update
            self.status_dot.configure(text_color="#ffcc00")
            self.status_text.configure(text="BYPASSING...")
            
            try:
                # Camera Movement Bypass Strategy
                pydirectinput.keyDown('right')
                time.sleep(0.5)
                pydirectinput.keyUp('right')
                time.sleep(0.3)
                
                pydirectinput.keyDown('left')
                time.sleep(0.5)
                pydirectinput.keyUp('left')
                time.sleep(0.3)

                pydirectinput.scroll(1)
                time.sleep(0.1)
                pydirectinput.scroll(-1)
            except:
                pass
                
            if self.is_running:
                self.status_dot.configure(text_color="#00ffcc")
                self.status_text.configure(text="ACTIVE")

if __name__ == "__main__":
    app = OverlayApp()
    app.mainloop()
