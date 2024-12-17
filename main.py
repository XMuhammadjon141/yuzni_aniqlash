import cv2
import face_recognition
import tkinter as tk
from tkinter import filedialog, messagebox

# O'qitilgan yuz ma'lumotlari
known_face_encodings = []
known_face_names = []

# Yangi yuzni kiritish funksiyasi
def add_new_face(name, frame):
    face_encodings = face_recognition.face_encodings(frame)
    if face_encodings:
        face_encoding = face_encodings[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
        messagebox.showinfo("Ma'lumot", f"{name} muvaffaqiyatli qo'shildi!")
    else:
        messagebox.showerror("Xatolik", "Yuz aniqlanmadi. Iltimos, qaytadan urinib ko'ring.")

# Suratga olish funksiyasi
def capture_face(name):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow('Press Space to Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):  # Space tugmasi bosilganda
            add_new_face(name, frame)
            cv2.imwrite(f"images/{name}.jpg", frame)
            break
    video_capture.release()
    cv2.destroyAllWindows()

# Yuzni aniqlash jarayonini to'xtatish uchun flag
stop_recognition = False

# Kamera orqali real vaqt mobaynida yuzni aniqlash
def run_face_recognition():
    global stop_recognition
    stop_recognition = False

    video_capture = cv2.VideoCapture(0)

    while not stop_recognition:
        # Kadrni o'qish
        ret, frame = video_capture.read()

        # Rasmni kichraytirish va RGB formatiga o'tkazish
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Yuzlarni aniqlash va kodlash
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Aniqlangan yuzlarni tanish va nomini chiqarish
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Yuqori kadr hajmini tiklash
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Yuqori, o'ng, pastki va chap xududlarni aniqlash
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        # Oyna chiqarish
        cv2.imshow('Video', frame)

        # 'q' tugmasi bosilganda chiqish
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Resurslarni bo'shatish
    video_capture.release()
    cv2.destroyAllWindows()

# Yuzni aniqlash jarayonini to'xtatish funksiyasi
def stop_face_recognition():
    global stop_recognition
    stop_recognition = True

# Foydalanuvchini ro'yxatdan o'tkazish oynasi
def add_user_window():
    add_user_win = tk.Toplevel(root)
    add_user_win.title("Yangi foydalanuvchi qo'shish")
    add_user_win.geometry("300x250")

    tk.Label(add_user_win, text="Ismni kiriting:").pack(pady=5)
    name_entry = tk.Entry(add_user_win)
    name_entry.pack(pady=5)

    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            frame = face_recognition.load_image_file(file_path)
            add_new_face(name_entry.get(), frame)

    def open_camera():
        name = name_entry.get()
        capture_face(name)

    capture_button = tk.Button(add_user_win, text="Suratga olish", command=open_camera)
    capture_button.pack(pady=10)

    upload_button = tk.Button(add_user_y=10)

# Tkinter oynasini yaratish
root = tk.Tk()
root.title('Yuzni aniqlash')
root.geometry('400x400')

face_recognition_button = tk.Button(roowin, text="Suratni yuklash", command=upload_photo)
    upload_button.pack(padt, text="Yuzni aniqlash", command=run_face_recognition)
face_recognition_button.pack(pady=10)

stop_button = tk.Button(root, text="To'xtatish", command=stop_face_recognition)
stop_button.pack(pady=10)

add_user_button = tk.Button(root, text="Yangi foydalanuvchi qo'shish", command=add_user_window)
add_user_button.pack(pady=10)

# Tkinter oynasini boshlash
root.mainloop()