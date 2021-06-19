from pathlib import Path

import cv2
import tkinter as tk
from PIL import ImageTk, Image


class App:
    def __init__(self, src_paths: list, dst_dir):
        self.src_paths = src_paths
        self.dst_dir = dst_dir
        self.path_pointer = 0

        self.window = tk.Tk()
        img, self.height, self.width = self.get_image(self.path_pointer)

        self.canvas = tk.Canvas(self.window, height=self.height, width=self.width)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=img)
        self.canvas.grid(row=2, column=1)

        self.points = []
        self.window.bind("<1>", self.handle_click)

        self.window.mainloop()

    def handle_click(self, event):
        x, y = event.x, event.y
        x = min(self.width, max(0, x))
        y = min(self.height, max(0, y))
        self.points += [(x, y, self.draw_point(x, y))]

        if len(self.points) == 4:
            self.finish_image()

    def finish_image(self):
        self.save_points()
        self.path_pointer += 1

        # remove old points
        for _, _, point_id in self.points:
            self.canvas.delete(point_id)
        self.points = []

        if self.path_pointer == len(self.src_paths):
            self.window.destroy()
            return

        img, self.height, self.width = self.get_image(self.path_pointer)
        self.canvas.itemconfig(self.image_on_canvas, image=img)
        self.canvas.image = img

    def save_points(self):
        assert len(self.points) == 4

        src_path = self.src_paths[self.path_pointer]
        points_path = self.dst_dir / f'{src_path.stem}.json'

        points = [(x / self.width, y / self.height) for x, y, _ in self.points]
        result = '[' + ', '.join([f'[{x:.4f}, {y:.4f}]' for x, y in points]) + ']'

        points_path.write_text(result)

    def get_image(self, idx):
        path = self.src_paths[idx]
        ext = Path(path).suffix[1:]

        if ext in ('jpg', 'png'):
            img = cv2.imread(str(path))[:, :, ::-1].copy()
        elif ext in ('mp4', 'mkv'):
            cap = cv2.VideoCapture(str(path))
            ret, img = cap.read()
            if not ret:
                raise
            img = img[:, :, ::-1].copy()
        else:
            raise KeyError(f'{path} is not image or video')

        height, width = img.shape[:2]
        tk_img = ImageTk.PhotoImage(Image.fromarray(img))
        return tk_img, height, width

    def draw_point(self, x, y, r=4, color='red'):
        x0, y0 = x - r, y - r
        x1, y1 = x + r, y + r
        point = self.canvas.create_oval(x0, y0, x1, y1, fill=color)
        return point


if __name__ == '__main__':
    src_paths = list(Path('data').glob('[!.]*'))
    dst_dir = Path('coords')
    dst_dir.mkdir(exist_ok=True)

    app = App(src_paths, dst_dir)
