import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
import matplotlib.pyplot as plt

# Bayesian Network 
bn = gum.BayesNet('ElectiveRecommendation')

# Avariables Addition
favorite_subject = bn.add(gum.LabelizedVariable('FavoriteSubject', 'Favorite Subject', ['AI', 'Mathematics', 'Software', 'Autonomous']))
work_preference = bn.add(gum.LabelizedVariable('WorkPreference', 'Work Preference', ['Artificial', 'Robotics']))
semester = bn.add(gum.LabelizedVariable('Semester', 'Semester', ['winter', 'summer']))
schedule = bn.add(gum.LabelizedVariable('Schedule', 'Schedule', ['morning', 'afternoon']))
elective_preference = bn.add(gum.LabelizedVariable('ElectivePreference', 'Elective Preference', ['EP_AI', 'EP_MRC', 'EP_AST', 'EP_AMR']))

# List of electives subjects
electives = [
    'Bayesian_Inference_and_Gaussian_Process', 'Natural_Language_Processing', 
    'Deep_Learning_for_Robot_Vision', 'Deep_Learning_Foundations', 
    'Probabilistic_Reasoning', 'Robot_Manipulation', 
    'Entrepreneurship_in_Robotics_and_Computer_Science', 'Human_centered_interaction_in_robotics', 
    'Advanced_Control', 'Cognitive_Robotics', 
    'Multiagent_and_Agent_Systems', 'Learning_and_Adaptivity', 
    'Adaptive_Signal_Processing', 'Evolutionary_Computation_Theory_and_Application'
]

electives_available = bn.add(gum.LabelizedVariable('ElectivesAvailable', 'Electives Available', electives))
recommended_electives = bn.add(gum.LabelizedVariable('RecommendedElectives', 'Recommended Electives', electives))

# Relation between nodes
bn.addArc(favorite_subject, elective_preference)
bn.addArc(work_preference, elective_preference)
bn.addArc(elective_preference, electives_available)
bn.addArc(semester, electives_available)
bn.addArc(schedule, electives_available)
bn.addArc(electives_available, recommended_electives)

# Conditional probability tables (CPT)
# CPT for ElectivePreference based on favorite subjects and work preference
bn.cpt(elective_preference)[{'FavoriteSubject': 'AI', 'WorkPreference': 'Artificial'}] = [0.7, 0.1, 0.15, 0.05]
bn.cpt(elective_preference)[{'FavoriteSubject': 'AI', 'WorkPreference': 'Robotics'}] = [0.5, 0.2, 0.1, 0.2]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Mathematics', 'WorkPreference': 'Artificial'}] = [0.25, 0.5, 0.05, 0.2]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Mathematics', 'WorkPreference': 'Robotics'}] = [0.2, 0.4, 0.1, 0.3]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Software', 'WorkPreference': 'Artificial'}] = [0.1, 0.05, 0.8, 0.05]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Software', 'WorkPreference': 'Robotics'}] = [0.05, 0.3, 0.35, 0.3]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Autonomous', 'WorkPreference': 'Artificial'}] = [0.3, 0.15, 0.05, 0.5]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Autonomous', 'WorkPreference': 'Robotics'}] = [0.1, 0.25, 0.05, 0.6]



#print("CPT for ElectivePreference:")
#print(bn.cpt(elective_preference))

# CPT for ElectivesAvailable based on elective, semester, and schedule preferences
# EP_AI
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AI', 'Semester': 'winter', 'Schedule': 'morning'}] = [
    0.09, 0.40, 0.00, 0.00, 0.05, 0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AI', 'Semester': 'winter', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.40, 0.40, 0.00, 0.00, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AI', 'Semester': 'summer', 'Schedule': 'morning'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.10, 0.00, 0.60, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AI', 'Semester': 'summer', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.05, 0.00, 0.40, 0.05, 0.40
]

# EP_MRC
bn.cpt(electives_available)[{'ElectivePreference': 'EP_MRC', 'Semester': 'winter', 'Schedule': 'morning'}] = [
    0.4, 0.05, 0.00, 0.00, 0.05, 0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_MRC', 'Semester': 'winter', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_MRC', 'Semester': 'summer', 'Schedule': 'morning'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.60, 0.00, 0.20, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_MRC', 'Semester': 'summer', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.30, 0.00, 0.05, 0.60, 0.05
]

# EP_AST
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AST', 'Semester': 'winter', 'Schedule': 'morning'}] = [
    0.10, 0.10, 0.00, 0.00, 0.10, 0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AST', 'Semester': 'winter', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.30, 0.07, 0.00, 0.00, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AST', 'Semester': 'summer', 'Schedule': 'morning'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.10, 0.00, 0.40, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AST', 'Semester': 'summer', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.025, 0.025, 0.025, 0.025, 0.40, 0.025, 0.30
]

# EP_AMR
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AMR', 'Semester': 'winter', 'Schedule': 'morning'}] = [
    0.20, 0.05, 0.00, 0.00, 0.30, 0.50, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AMR', 'Semester': 'winter', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AMR', 'Semester': 'summer', 'Schedule': 'morning'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.60, 0.20, 0.00, 0.05, 0.00, 0.00, 0.00
]
bn.cpt(electives_available)[{'ElectivePreference': 'EP_AMR', 'Semester': 'summer', 'Schedule': 'afternoon'}] = [
    0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.50, 0.00, 0.15, 0.30, 0.05
]
# CPT for RecommendedElectives
for elective in electives:
    bn.cpt(recommended_electives)[{'ElectivesAvailable': elective}] = [1 if elective == e else 0 for e in electives]

# Save Bayesian Network
gum.saveBN(bn, 'ElectiveRecommendation.bif')



def recommend_subjects(user_preferences):

    favorite_subject = user_preferences["subject"]
    work_preference = user_preferences["work"]
    semester = user_preferences["semester"]
    schedule = user_preferences["schedule"]

    
    bn = gum.loadBN('ElectiveRecommendation.bif')

    # Inference Object
    ie = gum.LazyPropagation(bn)

    # Evidence for preference
    ie.setEvidence({
        'FavoriteSubject': favorite_subject,
        'WorkPreference': work_preference,
        'Semester': semester,
        'Schedule': schedule
    })

    # Inferece
    ie.makeInference()

    # probabilities of recommended subjects
    recommended = ie.posterior('RecommendedElectives')

    
    #print(recommended)

    #extracting labels and subjects
    variable = recommended.variable(0)  
    labels = variable.labels()           

    values = recommended[:]

    #extracting the top 3 subjects
    subject_probabilities = list(zip(labels, values))
    subject_probabilities.sort(key=lambda x: x[1], reverse=True)
    top_3_subjects = subject_probabilities[:3]

    subj1 = top_3_subjects[0][0].replace("_"," ")
    subj2 = top_3_subjects[1][0].replace("_"," ")
    subj3 = top_3_subjects[2][0].replace("_"," ")

    return subj1, subj2, subj3

'''
favorite_subject = input("Enter your favorite subject (AI, MRC, AST, AMR): ")
work_preference = input("Enter your work preference (AI, Robotics): ")
semester = input("Enter your semester preference (winter, summer): ")
schedule = input("Enter your preferred schedule(morning, afternoon): ")
'''
#user_preferences = {"subject": "Mathematics", "work": "Artificial", "schedule": "afternoon", "semester": "summer"}
#val1,val2,val3 = recommend_subjects(user_preferences)
#print(val1)
#print(val2)
#print(val3)


