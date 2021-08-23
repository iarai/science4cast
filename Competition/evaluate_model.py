import json, pickle
import numpy as np
from utils import calculate_ROC

from simple_model import link_prediction_semnet

if __name__ == '__main__':

    #
    # Loading the validation data.
    #
    # full_dynamic_graph_sparse
    #           The entire semantic network until 2014 (Validation,CompetitionRun=False) or 2017 (Evaluation&Submission,CompetitionRun=True).
    #           numpy array, each entry describes an edge in the semantic network.
    #           Each edge is described by three numbers [v1, v2, t], where the edge is formed at time t between vertices v1 and v2
    #           t is measured in days since the 1.1.1990
    #
    # unconnected_vertex_pairs
    #           numpy array of vertex pairs v1,v2 with deg(v1)>=10, deg(v2)>=10, and no edge exists in the year 2014 (2017 for CompetitionRun=True). 
    #           The question that the neural network needs to solve: Will an edge form?
    #
    # year_start
    #           year_start=2014 (2017 for CompetitionRun=True)
    #
    # years_delta
    #           years_delta=3
    #
    
    # Baseline model on the validation data 2014 -> 2017: AUC=0.723 (train: 0.739, test: 0.745)
    #                       evaluation data 2017 -> 2020: AUC=0.xxx (train: 0.879, test: 0.718)
    
    CompetitionRun=True
    if CompetitionRun:
        # Will create file for submission to competition.
        data_source='CompetitionSet2017_3.pkl'
        print('Evaluation Run -- please submit the created pkl file.')
    else:
        # Testing the model, for validation.
        print('Validation Run, testing the model.')
        data_source='TrainSet2014_3.pkl'
        data_solution='TrainSet2014_3_solution.pkl'
    
    with open(data_source, "rb" ) as pkl_file:
        full_dynamic_graph_sparse,unconnected_vertex_pairs,year_start,years_delta = pickle.load(pkl_file)
    
    
    
    # Transfer the data to the model, except of the solution.
    # The model should return a sorted index list of vertex-pairs from unconnected_vertex_pairs which will form an edge.
    # Sorted from most likely to most unlikely
    
    all_idx=link_prediction_semnet(full_dynamic_graph_sparse,
                                   unconnected_vertex_pairs,
                                   year_start,
                                   years_delta
                                   )
    
    
    if CompetitionRun==True:
        # Save the results for submission.
        submit_file="model_all_idx"+str(year_start)+"_"+str(years_delta)+".json"
        all_idx_list_float=list(map(float, all_idx))
        with open(submit_file, "w", encoding="utf8") as json_file:
            json.dump(all_idx_list_float, json_file)
        
        print("Solution stored as "+submit_file+". Looking forward to your submission.")        
    
    else:
        with open(data_solution, "rb" ) as pkl_file:
            unconnected_vertex_pairs_solution = pickle.load(pkl_file)
        
        AUC=calculate_ROC(all_idx, np.array(unconnected_vertex_pairs_solution))
        print('Area Under Curve for Evaluation: ', AUC,'\n\n\n')
