# Benchmarking Various Phenotype Prediction Tools

## Overview
This project utilizes multi-modal data (gene expression data and various physiological features) that can be used to train to classify cells by cortical layer (aka, phenotype prediction).
In addition to common machine learning models, there are select tools in the bioinformatics field that have been developed specifically for phenotype prediction. This project 
seeks to benchmark such tools to determine which tool has the overall best performance when evaluating accuracy/F1 score, memory usage, and run time. Additionally, it may
provide evidence that models that have been specifially designed for phenotype prediction using gene expression data perform better than generally-applicable ML models.

## Workflow
1. Reformat data to be compatible with various models/tools.
3. Train/test/optimize each model.
4. Benchmark each model using the same evaluation process.

## Selected Tools
- DeepGAMI (deep learning phenotype prediction tool that can use SNPs, RNA-Seq data, physiological features, or two together)
- G2PDeep (deep learning phenotype prediction tool)
- Traditional ML models: MLP, KNN, SVM (linear and rbf kernels)

## Running the Code
Clone this repo, ensure that all dependencies are installed, then run the following in the command line:
```
python3 benchmark.py -o outfile.txt
```

## Downloading and Formatting the Data
Data can be accessed through the DeepGAMI GitHub repository. Clone the repo as instructed in the Dependencies section below.
Once you have cloned the repo, run the following to make a master dataset that is compatible with the other (non-DeepGAMI) scripts:

```
python3 joinData.py -g DeepGAMI/demo/expMat_filtered.csv -p DeepGAMI/demo/efeature_filtered.csv -l DeepGAMI/demo/label_visual.csv
```

## Dependencies
- DeepGAMI: clone the repo --> `git clone https://github.com/daifengwanglab/DeepGAMI`
- pytorch
- scikit-learn
- scipy
- numpy
- pandas
- captum
- imblearn
- seaborn
- matplotlib
