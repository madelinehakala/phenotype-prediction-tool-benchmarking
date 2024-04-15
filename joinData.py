import argparse
import sys
import pandas as pd


def check_arg(args = None):
	'''Parses command line arguments.'''
	parser = argparse.ArgumentParser(description = 'Making a multi-modal mouse cortical layer master dataset.')
	parser.add_argument('-g', '--geneExpressionDatasetPath',
		help = 'Path to the gene expression dataset',
		required = 'True'
		)	
	parser.add_argument('-p', '--physiologicalFeaturesDatasetPath',
		help = 'Path to the physiological features dataset',
		required = 'True'
		)	
	parser.add_argument('-l', '--labelsMetadataPath',
		help = 'Path to the metadata file with class labels',
		required = 'True'
		)
	return parser.parse_args(args)

# retrieving command line arguments and assigning to variables
args = check_arg(sys.argv[1:])
geneExpression = args.geneExpressionDatasetPath
physioFeatures = args.physiologicalFeaturesDatasetPath
labelMetadata = args.labelsMetadataPath

# reading gene expression data and mutating as needed
geneExpressionData = pd.read_csv(geneExpression)
geneExpressionData = geneExpressionData.set_index('Unnamed: 0').transpose().reset_index().rename(columns = {'index': 'cell'})

# reading physiological features data
physioFeaturesData = pd.read_csv(physioFeatures)
physioFeaturesData = physioFeaturesData.rename(columns={'Unnamed: 0': 'cell'})

# merging two datasets via left join
allFeatures = geneExpressionData.merge(physioFeaturesData, on = 'cell', how = 'left')

# reading labels metadata and dropping unneeded columns
labels = pd.read_csv(labelMetadata)
labels['label'].replace({'02/03/22': '2/3'}, inplace = True)
labels.drop('ttype', axis = 1, inplace = True)
labels.drop('ttype_sub', axis = 1, inplace = True)

# merging data with labels
allFeaturesWithLabels = allFeatures.merge(labels, on = 'cell', how = 'left')
allFeaturesWithLabels = allFeaturesWithLabels.rename(columns = {'label': 'cortical_layer_class_label'})
allFeaturesWithLabels.to_csv('mouse_cortical_layers.csv', index = False) # writing to csv
