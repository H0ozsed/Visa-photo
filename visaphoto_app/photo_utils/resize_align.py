from PIL import Image

def resize_and_center(image, face_coords, output_size=(600, 600), face_height_ratio=0.5):
    left, top, right, bottom = face_coords
    face_center_x = (left + right) // 2
    face_center_y = (top + bottom) // 2

    # Définir une zone de crop autour du visage avec padding
    width = right - left
    height = bottom - top
    padding = int(max(width, height) * 1.5)
    crop_left = max(face_center_x - padding, 0)
    crop_top = max(face_center_y - padding, 0)
    crop_right = face_center_x + padding
    crop_bottom = face_center_y + padding

    # Crop et resize
    image_cropped = image.crop((crop_left, crop_top, crop_right, crop_bottom))
    image_resized = image_cropped.resize(output_size, Image.ANTIALIAS)

    # Coller sur fond blanc
    final_image = Image.new("RGB", output_size, (255, 255, 255))
    final_image.paste(image_resized, (0, 0))
    return final_image
