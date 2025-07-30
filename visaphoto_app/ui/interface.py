import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from photo_utils.background_removal import remove_background
from photo_utils.face_detect import detect_face
from photo_utils.resize_align import resize_and_center

# Dossier de sortie
OUTPUT_FOLDER = "output_photos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_photo(input_path, output_path):
    try:
        # Suppression du fond
        img_no_bg = remove_background(input_path)

        # Détection du visage (sur l'image originale)
        face_coords = detect_face(input_path)

        # Redimensionnement et centrage
        final_img = resize_and_center(img_no_bg, face_coords)

        # Sauvegarde finale
        final_img.save(output_path)
        return output_path
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de traiter la photo : {e}")
        return None

def launch_app():
    root = tk.Tk()
    root.title("VisaPhoto Clone - by Ethaniel ❤️")
    root.geometry("600x700")
    root.configure(bg="#f0f0f0")

    # Label titre
    title = tk.Label(root, text="Photo d'identité automatique", font=("Arial", 18, "bold"), bg="#f0f0f0")
    title.pack(pady=20)

    # Zone de preview
    preview_label = tk.Label(root, text="Aucune image chargée", bg="#ccc", width=60, height=20)
    preview_label.pack(pady=10)

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not file_path:
            return
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            preview_label.config(image=img_tk, text="")
            preview_label.image = img_tk
            process_btn.config(state="normal")
            preview_label.file_path = file_path
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image : {e}")

    def process_current_photo():
        if not hasattr(preview_label, "file_path"):
            messagebox.showwarning("Attention", "Aucune image chargée.")
            return
        input_path = preview_label.file_path
        output_path = os.path.join(OUTPUT_FOLDER, "photo_result.jpg")

        result = process_photo(input_path, output_path)
        if result:
            messagebox.showinfo("Succès", f"Photo traitée et enregistrée : {result}")
            img = Image.open(result)
            img.thumbnail((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            preview_label.config(image=img_tk)
            preview_label.image = img_tk

    # Boutons
    open_btn = tk.Button(root, text="Choisir une photo", command=open_file, font=("Arial", 12))
    open_btn.pack(pady=10)

    process_btn = tk.Button(root, text="Traiter la photo", command=process_current_photo, state="disabled", font=("Arial", 12))
    process_btn.pack(pady=10)

    root.mainloop()
