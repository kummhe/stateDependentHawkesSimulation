#Market simulator class
import os
import numpy as np
import pandas as pd
from mpoints.hybrid_hawkes_exp import HybridHawkesExp
from mpoints import plot_tools
import seaborn  # for good-looking plots
from IPython.display import set_matplotlib_formats  # set the figures format to svg
set_matplotlib_formats('svg')

class MarketSimulator:

    def __init__(self, phis, nus, alphas, betas, n_events, n_states, events_labels, states_labels) -> None:
        
        #Variables are saved to refresh simulation at each change of state
        self.phis          = phis
        self.nus           = nus
        self.alphas        = alphas
        self.betas         = betas
        self.n_events      = n_events
        self.n_states      = n_states
        self.events_labels = events_labels
        self.states_labels = states_labels

        self.res_times  = []
        self.res_events = []
        self.res_states = []
        
        self.time_start = 0
        self.time_end   = 7200

        #First initialization of the model
        self.model = HybridHawkesExp(n_events, n_states, events_labels, states_labels)
        self.model.set_transition_probabilities(phis)
        self.model.set_hawkes_parameters(nus, alphas, betas)
        print("[MarketSimulation] Model initialized. Running simulation with startup parameters")

    def GetNextEvent(self, currentState: int) -> dict:
        
        #Generate new event
        times, events, states = self.model.simulate(self.time_start, self.time_end, None, None, None, None,
                                                                   currentState, max_number_of_events=1)
        #Append event to results
        self.res_times.append(times[0])
        self.res_events.append(events[0])
        self.res_states.append(states[0])

        dict = {"event_type" : events[0], "event_time" : times[0], "event_state" : states[0] }

        return dict
    
    def DumpSimulationResult(self) -> None:
        print ("[MarketSimulation]", self.res_times, self.res_events, self.res_states)

    def SaveResults(self) -> None:
        df = pd.DataFrame()
        df["times"] = self.res_times
        df["events"] = self.res_events
        df["states"] = self.res_states

        df.to_csv("results.csv")
