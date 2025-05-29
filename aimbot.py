from mss import mss
import cv2 as cv
import numpy as np
import pyautogui
from ultralytics import YOLO
from ultralytics.engine.results import Results
import torch



pyautogui.FAILSAFE = False

CLASSES = {
    0: 'Counter-Terrorist',
    1: 'Head',
    2: 'Terrorist',
    3: 'None'
}

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.coordinates = np.array([x, y], dtype=float)

    def __sub__(self, other: 'Point') -> float:
        return np.linalg.norm(self.coordinates - other.coordinates) # type: ignore

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"


class Target:
    def __init__(self, target: torch.Tensor) -> None:
        self.x: float = target[0].item()
        self.y: float = target[1].item()
        self.w: float = target[2].item()
        self.h: float = target[3].item()
        self.confidence: float = target[4].item()
        self.label: int = int(target[5].item())
        self.tensor: torch.Tensor = target
        self.coordinates = np.array([self.x+self.w/2, self.y + self.h/2])
        self.label_str: str = CLASSES[self.label]
        
    def __repr__(self) -> str:
        return f"{self.label_str}({self.x}, {self.y})"


def form_object_list(result: Results) -> list[Target]:
    object_list: list[Target] = []
    for box, cnf, label in zip(result.boxes.xywh, result.boxes.conf, result.boxes.cls): # type: ignore
        print(label.item()) # type: ignore
        if cnf>=0.55:
            object_list.append(Target([*box, cnf, label])) # type: ignore
    print(object_list)
    return object_list


def get_target(targets: list[Target], center: Point, filter_classes: list[int]) -> Target | None:
    targets =  sorted([t for t in targets if t.label in filter_classes], key=lambda target: center - target) # type: ignore
    if targets:
        return targets[0]
    return None

def shoot() -> None:
    pyautogui.mouseDown()
    pyautogui.mouseUp()

def draw_boxes(canvas, targets): # type: ignore
    canvas.delete("all") # type: ignore
    for t in targets: # type: ignore
        if t.label==2: # type: ignore
            canvas.create_rectangle(t.x-t.w/2, t.y-t.h/2, t.x+t.w/2, t.y +t.h/2, outline='red', width=5) # type: ignore
        elif t.label==0: # type: ignore
            canvas.create_rectangle(t.x-t.w/2, t.y-t.h/2, t.x+t.w/2, t.y +t.h/2, outline='blue', width=5) # type: ignore
        elif t.label==1: # type: ignore
            canvas.create_rectangle(t.x-t.w/2, t.y-t.h/2, t.x+t.w/2, t.y +t.h/2, outline='magenta', width=2) # type: ignore
  

from tkinter import Tk, Toplevel, Canvas


def main():
    transparent_color = 'grey15'
    root = Tk()
    top = Toplevel(root)
    top.attributes('-transparentcolor', transparent_color) # type: ignore
    top.attributes('-topmost', True) # type: ignore
    top.attributes('-fullscreen', True) # type: ignore
    canvas = Canvas(top, bg=transparent_color, highlightthickness=0)
    
    canvas.pack(fill='both', expand=True)
    center = Point(x=1920//2, y=1080//2)

    model = YOLO("./yolo11n.pt")
    
    SHOT_FILTER: list[int] = [2]
    with mss() as sct:
        while True:
            
            screenshot = np.array(sct.grab(sct.monitors[0]))[:, :, :3]

            result: Results = model.predict(screenshot, device=0)[0] # type: ignore
            
            objects: list[Target] = form_object_list(result)
            
            draw_boxes(canvas, objects)
            root.update()
            
            target: Target|None = get_target(objects, center, SHOT_FILTER)
            if target is not None:
                pyautogui.moveTo(target.x, target.y)
                shoot()
                shoot()
                shoot()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break


if __name__ == "__main__":
    main()
