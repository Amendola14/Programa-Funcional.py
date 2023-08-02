from fpdf import FPDF
from matplotlib import pyplot as plt

from fileCsv import mkdir_dir

class PDF(FPDF):
      
    def footer(self):
        # Pie de página del PDF
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        # Título del capítulo en el PDF
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, image_path):
        # Cuerpo del capítulo en el PDF
        self.image(image_path, x=10, y=None, w=190)

def generar_grafico(meses, ganancias, title):
    # Código para generar el gráfico de líneas y guardar el PDF
    plt.xlabel('MESES')
    plt.ylabel('$ - GANANCIAS MENSUALES')
    plt.plot(meses, ganancias)
    plt.title(title)
    image_path = f'./images/grafico_socios.png'
    if mkdir_dir('./images/'):
        plt.savefig(image_path)
    plt.show()
    pdf_path = './pdf/grafico_lineal.pdf'
    if mkdir_dir('./pdf/'):
        pdf = PDF()
        pdf.add_page()
        pdf.chapter_title(f'Ganancias total: ${sum(ganancias)}')
        pdf.chapter_body(image_path)
        pdf.output(pdf_path)

def generar_grafico_ganancias_administrador(ganancias_por_mes):
    # Verificar que existen datos para los meses de Julio, Junio y Agosto
    if 'Julio' not in ganancias_por_mes or 'Junio' not in ganancias_por_mes or 'Agosto' not in ganancias_por_mes:
        print("No hay datos disponibles para los meses de Julio, Junio y Agosto.")
        return

    # Obtener las ganancias para los meses predeterminados
    ganancias_julio = ganancias_por_mes['Julio']
    ganancias_junio = ganancias_por_mes['Junio']
    ganancias_agosto = ganancias_por_mes['Agosto']

    # Generar el gráfico de torta con diferentes colores para cada mes
    etiquetas = ['Julio', 'Junio', 'Agosto']
    valores = [ganancias_julio, ganancias_junio, ganancias_agosto]
    colores = ['red', 'blue', 'green']

    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=etiquetas, colors=colores, autopct='%1.1f%%', pctdistance=0.85, startangle=140)
    plt.title("Estadísticas de Ganancia por Mes - Administrador")
    plt.axis('equal')
    plt.show()
