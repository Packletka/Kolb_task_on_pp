import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rectangle_and_point(sw, ne, point):
    fig, ax = plt.subplots()
    rect_width = ne[0] - sw[0]
    rect_height = ne[1] - sw[1]
    rectangle = patches.Rectangle(sw, rect_width, rect_height, linewidth=1, edgecolor='blue', facecolor='lightblue', alpha=0.5)
    ax.add_patch(rectangle)
    ax.plot(point[0], point[1], 'ro')

    ax.set_xlim(min(sw[0], point[0]) - 1, max(ne[0], point[0]) + 1)
    ax.set_ylim(min(sw[1], point[1]) - 1, max(ne[1], point[1]) + 1)
    ax.grid()

    plt.title('N')
    plt.xlabel('S')
    plt.ylabel('W')
    plt.axhline(0, color='black', linewidth=1, ls='-')
    plt.axvline(0, color='black', linewidth=1, ls='-')

    # Сохраняем график в файл
    plt.savefig('rectangle_and_point.png')
    plt.close()  # Закрываем фигуру

# Пример использования
sw_corner = (-1, -2)
ne_corner = (5, 3)
point_coordinates = (-6, 4)

draw_rectangle_and_point(sw_corner, ne_corner, point_coordinates)
