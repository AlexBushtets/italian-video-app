import os
import cv2
import numpy as np
import random
from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm

os.makedirs("videos", exist_ok=True)


class VerbVideoCreator:
    def __init__(self, filename, delay=5, video_filename="videos/verbs_video.mp4", order="shuffle", with_audio=True):
        self.delay_seconds = delay
        self.fps = 24
        self.width = 1080
        self.height = 1080
        self.video_filename = video_filename
        self.with_audio = with_audio
        self.font_path = "C:/Windows/Fonts/arial.ttf"

        with open(filename, 'r', encoding='utf-8') as f:
            self.lines = [line.strip() for line in f if line.strip()]

        if order == "shuffle":
            random.shuffle(self.lines)

        self.out = cv2.VideoWriter(
            self.video_filename,
            cv2.VideoWriter_fourcc(*'mp4v'),
            self.fps,
            (self.width, self.height)
        )

    def create_video(self):
        total_frames = len(self.lines) * self.fps * self.delay_seconds
        progress_bar = tqdm(total=total_frames, desc="Создание видео", ncols=100)

        for word in self.lines:
            img = self.generate_image_with_text(word)
            for _ in range(self.fps * self.delay_seconds):
                self.out.write(img)
                progress_bar.update(1)

        self.out.release()
        progress_bar.close()
        print(f"\n✅ Видео сохранено как {self.video_filename}")

    def generate_image_with_text(self, text):
        bg_color = tuple(random.randint(220, 255) for _ in range(3))
        img = Image.new("RGB", (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)

        font_size = 60
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except IOError:
            print("⚠️ Не удалось загрузить шрифт.")
            exit()

        wrapped_text = self.wrap_text(text, font, self.width - 40)
        total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 10 for line in wrapped_text)
        y_offset = (self.height - total_text_height) // 2

        for line in wrapped_text:
            text_size = draw.textbbox((0, 0), line, font=font)
            draw.text(
                ((self.width - (text_size[2] - text_size[0])) // 2, y_offset),
                line,
                fill=(0, 0, 0),
                font=font
            )
            y_offset += text_size[3] - text_size[1] + 10

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_size = font.getbbox(test_line)
            if text_size[2] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

def generate_video(category: str, count: int, delay: int = 3, order: str = "shuffle", format: str = "video_audio", output_path: str = None) -> str:
    input_filename = f"words/{category}_{count}.txt"
    output_filename = output_path or f"videos/{category}_{count}_{delay}s_{order}_{format}.mp4"
    lock_path = output_filename + ".lock"

    creator = VerbVideoCreator(
        filename=input_filename,
        delay=delay,
        video_filename=output_filename,
        order=order
    )
    creator.create_video()

    # Удаляем .lock-файл по завершению
    if os.path.exists(lock_path):
        os.remove(lock_path)

    print(f"\n✅ Видео сохранено как {output_filename}")
    return output_filename





