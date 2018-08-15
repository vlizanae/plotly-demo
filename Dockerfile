FROM jupyter/datascience-notebook:latest

WORKDIR work

RUN pip install --upgrade pip
RUN pip install flask==0.12.2
RUN pip install plotly dash dash_core_components dash_html_components
