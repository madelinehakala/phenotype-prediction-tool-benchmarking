import argparse
import sys
import os
import shutil
import csv
import pandas as pd
import time
import tracemalloc
import seaborn as sns

def check_arg(args = None):
	'''Parses command line arguments.'''
	parser = argparse.ArgumentParser(description = 'Pipeline for scRNA-Seq analysis.')
	parser.add_argument('-d', '--directory',
		help = 'Directory where data and scripts are stored',
		required = 'True'
		)	
	parser.add_argument('-l', '--logFileName',
		help = 'Desired Log File Name',
		required = 'True'
		)
	return parser.parse_args(args)

def enterDirectory(directory):
  os.chdir(directory)
  
def createLog(logFileName):
  '''Creates an empty log file where run info will be stored.'''
  logFile = open(logFileName, 'w')
  return logFile

def trackRuntime(command):
  '''Tracks the run time of a command.'''
  startTime = time.time()
  os.system(command)
  stopTime = time.time()
  runTime = (stopTime - startTime)
  return runTime
  
def trackMemoryUsage(command):
  '''Tracks the peak memory usage of a command.'''
  tracemalloc.start()
  os.system(command)
  memory = tracemalloc.get_traced_memory()[1]
  return memory

def benchmark(command, modelName):
  '''Calls the runtime and memory usage functions to benchmark a command.'''
  runtime = trackRuntime(command)
  memory = trackMemoryUsage(command)
  logFile.write(f'{modelName},{runtime},{memory}\n')
  
# retrieving command line arguments and assigning to variables
args = check_arg(sys.argv[1:])
directory = args.directory
logFileName = args.logFileName

# calling functions to benchmark various models
enterDirectory(directory)
logFile = createLog(logFileName)
logFile.write('model,runtime_s,memory_b\n')
defaultKNN = benchmark('python3 defaultKNN.py', 'Default_KNN')
optimizedKNN = benchmark('python3 tunedKNN.py', 'Tuned_KNN')
defaultSVM = benchmark('python3 defaultSVM.py', 'Default_SVM')
optimizedSVM = benchmark('python3 tunedSVM.py', 'Tuned_SVM')
defaultMLP = benchmark('python3 defaultMLP.py', 'Default_MLP')
tunedMLP = benchmark('python3 tunedMLP.py', 'Tuned_MLP')
deepGAMI = benchmark('cd DeepGAMI && python -u DeepGamiTrain.py --input_files "./demo/expMat_filtered.csv,./demo/efeature_filtered.csv" '
                        '--disease_label_file "./demo/label_visual.csv" --num_fc_neurons "50" --latent_dim 100 --n_iter 100 --batch_size 30 '
                        '--learn_rate 0.001 --out_reg 0.005 --corr_reg 1 --epochs 100 --cross_validate="True" --model_type="fully_connect" '
                        '--save "." > "sc_MVC_result.txt" --norm_method "standard,standard" && '
                        'python -u DeepGamiTest_SM.py --input_file="./demo/test/independent_test_118_gexMat.csv" --model_file="./demo/run_92_best_model.pth" '
                        '--task="multiclass"', 'DeepGAMI')


# reading results
results = pd.read_csv(f'{logFileName}')
results['F1'] = [0.46, 0.46, 0.50, 0.53, 0.49, 0.55, 0.57] # adding column for F1 scores as they were calculated in other scripts

# plotting run time
runtimePlot = sns.barplot(data = results, x = 'model', y = 'runtime_s')
runtimePlot.set(xlabel = 'Model', ylabel = 'Run Time (s)')
runtimePlot.set_xticklabels(runtimePlot.get_xticklabels(), rotation = 30)
getRuntimePlot = runtimePlot.get_figure()
getRuntimePlot.tight_layout()
getRuntimePlot.savefig('runtime.png')

# plotting memory usage
memoryPlot = sns.barplot(data = results, x = 'model', y = 'memory_b')
memoryPlot.set(xlabel = 'Model', ylabel = 'Peak Memory Usage (B)')
memoryPlot.set_xticklabels(memoryPlot.get_xticklabels(), rotation = 30)
getMemoryPlot = memoryPlot.get_figure()
getMemoryPlot.tight_layout()
getMemoryPlot.savefig('memory.png')

# plotting f1
f1Plot = sns.barplot(data = results, x = 'model', y = 'F1')
f1Plot.set(xlabel = 'Model', ylabel = 'F1 Score')
f1Plot.set_xticklabels(f1Plot.get_xticklabels(), rotation = 30)
f1Plot = f1Plot.get_figure()
f1Plot.tight_layout()
f1Plot.savefig('f1.png')

