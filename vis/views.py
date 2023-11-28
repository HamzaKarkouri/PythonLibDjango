from django.shortcuts import render
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import numpy as np
from pd.models import UploadedFile
# Create your views here.

# def show1(request):
#     context = {}
#     uploaded_files = UploadedFile.objects.all()
#     context['uploaded_files'] = uploaded_files
#     charts = {

#               'Line_Plot':'Line Plot',
#               'Scatter_Plot':'Scatter Plot',
#               'box_plot':'Box Plot',
#               'Histogram':'Histogram',
#               'Image':'Image',
#               'Kde_Plot':'Kde Plot',
#               'Violin_Plot':'Violin Plot',
#               'Bar_plot':'Bar Plot',
#               'Heatmap':'Heatmap',
#               'Pie_chart':'Pie Chart'

#              }
#     context['charts']= charts
#     print("heeeeeeeeeeeeeeeeeeeeere")
#     return render(request, 'chart_view.html',context )






def show(request):
    context = {}
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    

    charts = {

              'Line_Plot':'Line Plot',
              'Scatter_Plot':'Scatter Plot',
              'box_plot':'Box Plot',
              'Histogram':'Histogram',
              'Image':'Image',
              'Kde_Plot':'Kde Plot',
              'Violin_Plot':'Violin Plot',
              'Bar_plot':'Bar Plot',
              'Heatmap':'Heatmap',
              'Pie_chart':'Pie Chart'

             }
    
    if request.method == 'POST':
        print("2222")
        filename1 = request.POST.get('dropdown1', None)
        filename = filename1.split("uploaded_csv/")[1]
        print("3333"+filename)
        # Filter UploadedFile objects based on the file name
        uploaded_files = UploadedFile.objects.filter(file__contains=filename)

        if uploaded_files.exists():
            print(4444)
            # Assuming you want to work with the first matching file
            uploaded_file = uploaded_files.first()

            # Read the CSV file using pandas
            df = pd.read_csv(uploaded_file.file.path)

            context['datahtml'] = df
            context['lendata'] = len(df)
            context['selected'] = filename1
            context['columns'] = df
        
        selected_chart_key = request.POST.get('selected_chart')
        print(selected_chart_key)
        choix1 = request.POST.get('choix1')
        print(choix1)
        choix2 = request.POST.get('choix2')
        print(choix2)


        filename = request.POST.get('dropdown1')
        print("here"+request.POST.get('dropdown1'))
        # filename = filename.split("uploaded_csv/")[1]

        # Filter UploadedFile objects based on the file name
        uploaded_files = UploadedFile.objects.filter(file__contains=filename)
        if selected_chart_key:
            context['selected'] = charts[selected_chart_key]

        print(uploaded_files)
        
        if selected_chart_key == 'Line_Plot':
            print(selected_chart_key)
            
         
            df = pd.DataFrame(uploaded_files)
            df[choix1] = pd.to_datetime(df[choix1])

            sns.set()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=choix1, y=choix2, data=df, marker='o', color='b', label=choix2, ax=ax)
            ax.set_xlabel(choix1)
            ax.set_ylabel(choix2)
            ax.set_title('Line Plot')
            ax.legend()

            # Convert the plot to an image
            buf = io.BytesIO()
            canvas = FigureCanvasAgg(fig)
            canvas.print_png(buf)
            data = base64.b64encode(buf.getbuffer()).decode('utf-8')
            plt.close(fig)
            # Embed the image in the HTML response
            context['image'] = data



        if selected_chart_key == 'Scatter_Plot':
            print(selected_chart_key)

            diamonds = sns.load_dataset('diamonds')
            diamonds = diamonds[
            diamonds.cut.isin(['Premium', 'Good']) &
            diamonds.color.isin(['D', 'F', 'J'])
            ].sample(n=100, random_state=22)
            diamonds.shape 
            sns.scatterplot(x='carat', y='price', data=diamonds)
            plt.title('Scatter Plot of Carat vs. Price')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            # Encode the image as base64
            graph = base64.b64encode(image_png).decode()
            context['image'] = graph

        if selected_chart_key == 'box_plot':
            print(selected_chart_key)

            cars = sns.load_dataset('mpg').dropna()
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            sns.boxplot(cars.mpg, ax=axes[0])
            axes[0].set_title('Box Plot - Overall MPG')
            sns.boxplot(x=cars.origin, y=cars.mpg, ax=axes[1])
            axes[1].set_title('Box Plot - MPG by Origin')
            sns.boxplot(x='origin', y='mpg', hue='cylinders', data=cars, ax=axes[2])
            axes[2].set_title('Box Plot - MPG by Origin and Cylinders')
            plt.tight_layout()

            # Save the plot to a BytesIO object
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            # Encode the image as base64
            graph = base64.b64encode(image_png).decode()
            context['image'] = graph

        if selected_chart_key == 'Histogram':

            penguins = sns.load_dataset('penguins')
            penguins.dropna(inplace=True)

            # Create a figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))

            # Histogram for bill length
            sns.histplot(penguins.bill_length_mm, ax=axes[0, 0])
            axes[0, 0].set_title('Histogram - Bill Length')

            # Histogram for bill length by species
            sns.histplot(x='bill_length_mm', data=penguins, hue='species', ax=axes[0, 1])
            axes[0, 1].set_title('Histogram by Species - Bill Length')

            # Generate a random grayscale image
            X = np.random.randint(0, 256, size=(50, 50))

            # Display the grayscale image
            axes[1, 0].imshow(X, cmap='gray')
            axes[1, 0].set_title('Random Grayscale Image')

            # Display the histogram of the image
            axes[1, 1].hist(X.ravel(), color='blue', bins=50)
            axes[1, 1].set_title('Histogram of the Image')

            # Adjust layout
            plt.tight_layout()

            # Save the plot to a BytesIO object
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            # Encode the image as base64
            graph = base64.b64encode(image_png).decode()
            context['image'] = graph


        context['lendata'] = len(context['datahtml'])
    context['charts']= charts
    return render(request, 'chart_views.html',context )

