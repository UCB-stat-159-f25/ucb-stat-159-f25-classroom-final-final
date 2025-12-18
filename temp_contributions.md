(will move to main.ipynb)

Peter Forberg:
I downloaded the data, created additional data files based on the codebook, and generated an outline for our project. I setup the structure of the analysis notebooks. For `1-intro_exploration.ipynb`, I created a cleaned dataframe and provided some initial exploration. For `2-finding_associations.ipynb`, I added additional analyses using correlation matrices (specifically to identify top correlations and then introduce dimension control). For `3-identify_archetypes.ipynb`, I tested multiple clustering and dimension reduction techniques (including some abandoned factor analysis and self-organizing maps). I wrote/adapted the code for PCA, GMM, and HAC. I contributed to the `environment.yml` and the `README.md`.

Neha Suresh:
I worked primarily on the `1-intro_exploration.ipynb` notebook, where I used the cleaned data from Peter to create EDA charts and explore correlations. I continued exploring correlations in `2-finding-associations.ipynb` to generate a correlation map for the selected BAP features. I also modularized some of the EDA code into functions to make it easier for my team to reuse and extend. Additionally, I saved all visualizations in the visualizations folder and the processed data in the data folder for easy access and reusability across notebooks. Finally, I updated the environment.yml file based on the imports I used and tested the environment to ensure all notebooks I worked on run smoothly.

Harish Raghunath:

Sofia Lendahl:
I worked on consolidating all the analysis notebooks into the `main.ipynb` notebook. I organized this notebook into a research paper format, saved key dataframes from the analysis notebook into the `data` folder, displayed key figures from the `visualizations` folder, summarized key findings, and cleaned up the verbiage. I also created a binder link and attached the badge to the `README.md`, created the MyST site and deployed to GitHub Pages, and rendered all of the analysis notebooks and main notebook each as a separate PDF file using MyST and stored them in the `pdf_builds` folder.
