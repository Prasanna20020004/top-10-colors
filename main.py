from PIL import Image
import numpy as np
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


def get_top_10():
    file = "static/images/bleach.jpg"
    img = Image.open(file)

    image_array = np.array(img)

    num_pixels = image_array.shape[0] * image_array.shape[1]
    reshaped_data = image_array.reshape(num_pixels, -1)

    df = pd.DataFrame(reshaped_data, columns=['R', 'G', 'B'])
    count = df.groupby(["R", "G", "B"]).size().reset_index(name='Count')
    count = count.sort_values(by="Count", ascending=False)
    return count[1:10]


@app.route("/")
def home():
    color_count = get_top_10()
    img_array = [(r, g, b) for r, g, b in zip(color_count["R"], color_count["G"], color_count["B"])]
    # print(img_array)
    return render_template("index.html", colors=img_array)


if __name__ == "__main__":
    app.run(debug=False)
