# Benchmarking Various Phenotype Prediction Tools

## Overview
This project utilizes an RNA-Seq dataset from the UCI Machine Learning Repository that can be used to train and test models for their ability to predict whether a patient has cancer.
In the bioinformatics field, there are many tools that have been developed specifically for phenotype prediction--in addition to common machine learning models. This project 
seeks to benchmark such tools to determine which tool has the overall best performance when evaluating accuracy/F1 score, memory usage, and run time. Additionally, it may
provide evidence that models that have been specifially designed for phenotype prediction using gene expression data perform better than generally-applicable ML models.

## Workflow
1. Download data (https://archive.ics.uci.edu/dataset/401/gene+expression+cancer+rna+seq)
2. Install necessary dependencies.
3. Train/test/optimize each model.
4. Benchmark each model using the same evaluation process.

## Selected Tools
- DeepGAMI (phenotype prediction tool that can use SNPs, RNA-Seq data, or both)
- G2PDeep (phenotype prediction tool)
- ML models: KNN, Logistic Regression, SVM (linear and rbf kernels)

## Running the Code
Clone this repo, ensure that all dependencies are installed, then run the following in the command line:
```
python3 benchmark.py -o outfile.txt
```

## Downloading the Data
Data can be accessed through the DeepGAMI GitHub repository. Clone the repo as instructed in the Dependencies section below. The data will be found in the "demo" folder.
Once you have cloned the repo, run the following to make a master dataset that is compatible with the other (non-DeepGAMI) scripts:
```
python3 joinData.py -g [Gene Expression Dataset Path] -p [Physiological Features Dataset Path] -l [Labels/Metadata File Path]
```

Ex. I ran the following:
```
python3 joinData.py -g DeepGAMI/demo/expMat_filtered.csv -p DeepGAMI/demo/efeature_filtered.csv -l DeepGAMI/demo/label_visual.csv
```

## Dependencies
- DeepGAMI (clone the repo: https://github.com/daifengwanglab/DeepGAMI)
- pytorch
- scikit-learn
- scipy
- numpy
- pandas
- captum
- imblearn
- MORE TO ADD
