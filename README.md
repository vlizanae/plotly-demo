# Plotly for Dashboarding!

Plotly + Dash material for the U-planner talk on 2018-08-16.

### TODO:

* Comment the code.

---
## Usage:

#### Only running the application:

You can see the results by pulling or building the **Dash app** image:

```
docker pull vlizana/dash-app-test
docker run -p 8080:80 vlizana/dash-app-test
```
 and then accessing _localhost:8080_ on the browser, or

 ```
 docker build -t <tag> . # on the dash_app folder
 docker run -p 8080:80 <tag>
 ```

 #### Running the notebooks:

You can also run the notebooks inside a container:

 ```
 docker build -t <tag> . # on the root folder
 docker container run -p 8000:8888 -p 8080:8080 -v $(pwd)/work:/home/jovyan/work:Z <tag>
 ```
