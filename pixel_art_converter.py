import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art Converter")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        self.original_image = None
        self.pixelated_image = None
        self.image_path = None

        self.setup_ui()

    def setup_ui(self):
        font_title = ("Helvetica", 14, "bold")
        font_text = ("Helvetica", 10)

        # Control frame
        control_frame = tk.Frame(self.root, bg="#2e2e2e", padx=20, pady=20)
        control_frame.pack(side="left", fill="y")

        tk.Label(control_frame, text="Pixel Art Generator", font=font_title, bg="#2e2e2e", fg="white").pack(pady=(0, 20))

        btn_cargar = tk.Button(control_frame, text="Cargar imagen", command=self.cargar_imagen, bg="#4e4e4e", fg="white", font=font_text)
        btn_cargar.pack(fill="x", pady=5)

        tk.Label(control_frame, text="Tamaño del bloque", bg="#2e2e2e", fg="white", font=font_text).pack(pady=(15, 5))
        self.bloque_slider = tk.Scale(control_frame, from_=2, to=64, orient="horizontal", bg="#3a3a3a", fg="white")
        self.bloque_slider.set(8)
        self.bloque_slider.pack(fill="x")

        self.modo_avanzado = tk.BooleanVar()
        chk_avanzado = tk.Checkbutton(control_frame, text="Modo avanzado (menos colores)", variable=self.modo_avanzado, bg="#2e2e2e", fg="white", font=font_text, selectcolor="#3a3a3a")
        chk_avanzado.pack(pady=10, anchor="w")

        btn_generar = tk.Button(control_frame, text="Generar Pixel Art", command=self.generar_pixel_art, bg="#6a9955", fg="white", font=font_text)
        btn_generar.pack(fill="x", pady=5)

        self.btn_guardar = tk.Button(control_frame, text="Guardar imagen", command=self.guardar_imagen, state="disabled", bg="#007acc", fg="white", font=font_text)
        self.btn_guardar.pack(fill="x", pady=(20, 5))

        # Preview area
        self.visor = tk.Label(self.root, bg="#1e1e1e")
        self.visor.pack(side="right", expand=True, fill="both", padx=20, pady=20)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.pdf")])
        if ruta:
            self.image_path = ruta
            imagen = Image.open(ruta).convert("RGB")
            self.original_image = imagen
            self.mostrar_imagen(imagen)
            self.btn_guardar.config(state="disabled")

    def generar_pixel_art(self):
        if not self.original_image:
            return

        tamaño_bloque = self.bloque_slider.get()
        imagen = self.original_image.copy()
        ancho, alto = imagen.size

        if self.modo_avanzado.get():
            imagen = imagen.convert("P", palette=Image.ADAPTIVE, colors=32).convert("RGB")

        bloques_ancho = max(1, ancho // tamaño_bloque)
        bloques_alto = max(1, alto // tamaño_bloque)

        reducida = imagen.resize((bloques_ancho, bloques_alto), resample=Image.NEAREST)
        pixelada = reducida.resize((ancho, alto), resample=Image.NEAREST)

        self.pixelated_image = pixelada
        self.mostrar_imagen(pixelada)
        self.btn_guardar.config(state="normal")

    def mostrar_imagen(self, img):
        vista = img.copy()
        vista.thumbnail((500, 500))
        self.tk_imagen = ImageTk.PhotoImage(vista)
        self.visor.config(image=self.tk_imagen)

    def guardar_imagen(self):
        if self.pixelated_image:
            ruta = filedialog.asksaveasfilename(defaultextension=".png")
            if ruta:
                self.pixelated_image.save(ruta)


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()
