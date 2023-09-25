import os
import replicate
os.environ['REPLICATE_API_TOKEN'] = 'r8_1nh4HC3tqllsdse9sm1ueWgYbcyywDf05wjz6'
import cv2
import numpy as np

def render(path,model,prompt=""):
    grey = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(grey,(5,5),100)
    thresh = cv2.threshold(blurred,150, 255, cv2.THRESH_BINARY)[1]
    white_canvas = np.ones_like(blurred) * 255
    result = cv2.bitwise_and(white_canvas, white_canvas, mask=thresh)

    cv2.imwrite("./processed.png",result)
    path = "./processed.png"
    
    if model==1:
        output = replicate.run(
            "jagilley/controlnet-scribble:435061a1b5a4c1e26740464bf786efdfa9cb3a3ac488595a2de23e143fdb0117",
            input={"image": open(path, "rb"),
                "prompt": prompt,
                }
        )
        return output[1]
    elif model==2:
        output = replicate.run(
            "rossjillian/controlnet:795433b19458d0f4fa172a7ccf93178d2adb1cb8ab2ad6c8fdc33fdbcd49f477",
            input={"image": open(path, "rb"),
                "prompt": prompt,
                "structure":"pose"
                }
        )
        return output[0]

def set_key(key):
    os.environ['REPLICATE_API_TOKEN'] = key
    return os.environ['REPLICATE_API_TOKEN']
