# CS 1.6 Aimbot using Yolo11n object detection model

<img src="./inference.GIF"  width=640 />

## Summary
* Project created as part of KAU Computer Vision Course by @msamrai
* 🦾We trained Yolo11n in Googgle Colab with **A100 GPU** in 100 epochs 
* 🎯Inference with **NVIDIA MX110** (🥲) got approximately 2 FPS
* 🗃️We trained on 2134 images, check out [more](## Dataset)
* 💻Realtime overlay with tkinter

> [!CAUTION]
> Project created in educational purposes, all inference was performed in singleplayer mode.
> 
> DO NOT USE IT IN MULTIPLAYER

## Dataset
* We created [our dataset](https://app.roboflow.com/study-wd0b8/cs-1.6-czwln/browse) using **Roboflow**
* We forked [this dataset](https://app.roboflow.com/study-wd0b8/cs-1.6-players-detection-ed8p3/overview) with 1881 image
* And added 253 images, from self-produced gameplay, and Youtube videos

## Training
Check out [training notebook](train_yolo11n.ipynb)
## Reference and inspiration
Check out [this amazing CS:GO aimbot](https://github.com/daniabib/csgo-aimbot) by @daniabib , which we inspired, and based our code of aimbot
