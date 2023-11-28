import os
from uuid import uuid4

import matplotlib.pyplot as plt


fig = None


def render_latex(sm, tm, latex: str):
    global fig
    if fig is None:
        fig = plt.figure()
    # Создание области отрисовки
    fig.clear()
    fig.set_facecolor(tm['MenuColor'])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    # Отрисовка формулы
    t = ax.text(0.5, 0.5, f"${latex}$",
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=14, color=tm['TextColor'])

    # Определение размеров формулы
    ax.figure.canvas.draw()
    bbox = t.get_window_extent()

    # Установка размеров области отрисовки
    fig.set_size_inches(bbox.width / 100, bbox.height / 100)  # dpi=80

    os.makedirs(f"{sm.app_data_dir}/GPT/temp", exist_ok=True)
    image_id = uuid4()
    path = f"{sm.app_data_dir}/GPT/temp/{image_id}.svg"
    plt.savefig(path)
    return path
