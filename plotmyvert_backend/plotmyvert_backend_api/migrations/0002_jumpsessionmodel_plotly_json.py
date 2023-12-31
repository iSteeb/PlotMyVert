# Generated by Django 5.0 on 2023-12-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plotmyvert_backend_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jumpsessionmodel',
            name='plotly_json',
            field=models.TextField(default="{data: [{type: 'scatter',mode: 'markers',name: 'Sample Data',x: [1, 2, 3, 4],y: [10, 11, 12, 13],marker: { color: '#1f77b4', size: 6 }}],layout: {title: { text: 'Sample Plot' },xaxis: { title: { text: 'X-axis' } },yaxis: { title: { text: 'Y-axis' } },autosize: false}}"),
            preserve_default=False,
        ),
    ]
