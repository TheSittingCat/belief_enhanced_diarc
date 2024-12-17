# Belief Enhanced DIARC

This is the GitHub Repo for the implementation of DIARC with the LLM based belief maintainer. The belief maintainer is deployed as a TRADE Service that can both be used individually or as a part of a larger DIARC program through DIARC configurations. 

## Requirements

In order to install all the Python requirements, from the high level directory run the command

'''
pip -r requirements.txt
'''

This should install the required packages for the purposes of this project. 

### Windows Installation

Note that PyTrade-Wrapper requires Numpy 2.0.2 which is incompatible with Windows machines as it was never properly released for Windows machines and relied on MinGW compilation to work. As such, it is possible to crash the library if you specifically try to install that version on a Windows machine. 

To avoid this error, it is possible to install the latest versions of Numpy and Jpype and force the Python package manager to skip the dependency check. To do this, perform the following: 

1- Install PyTrade-Wrapper
2- Install Numpy and Jpype with

'''
pip install --no-deps numpy
pip install --no-deps jpype1
'''

Alternatively, you can also install numpy and Jpype1 first and then install PyTrade-Wrapper with no dependencies, but in that case additional libraries might have to be installed as well. 

In addition to the aforementioned Python libraries, all installation versions require Metric-FF which in turn requires Flex and Bison libraries. Please see [Link][https://github.com/Vidminas/metric-ff-crossplatform] for MinGW installation of the required libraries. We additionally include the executables to these libraries in the "metric-ff" folder. 

Prior to the execution of the program, the PyTrade library should also be set up, please see [Link][https://pypi.org/project/pyTRADE-wrapper/] for detailed steps on how to set it up in a DIARC based environment. 

## Execution

This Repository contains a number of contributions to the original DIARC code that are mostly salf-contained and can be run in isolation. Based on your requirements, the following modules can be executed. 

Additionally, all evaluation and training steps require the TextWorld KG dataset for proper execution. Please see [Link][https://github.com/MikulasZelinka/textworld_kg_dataset] for access to this dataset. Extract all dataset files to Data/KG folder for the purposes of evaluation and make sure that they are named `test_dataset.json`, `valid_dataset.json` and `test_dataset.json`.

### Evaluation Replication 

To run the evaluation pipeline for any openai based model (not only GPT-4o-mini), execute the eval.py file located at Python/eval.py. Don't forget to replace the `model` value in `get_answer` function with your own model such `gpt-4o-mini`. Note that this requires an active OpenAI API key. 
 

### Training Replication

The run the training pipeline for any openai based model (not only GPT-4o-mini), first execute the train.py file located at Python/train.py in order to prepare the training requirements, and then run the perform_train.py file located at Python/perform_train.py. Note that as perform_train creates a new OpenAI model instance, it is best to inform us before the training process so we provide the adequate model id for testing purposes. 

### Analysis

The analysis are mostly self-contained and can be run directly, it is possible to run performance_analysis.py located at Python/performance_analysis.py to produce the figures as seen in the report. Additionally, it is possible to run training_analysis.py located at Python/training_analysis.py and training_data_analysis.py located at Python/training_data_analysis.py to run training based error and statistical analysis. 

Please note that training_data_analysis.py requires the tiktoken library for the correct execution which in turn loads an OpenAI BPE tokenizer and is computationally heavy. As such, I recommend running it in a Google Colab notebook rather than locally. If you wish to run the analysis file locally, the required library can be installed with `pip install tiktoken`. 

### TRADE Service

The TRADE Service can be started (or executed) by running the llm_belief_updater.py file from core\src\main\java\edu\tufts\hrilab\slug\parsing\llm\llm_belief_updater.py. Note that as of this version, a bug exists that intermittently prevents the Python TRADE service to be cross registered with the original DIARC TRADE. Once a new version of PyTrade is released, we will make updates to fix this bug and use the latest PyTrade capabilities. Until then, we suggest the direct execution of the Trade Service via `trade.call` functionality as seen in llm_belief_updater.py. Otherwise, it is also possible to call the registered Trade Service directly from a DIARC configuration file or component as another TRADE service. 

## Contrbituions

All contributions, including code contributions not directly used in the execution or towards preamble files or backend requirements can be viewed at [Link][https://github.com/TheSittingCat/belief_enhanced_diarc/commits/main/] filterable by user where the usernames correspond to real persons as follows: 

'''
thesittingcat -> Kaveh Eskandari Miandoab
bluebobcat -> Clea Demuynck
jujis -> Juliana Alscher
Sulfruos -> Arvind Pillai
'''

In addition, the following additions and differences exist between two repositories (the original and belief enhanced):

'''
eval.py
perform_train.py
performance_analysis.py
read_kg_data.py
train.py
training_analysis.py
training_data_analysis.py
llm_belief_updater.py
LLMBeliefUpdater.java
BeliefUpdateLLM.java
projConfig.java
couting.py
belief_system_reader.py
testing .pl files
testing .asl files
'''

Given the extent of additions, it is recommended to use the whole DIARC repository as the base for this one, however, it is also possible to copy the related files to their respective folders and execute directly from DIARC. 