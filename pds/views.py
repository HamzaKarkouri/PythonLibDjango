# views.py
from django.shortcuts import render
from pd.models import UploadedFile
import pandas as pd

def list_uploaded_files(request):
    context = {}
    aggregations = {
    'Mean': 'mean',
    'Sum': 'sum',
    'Max': 'max',
    'Min': 'min',
    'Median':'median',
    'Count': 'count',
}
    context['agg'] = aggregations
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    print("11111")
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

        
       # Accessing selected columns
        print("hello")
        selected_columns = request.POST.getlist('selected_columns')
        print('Selected Columns:', selected_columns)
        if selected_columns:
            if selected_columns != 'all':
                context['datahtml'] = df[selected_columns]


        # Accessing head and tail checkboxes
        slice_option = request.POST.get('slice_option', '')
        print('Slice Option:', slice_option)
        if slice_option == 'head':
            context['datahtml'] = context['datahtml'].head()
        elif slice_option == 'tail':
            context['datahtml'] = context['datahtml'].tail()

        

        

        # Accessing line1 and line2 inputs
        line1_value = int(request.POST.get('line1',0))
        line2_value = int(request.POST.get('line2', 0))

        if line2_value == 0 and line1_value != 0:
            context['datahtml'] = context['datahtml'].iloc[line1_value]
        elif line2_value != 0 and line1_value != 0:
            context['datahtml'] = context['datahtml'].iloc[line1_value:line2_value]
     


        print('Line 1 Value:', line1_value)
        print('Line 2 Value:', line2_value)

        # Accessing sample input
        sample_value = int(request.POST.get('sample', 0))
        print('Sample Value:', sample_value)

        # Accessing group by select and selected columns
        group_by_column = request.POST.get('group', '')
        print('Group By Column:', group_by_column)

        group_by_selected_columns = request.POST.getlist('selected_columns2')
        print('Group By Selected Columns:', group_by_selected_columns)
        
        agg = request.POST.get('agg', '')
        print(' agg:', agg)


        if group_by_column and group_by_selected_columns:
            if agg == 'Mean':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].mean()
            elif agg == 'Sum':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].sum()
            elif agg == 'Max':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].max()
            elif agg == 'Min':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].min()
            elif agg == 'Median':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].median()
            elif agg == 'Count':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].count()

        context['lendata'] = len(context['datahtml'])
    return render(request, 'list_files.html', context)

