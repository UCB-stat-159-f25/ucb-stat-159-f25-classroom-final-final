(will move to main.ipynb)

Peter Forberg:
I downloaded the data, created additional data files based on the codebook, and generated an outline for our project. I setup the structure of the analysis notebooks. For `1-intro_exploration.ipynb`, I created a cleaned dataframe and provided some initial exploration. For `2-finding_associations.ipynb`, I added additional analyses using correlation matrices (specifically to identify top correlations and then introduce dimension control). For `3-identify_archetypes.ipynb`, I tested multiple clustering and dimension reduction techniques (including some abandoned factor analysis and self-organizing maps). I wrote/adapted the code for PCA, GMM, and HAC. I contributed to the `environment.yml` and the `README.md`.

Neha Suresh:
I worked primarily on the `1-intro_exploration.ipynb` notebook, where I used the cleaned data from Peter to create EDA charts and explore correlations. I continued exploring correlations in `2-finding-associations.ipynb` to generate a correlation map for the selected BAP features. I also modularized some of the EDA code into functions to make it easier for my team to reuse and extend. Additionally, I saved all visualizations in the visualizations folder and the processed data in the data folder for easy access and reusability across notebooks. Finally, I updated the environment.yml file based on the imports I used and tested the environment to ensure all notebooks I worked on run smoothly.

Harish Raghunath:
I worked on designing separating the function definitions through separate files and packages, as well as making the Makefile and researching the license to use for our group. For the functions, I took the modularized functions Neha and Peter designed in the notebooks and made an installable package called "finaltools" which contains the tests and functions with relevant docstrings for the python file and each function. Furthermore, I designed the tests which verify the functionality of the functions defined, and read through the LICENSE guide to choose the right license for the project.

Sofia Lendahl:
