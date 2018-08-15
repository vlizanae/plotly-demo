FROM vlizana/alpine-pandas-py3

WORKDIR application

ADD app.py .
ADD pokemons.csv .
ADD assets assets

RUN pip3 install flask==0.12.2
RUN pip3 install plotly dash dash_renderer dash_core_components dash_html_components

EXPOSE 80

CMD python3 app.py
