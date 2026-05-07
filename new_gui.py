import math
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from results import Get_Result

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


APP_BG = "#050914"
WINDOW_BG = "#0c1322"
TITLE_BG = "#141c2b"
PANEL = "#151f31"
PANEL_2 = "#1b2639"
BORDER = "#34415f"
MUTED = "#9aa7bf"
DIM = "#66738d"
TEXT = "#f8fbff"
CYAN = "#18d4ff"
PURPLE = "#9c4dff"
PINK = "#ff6376"
RED = "#ff4d4d"
BLUE = "#72b7ff"
GREEN = "#4ee07a"
YELLOW = "#ffd84d"
TEAL = "#55dfd4"


CLASSES = [
    ("Actinic Keratoses", "AK", 27.89, RED),
    ("Dermatofibroma", "DF", 25.43, "#58cbe7"),
    ("Basal Cell Carcinoma", "BCC", 23.02, "#ff7f85"),
    ("Benign Keratosis", "BKL", 8.72, TEAL),
    ("Melanoma", "MEL", 6.43, "#ff4a55"),
    ("Melanocytic Nevi", "NV", 4.58, GREEN),
    ("Vascular Lesions", "VASC", 3.93, YELLOW),
]


class RoundedCanvas(tk.Canvas):
    def rounded_rect(self, x1, y1, x2, y2, radius=18, **kwargs):
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class SkinCancerDetectionInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Skin Cancer Detection System")
        self.root.geometry("980x600")
        self.root.minsize(880, 600)
        self.root.configure(bg=APP_BG)

        self.canvas = RoundedCanvas(root, bg=APP_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=8)

        self.image_path = None
        self.preview_image = None
        self.tk_images = []
        self.click_zones = {}
        self.history = []
        self.predictions = []

        self.model_loaded = False
        self.is_predicting = False
        self.model_handler = Get_Result()
        threading.Thread(target=self._load_model_thread, daemon=True).start()

        self.canvas.bind("<Configure>", self.render)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_motion)

    def _load_model_thread(self):
        self.model_handler.model_load()
        self.model_loaded = True
        self.root.after(0, self.render)

    def set_image(self, path, add_history=True):
        if not self.model_loaded:
            messagebox.showinfo("Bilgi", "Model henüz yüklenmedi, lütfen bekleyin.")
            return

        self.image_path = Path(path)
        self.load_preview()
        
        self.is_predicting = True
        self.render()
        threading.Thread(target=self._predict_thread, args=(path, add_history), daemon=True).start()

    def _predict_thread(self, path, add_history):
        try:
            preds_dict = self.model_handler.get_image_pre_all(str(path))
            mapping = {
                "akiec": ("akiec", "akiec", RED),
                "bcc": ("bcc", "bcc", "#ff7f85"),
                "bkl": ("bkl", "bkl", TEAL),
                "df": ("df", "df", "#58cbe7"),
                "mel": ("mel", "mel", "#ff4a55"),
                "nv": ("nv", "nv", GREEN),
                "vasc": ("vasc", "vasc", YELLOW)
            }
            
            mixed = []
            for key, prob in preds_dict.items():
                name, code, color = mapping[key]
                mixed.append((name, code, prob, color))
                
            mixed.sort(key=lambda item: item[2], reverse=True)
            self.predictions = mixed
            
            if add_history:
                self.history.insert(0, (self.image_path, self.predictions))
                self.history = self.history[:4]
        except Exception as e:
            print("Hata:", e)
            
        self.is_predicting = False
        self.root.after(0, self.render)

    def load_preview(self):
        self.preview_image = None
        self.tk_images.clear()
        if not self.image_path or not self.image_path.exists():
            return

        if Image and ImageTk:
            try:
                self.preview_image = Image.open(self.image_path).convert("RGB")
            except Exception:
                self.preview_image = None
            return

        try:
            self.preview_image = tk.PhotoImage(file=str(self.image_path))
        except tk.TclError:
            self.preview_image = None

    def render(self, event=None):
        self.canvas.delete("all")
        self.click_zones.clear()
        width = max(self.canvas.winfo_width(), 880)
        height = max(self.canvas.winfo_height(), 520)

        self.canvas.rounded_rect(2, 2, width - 2, height - 2, 18, fill=WINDOW_BG, outline="#25314a", width=1)
        self.canvas.create_rectangle(14, 16, width - 14, 54, fill=TITLE_BG, outline="#273550")
        self.draw_titlebar(width)

        if not getattr(self, 'model_loaded', False):
            self.canvas.create_text(width / 2, 60, text="Model yükleniyor, lütfen bekleyin...", fill=YELLOW, font=("Segoe UI", 10, "bold"))
        elif getattr(self, 'is_predicting', False):
            self.canvas.create_text(width / 2, 60, text="Görsel analiz ediliyor...", fill=CYAN, font=("Segoe UI", 10, "bold"))

        content_top = 72
        left_x = 34
        left_w = 214
        gap = 18
        main_x = left_x + left_w + gap
        main_w = width - main_x - 32

        self.draw_upload_panel(left_x, content_top, left_w, 222)
        self.draw_history(left_x, content_top + 234, left_w, 260)
        self.draw_result_panel(main_x, content_top, main_w, 164)
        self.draw_pie_panel(main_x, content_top + 174, main_w * 0.50 - 7, 300)
        self.draw_probability_panel(main_x + main_w * 0.50 + 7, content_top + 174, main_w * 0.50 - 7, 300)

    def draw_titlebar(self, width):
        x = 32
        for color in ("#ff453a", "#ffcc00", "#32d74b"):
            self.canvas.create_oval(x, 31, x + 8, 39, fill=color, outline="")
            x += 15
        self.canvas.create_text(82, 35, text="Skin Cancer Detection System", fill=CYAN, anchor="w", font=("Segoe UI", 10, "bold"))
        self.canvas.create_text(width - 60, 35, text="↙  ↗  ×", fill=DIM, anchor="w", font=("Segoe UI", 11))

    def draw_upload_panel(self, x, y, w, h):
        self.canvas.rounded_rect(x, y, x + w, y + h, 12, fill="#0f1728", outline=BORDER, dash=(3, 3))
        self.click_zones["upload"] = (x, y, x + w, y + h)

        image_x, image_y = x + 18, y + 18
        image_w, image_h = w - 36, h - 64
        self.canvas.rounded_rect(image_x, image_y, image_x + image_w, image_y + image_h, 8, fill="#111827", outline="#263552")

        if self.preview_image:
            self.draw_preview_image(image_x, image_y, image_w, image_h)
        else:
            self.canvas.create_text(image_x + image_w / 2, image_y + 58, text="＋", fill=CYAN, font=("Segoe UI", 34, "bold"))
            self.canvas.create_text(
                image_x + image_w / 2,
                image_y + 102,
                text="Görsel yükle",
                fill=TEXT,
                font=("Segoe UI", 13, "bold"),
            )
            self.canvas.create_text(
                image_x + image_w / 2,
                image_y + 128,
                text="PNG, JPG veya JPEG",
                fill=MUTED,
                font=("Segoe UI", 9),
            )

        filename = self.image_path.name if self.image_path else "Analiz için görsel seç"
        if len(filename) > 30:
            filename = filename[:27] + "..."
        self.canvas.create_text(x + 18, y + h - 25, text="▧  " + filename, fill=MUTED, anchor="w", font=("Segoe UI", 8))

    def draw_preview_image(self, x, y, w, h):
        if Image and ImageTk and hasattr(self.preview_image, "copy"):
            image = self.preview_image.copy()
            image.thumbnail((int(w), int(h)))
            tk_image = ImageTk.PhotoImage(image)
            self.tk_images.append(tk_image)
            self.canvas.create_image(x + w / 2, y + h / 2, image=tk_image, anchor="center")
            return

        if isinstance(self.preview_image, tk.PhotoImage):
            self.tk_images.append(self.preview_image)
            self.canvas.create_image(x + w / 2, y + h / 2, image=self.preview_image, anchor="center")

    def draw_history(self, x, y, w, h):
        self.canvas.rounded_rect(x, y, x + w, y + h, 12, fill="#0f1728", outline="#263552")
        self.canvas.create_text(x + 16, y + 23, text="↻", fill=PURPLE, anchor="w", font=("Segoe UI", 12, "bold"))
        self.canvas.create_text(x + 32, y + 24, text="History", fill=TEXT, anchor="w", font=("Segoe UI", 12, "bold"))
        count = f"{len(self.history)}/4"
        self.canvas.create_text(x + w - 16, y + 24, text=count, fill=DIM, anchor="e", font=("Segoe UI", 8))

        if not self.history:
            self.canvas.create_text(x + w/2, y + 60, text="Henüz görsel yok", fill=MUTED, font=("Segoe UI", 9))
            return

        item_y = y + 42
        for i, (path, preds) in enumerate(self.history):
            if item_y + 46 > y + h - 10:
                break
                
            top = preds[0]
            file_name = path.name
            
            self.canvas.rounded_rect(x + 12, item_y, x + w - 12, item_y + 46, 8, fill=PANEL_2, outline="")
            self.click_zones[f"history_{i}"] = (x + 12, item_y, x + w - 12, item_y + 46)
            short_file = file_name if len(file_name) <= 23 else file_name[:20] + "..."
            self.canvas.create_text(x + 60, item_y + 14, text=top[0], fill=PINK, anchor="w", font=("Segoe UI", 8, "bold"))
            self.canvas.create_text(x + 60, item_y + 30, text=short_file, fill=DIM, anchor="w", font=("Segoe UI", 7))
            self.canvas.create_rectangle(x + 60, item_y + 37, x + 136, item_y + 39, fill=PINK, outline="")
            self.canvas.create_text(x + w - 18, item_y + 34, text=f"{top[2]:.0f}%", fill=TEXT, anchor="e", font=("Segoe UI", 8, "bold"))
            self.canvas.rounded_rect(x + 20, item_y + 6, x + 54, item_y + 40, 5, fill="#273044", outline="")
            self.canvas.create_text(x + 37, item_y + 23, text="Img", fill=MUTED, font=("Segoe UI", 7))
            item_y += 52

    def draw_thumbnail(self, x, y, w, h):
        self.canvas.rounded_rect(x, y, x + w, y + h, 5, fill="#273044", outline="")
        if self.preview_image and Image and ImageTk and hasattr(self.preview_image, "copy"):
            image = self.preview_image.copy()
            image.thumbnail((w, h))
            tk_image = ImageTk.PhotoImage(image)
            self.tk_images.append(tk_image)
            self.canvas.create_image(x + w / 2, y + h / 2, image=tk_image, anchor="center")

    def draw_result_panel(self, x, y, w, h):
        self.canvas.rounded_rect(x, y, x + w, y + h, 12, fill=PANEL, outline=BORDER)
        self.canvas.create_text(x + 18, y + 28, text="↗", fill=CYAN, anchor="w", font=("Segoe UI", 12, "bold"))
        self.canvas.create_text(x + 40, y + 28, text="Diagnosis Result", fill=TEXT, anchor="w", font=("Segoe UI", 12, "bold"))

        if not self.predictions:
            self.canvas.create_text(x + w/2, y + h/2 + 10, text="Sonuçları görmek için bir görsel yükleyin", fill=MUTED, font=("Segoe UI", 10))
            return

        top = self.predictions[0]
        card_w = (w - 40) / 2
        card_y = y + 54
        self.canvas.rounded_rect(x + 16, card_y, x + 16 + card_w, y + h - 18, 9, fill="#2a2635", outline="#74445a")
        self.canvas.rounded_rect(x + 24 + card_w, card_y, x + w - 16, y + h - 18, 9, fill="#292453", outline="#4c2baa")

        self.canvas.create_text(x + 16 + card_w / 2, card_y + 29, text="Predicted Class", fill=MUTED, font=("Segoe UI", 8))
        self.canvas.create_text(x + 16 + card_w / 2, card_y + 62, text=top[0], fill=PINK, font=("Segoe UI", 18, "bold"))
        self.canvas.create_text(x + 16 + card_w / 2, card_y + 84, text=f"({top[1]})", fill=DIM, font=("Segoe UI", 8))

        conf = f"{top[2]:.1f}%"
        self.canvas.create_text(x + 24 + card_w + card_w / 2, card_y + 29, text="Confidence", fill=MUTED, font=("Segoe UI", 8))
        self.canvas.create_text(x + 24 + card_w + card_w / 2, card_y + 64, text=conf, fill="#90baff", font=("Segoe UI", 26, "bold"))

    def draw_pie_panel(self, x, y, w, h):
        self.canvas.rounded_rect(x, y, x + w, y + h, 12, fill=PANEL, outline=BORDER)
        self.canvas.create_text(x + 18, y + 28, text="◔", fill=PURPLE, anchor="w", font=("Segoe UI", 13, "bold"))
        self.canvas.create_text(x + 40, y + 28, text="Class Distribution", fill=TEXT, anchor="w", font=("Segoe UI", 11, "bold"))
        self.canvas.rounded_rect(x + w - 82, y + 18, x + w - 18, y + 40, 7, fill="#202d42", outline="")
        self.canvas.rounded_rect(x + w - 82, y + 18, x + w - 48, y + 40, 7, fill=PURPLE, outline="")
        self.canvas.create_text(x + w - 65, y + 29, text="Pie", fill=TEXT, font=("Segoe UI", 8, "bold"))
        self.canvas.create_text(x + w - 34, y + 29, text="Bar", fill=MUTED, font=("Segoe UI", 8))

        if not self.predictions:
            self.canvas.create_text(x + w/2, y + h/2 + 10, text="Veri Yok", fill=MUTED, font=("Segoe UI", 10))
            return

        center_x = x + w * 0.50
        center_y = y + h * 0.57
        radius = min(w, h) * 0.23
        start = 90
        for name, code, score, color in self.predictions:
            extent = -score / 100 * 360
            if extent >= -0.1: continue
            
            if extent <= -359.9:
                self.canvas.create_oval(
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                    fill=color,
                    outline="#edf2ff",
                    width=1,
                )
            else:
                self.canvas.create_arc(
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                    start=start,
                    extent=extent,
                    fill=color,
                    outline="#edf2ff",
                    width=1,
                )
            if score >= 3.0:
                mid = math.radians(start + extent / 2)
                label_x = center_x + math.cos(mid) * (radius + 48)
                label_y = center_y - math.sin(mid) * (radius + 34)
                self.canvas.create_text(
                    label_x,
                    label_y,
                    text=f"{code}: {score:.1f}%",
                    fill=color,
                    font=("Segoe UI", 8, "bold"),
                )
            start += extent

    def draw_probability_panel(self, x, y, w, h):
        self.canvas.rounded_rect(x, y, x + w, y + h, 12, fill=PANEL, outline=BORDER)
        self.canvas.create_text(x + 18, y + 28, text="↧", fill=CYAN, anchor="w", font=("Segoe UI", 13, "bold"))
        self.canvas.create_text(x + 40, y + 28, text="Probability Breakdown", fill=TEXT, anchor="w", font=("Segoe UI", 11, "bold"))

        if not self.predictions:
            self.canvas.create_text(x + w/2, y + h/2 + 10, text="Veri Yok", fill=MUTED, font=("Segoe UI", 10))
            return

        list_x = x + 18
        list_y = y + 54
        bar_w = w - 58
        max_score = max(score for _, _, score, _ in self.predictions) or 1
        for index, (name, _code, score, color) in enumerate(self.predictions):
            row_y = list_y + index * 32
            self.canvas.create_oval(list_x, row_y + 3, list_x + 8, row_y + 11, fill=color, outline="")
            self.canvas.create_text(list_x + 15, row_y + 7, text=name, fill=TEXT, anchor="w", font=("Segoe UI", 7, "bold"))
            self.canvas.create_text(x + w - 38, row_y + 7, text=f"{score:.2f}%", fill=color, anchor="e", font=("Segoe UI", 7, "bold"))
            self.canvas.create_rectangle(list_x, row_y + 17, list_x + bar_w, row_y + 22, fill="#223047", outline="")
            self.canvas.create_rectangle(
                list_x,
                row_y + 17,
                list_x + bar_w * (score / max_score),
                row_y + 22,
                fill=color,
                outline="",
            )

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Görsel seç",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.set_image(path)

    def handle_click(self, event):
        zone = self.click_zones.get("upload")
        if zone and zone[0] <= event.x <= zone[2] and zone[1] <= event.y <= zone[3]:
            self.choose_image()
            return
            
        for key, zone in self.click_zones.items():
            if key.startswith("history_") and zone[0] <= event.x <= zone[2] and zone[1] <= event.y <= zone[3]:
                idx = int(key.split("_")[1])
                path, preds = self.history[idx]
                self.image_path = path
                self.predictions = preds
                self.load_preview()
                self.render()
                break

    def handle_motion(self, event):
        hovering = False
        for key, zone in self.click_zones.items():
            if zone[0] <= event.x <= zone[2] and zone[1] <= event.y <= zone[3]:
                hovering = True
                break
        self.canvas.configure(cursor="hand2" if hovering else "")


def main():
    root = tk.Tk()
    app = SkinCancerDetectionInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()