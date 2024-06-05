from flask import Flask, render_template, send_file, make_response
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

def generate_and_save_coordinates(num_points=1000, filename='coordinates.xlsx'):
    x_coords = np.random.randint(0, 1001, num_points)
    y_coords = np.random.randint(0, 1001, num_points)
    df = pd.DataFrame({'X': x_coords, 'Y': y_coords})
    df.to_excel(filename, index=False)
    return df

def plot_colored_grid(df, grid_size=200):
    x_coords = df['X']
    y_coords = df['Y']

    # Renk paleti oluşturma
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink', 'brown', 'cyan', 'magenta']
    color_dict = {}

    plt.figure(figsize=(10, 10))
    for i in range(0, 1000, grid_size):
        for j in range(0, 1000, grid_size):
            grid_points = df[(x_coords >= i) & (x_coords < i + grid_size) & 
                             (y_coords >= j) & (y_coords < j + grid_size)]
            if not grid_points.empty:
                # Her grid hücresi için renk seçimi
                color_key = (i // grid_size, j // grid_size)
                if color_key not in color_dict:
                    color_dict[color_key] = colors[len(color_dict) % len(colors)]
                plt.scatter(grid_points['X'], grid_points['Y'], color=color_dict[color_key], alpha=0.5)

    plt.xlabel('X Koordinatları')
    plt.ylabel('Y Koordinatları')
    plt.title(f'{grid_size}x{grid_size} Izgaraya Bölünmüş Rastgele Noktalar')
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/')
def index():
    return render_template('index.html', name="Elife Beyzanur", surname="Yüksel", student_id="171213069")

@app.route('/generate_plot')
def generate_plot():
    df = generate_and_save_coordinates()
    img = plot_colored_grid(df)
    return send_file(img, mimetype='image/png')

@app.route('/download_excel')
def download_excel():
    df = generate_and_save_coordinates()
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='coordinates.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
