import numpy as np
import random
from math import inf


class Params:
    pass

class Particle:
    """
    Represents a particle of the Particle Swarm Optimization algorithm.
    """
    def __init__(self,lower_bound,upper_bound):
        """
        Creates a particle of the Particle Swarm Optimization algorithm.

        :param lower_bound: lower bound of the particle position.
        :type lower_bound: numpy array.
        :param upper_bound: upper bound of the particle position.
        :type upper_bound: numpy array.
        """
        delta=upper_bound-lower_bound
        self.x=np.random.uniform(lower_bound,upper_bound)
        self.v=np.random.uniform(-delta,delta)
        self.bp=self.x
        self.value=-inf
        self.best_value=-inf

class ParticleSwarmOptimization:
    """
    Represents the Particle Swarm Optimization algorithm.
    Hyperparameters:
        inertia_weight: inertia weight.
        cognitive_parameter: cognitive parameter.
        social_parameter: social parameter.

    :param hyperparams: hyperparameters used by Particle Swarm Optimization.
    :type hyperparams: Params.
    :param lower_bound: lower bound of particle position.
    :type lower_bound: numpy array.
    :param upper_bound: upper bound of particle position.
    :type upper_bound: numpy array.
    """
    def __init__(self, hyperparams,lower_bound,upper_bound):
        # Todo: implement
        self.particles=[]
        for i in range(hyperparams.num_particles):
            self.particles.append(Particle(lower_bound,upper_bound))
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.delta=upper_bound-lower_bound
        self.best_position_idx=0
        self.num=hyperparams.num_particles
        self.w=hyperparams.inertia_weight
        self.phip= hyperparams.cognitive_parameter
        self.phig= hyperparams.social_parameter
        self.evaluate_idx=0

    def get_best_position(self)->np.ndarray:
        """
        Obtains the best position so far found by the algorithm.

        :return: the best position.
        :rtype: numpy array.
        """
        # Todo: implement
        return self.particles[self.best_position_idx].bi

    def get_best_value(self)->float:
        """
        Obtains the value of the best position so far found by the algorithm.

        :return: value of the best position.
        :rtype: float.
        """
        # Todo: implement
        return  self.particles[self.best_position_idx].best_value

    def get_position_to_evaluate(self)->np.ndarray:
        """
        Obtains a new position to evaluate.

        :return: position to evaluate.
        :rtype: numpy array.
        """
        return self.particles[self.evaluate_idx].x
        # Todo: implement
        #return self.lower_bound  # Remove this line

    def advance_generation(self)->None:
        """
        Advances the generation of particles. Auxiliary method to be used by notify_evaluation().
        """
        for i in range(self.num):
            rp=random.uniform(0,1)
            rg=random.uniform(0,1)
            self.particles[i].v=self.w*self.particles[i].v+rp*self.phip*(self.particles[i].bp-self.particles[i].x)+rg*self.phig*(self.particles[self.best_position_idx].bi-self.particles[i].x)
            self.particles[i].v=np.clip(self.particles[i].v,-self.delta,self.delta)
            self.particles[i].x=np.clip(self.particles[i].x+self.particles[i].v,self.lower_bound,self.upper_bound)
            


    def notify_evaluation(self, value:float)->None:
        """
        Notifies the algorithm that a particle position evaluation was completed.

        :param value: quality of the particle position.
        :type value: float.
        """
        self.particles[self.evaluate_idx].value=value
        if value>self.particles[self.evaluate_idx].best_value:
            self.particles[self.evaluate_idx].best_value=value
            self.particles[self.evaluate_idx].bi=self.particles[self.evaluate_idx].x
        if value>self.particles[self.best_position_idx].best_value:
            self.best_position_idx=self.evaluate_idx
        if self.evaluate_idx==self.num-1:
            self.advance_generation()
        self.evaluate_idx=(self.evaluate_idx+1)%self.num