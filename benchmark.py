import argparse
import sys
import os
import shutil
import csv
import pandas as pd
import time
import tracemalloc

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
  logFile.write(f'{modelName}\nRun Time (s): {runtime}\nMemory (B): {memory}\n\n')
  
# retrieving command line arguments and assigning to variables
args = check_arg(sys.argv[1:])
directory = args.directory
logFileName = args.logFileName

# calling functions to benchmark various models
enterDirectory(directory)
logFile = createLog(logFileName)
defaultKNN = benchmark('python3 defaultKNN.py', 'Default KNN')
optimizedKNN = benchmark('python3 optimizedKNN.py', 'Optimized KNN')
defaultSVM = benchmark('python3 defaultSVM.py', 'Default SVM')
optimizedSVM = benchmark('python3 optimizedSVM.py', 'Optimized SVM')
deepGAMI = benchmark('cd DeepGAMI && python -u DeepGamiTrain.py --input_files "./demo/expMat_filtered.csv,./demo/efeature_filtered.csv" '
                        '--disease_label_file "./demo/label_visual.csv" --num_fc_neurons "50" --latent_dim 100 --n_iter 100 --batch_size 30 '
                        '--learn_rate 0.001 --out_reg 0.005 --corr_reg 1 --epochs 100 --cross_validate="True" --model_type="fully_connect" '
                        '--save "." > "sc_MVC_result.txt" --norm_method "standard,standard" && '
                        'python -u DeepGamiTest_SM.py --input_file="./demo/test/independent_test_118_gexMat.csv" --model_file="./demo/run_92_best_model.pth" '
                        '--task="multiclass"', 'DeepGAMI')

