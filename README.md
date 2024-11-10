# CoCo: Code Completion Test Project

Welcome to the CoCo repository!  
This project is a test task for JetBrains CodeCompletion and is named as a reference to the COCo dataset.  
Some of the source code is purposely overcomplicated to demonstrate the ability to work with complex codebases and create a very general base for future work.

## Overview
This project involves generating code data, performing analysis on it, and drawing conclusions for future work.

## Data Generation
The data generation process is handled by the `generator.py` script, 
which reads configurations from the `simple_sampler.yaml` file.  
The steps include:
- Collecting Source Code Files: It scans a specified directory for source code files with a particular extension (e.g., .py files).
- Filtering Code Lines: Utilizes regular expressions to exclude certain lines, such as imports.
- Splitting Code: Divides code into prefixes, middles, and suffixes based on various specified parameters and provided strategies (`finish_lines`, `finish_words`).
- Predicting with specified models: Utilizes the specified models to predict the middle part of the code.
- Saves the generated data to a specified file.

To generate data, run the following command:
```bash
python code/generator.py configs/simple_sampler.yaml
```

## Data Analysis
Analysis is performed in the Jupyter Notebook `analysis.ipynb`, which includes:
- Descriptive Statistics: Computing metrics like mean, standard deviation, min, max, and quartiles for various code quality metrics such as BLEU, CHRF, and CodeBLEU.
- Correlation Analysis: Assessing the relationships between different metrics to understand their interdependencies.
- Visualizations: Creating plots to visualize distributions and correlations among metrics.

Note that some of the Jupyter Notebook cells outputs aren't displayed correctly unless you run them.  
Running all the cells takes a couple of seconds, so don't worry about that.  

## Conclusion
The analysis shows that 
- CodeBLEU is the closest metric to my human evaluation 
- Unlike all the other metrics, CodeBLEU suggests predicting using `finish_lines` strategy, rather than `finish_words` strategy. 

## Future Work
Planned enhancements include:

- Optimizing Sampling Strategies: Exploring diverse sampling methods to improve data quality and representativeness.
- Expanding Metric Coverage: Introducing additional metrics to cover more dimensions of code quality and performance.
- Model Improvements: Experimenting with larger or specialized models to enhance code completion results.
- Automation: Developing scripts to streamline the data generation and analysis processes for scalability.

## Getting Started
1. Clone the repository.
```bash
git clone https://github.com/grach0v/CoCo.git
cd CoCo
```
2. Set up the environment.
```bash
conda create --name coco_env --file enironment.txt
conda activate coco_env
```
3. Open `analysis.ipynb` in Jupyter Notebook and run the cells to perform the analysis.
4. Carefuly read the source code, because I put a lot of effort into it.
5. Enjoy the project!


