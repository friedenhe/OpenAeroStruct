from __future__ import print_function

# Append the parent directory to the system path so we can call those Python
# files. If you have OpenAeroStruct in your PYTHONPATH, this is not necessary.
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from run_classes import OASProblem
from time import time
import numpy as np

# Set problem type
prob_dict = {'type' : 'aerostruct',
             'optimize' : False, # Don't optimize, only perform analysis
             'record_db' : True,
             }

# Instantiate problem and add default surface
OAS_prob = OASProblem(prob_dict)

# Create a dictionary to store options about the surface.
# Here we have 3 twist control points and 3 thickness control points.
# We also set the discretization, span, and panel spacing.
surf_dict = {'name' : 'wing',
             'symmetry' : True,
             'num_y' : 7,
             'num_x' : 2,
             'num_twist_cp' : 3,
             'num_thickness_cp' : 3,
             'num_chord_cp' : 2,
             'wing_type' : 'CRM',
             'CD0' : 0.015,
             'span_cos_spacing' : 0.,
             }

# Add the specified wing surface to the problem
OAS_prob.add_surface(surf_dict)

# Set up the problem. Once we have this done, we can modify the internal
# unknowns and run the multidisciplinary analysis at that design point.
OAS_prob.add_desvar('wing.twist_cp')
OAS_prob.add_desvar('wing.thickness_cp')
OAS_prob.add_desvar('wing.chord_cp')
OAS_prob.setup()

# Define a function that calls the already set-up problem
def run_aerostruct(twist_cp, thickness_cp, alpha, root_chord, taper_ratio):
    OAS_prob.prob['alpha'] = alpha
    OAS_prob.prob['wing.twist_cp'] = twist_cp
    OAS_prob.prob['wing.thickness_cp'] = thickness_cp
    OAS_prob.prob['wing.chord_cp'] = np.array([taper_ratio, 1.]) * root_chord
    OAS_prob.run()

    return OAS_prob.prob['fuelburn'], OAS_prob.prob['wing_perf.structural_weight'], OAS_prob.prob['wing_perf.L'], OAS_prob.prob['total_weight'], OAS_prob.prob['wing_perf.failure']

# These would be the inputs to the black box
alpha = 4.
twist_cp = np.linspace(-5., 5., 3)
thickness_cp = np.ones((3)) * 0.05
root_chord = 1.
taper_ratio = 1.

# Actually run the analysis
fuelburn, structural_weight, lift, total_weight, failure = run_aerostruct(twist_cp, thickness_cp, alpha, root_chord, taper_ratio)

print('fuelburn:          {:18.5f} kg'.format(fuelburn))
print('structural_weight: {:18.5f} N '.format(structural_weight))
print('lift:              {:18.5f} N'.format(lift))
print('total_weight:      {:18.5f} N'.format(total_weight))
print('failure:           {:18.5f}'.format(failure)) # Needs to be <0 to not fail
