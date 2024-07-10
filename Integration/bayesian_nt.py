import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
import matplotlib.pyplot as plt

# Crear la red bayesiana
bn = gum.BayesNet('ElectiveRecommendation')

# Añadir variables
favorite_subject = bn.add(gum.LabelizedVariable('FavoriteSubject', 'Favorite Subject', ['AI', 'Mathematics', 'Software', 'Autonomous']))
work_preference = bn.add(gum.LabelizedVariable('WorkPreference', 'Work Preference', ['Artificial', 'Robotics']))
semester = bn.add(gum.LabelizedVariable('Semester', 'Semester', ['winter', 'summer']))
schedule = bn.add(gum.LabelizedVariable('Schedule', 'Schedule', ['morning', 'afternoon']))
elective_preference = bn.add(gum.LabelizedVariable('ElectivePreference', 'Elective Preference', ['EP_AI', 'EP_MRC', 'EP_AST', 'EP_AMR']))

# Materias electivas basadas en la imagen
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

# Añadir arcos
bn.addArc(favorite_subject, elective_preference)
bn.addArc(work_preference, elective_preference)
bn.addArc(elective_preference, electives_available)
bn.addArc(semester, electives_available)
bn.addArc(schedule, electives_available)
bn.addArc(electives_available, recommended_electives)

# Definir tablas de probabilidad condicional (CPT)
# CPT para ElectivePreference basadas en las materias favoritas y preferencia de trabajo
bn.cpt(elective_preference)[{'FavoriteSubject': 'AI', 'WorkPreference': 'Artificial'}] = [0.7, 0.1, 0.15, 0.05]
bn.cpt(elective_preference)[{'FavoriteSubject': 'AI', 'WorkPreference': 'Robotics'}] = [0.5, 0.2, 0.1, 0.2]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Mathematics', 'WorkPreference': 'Artificial'}] = [0.25, 0.5, 0.05, 0.2]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Mathematics', 'WorkPreference': 'Robotics'}] = [0.2, 0.4, 0.1, 0.3]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Software', 'WorkPreference': 'Artificial'}] = [0.1, 0.05, 0.8, 0.05]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Software', 'WorkPreference': 'Robotics'}] = [0.05, 0.3, 0.35, 0.3]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Autonomous', 'WorkPreference': 'Artificial'}] = [0.3, 0.15, 0.05, 0.5]
bn.cpt(elective_preference)[{'FavoriteSubject': 'Autonomous', 'WorkPreference': 'Robotics'}] = [0.1, 0.25, 0.05, 0.6]

# CPT para ElectivesAvailable basado en las preferencias de electiva, semestre y horario
# Ajustar las probabilidades de acuerdo a los datos específicos de la imagen
# Imprimir CPT de ElectivePreference
print("CPT for ElectivePreference:")
print(bn.cpt(elective_preference))


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
# CPT para RecommendedElectives
for elective in electives:
    bn.cpt(recommended_electives)[{'ElectivesAvailable': elective}] = [1 if elective == e else 0 for e in electives]

# Guardar la red bayesiana
gum.saveBN(bn, 'ElectiveRecommendation.bif')



def recommend_subjects(user_preferences):

    favorite_subject = user_preferences["subject"]
    work_preference = user_preferences["work"]
    semester = user_preferences["semester"]
    schedule = user_preferences["schedule"]

        # Cargar la red bayesiana
    bn = gum.loadBN('ElectiveRecommendation.bif')

    # Crear el objeto de inferencia
    ie = gum.LazyPropagation(bn)

    # Establecer la evidencia para las nuevas preferencias
    ie.setEvidence({
        'FavoriteSubject': favorite_subject,
        'WorkPreference': work_preference,
        'Semester': semester,
        'Schedule': schedule
    })

    # Realizar la inferencia
    ie.makeInference()

    # Obtener las probabilidades de las materias recomendadas
    recommended = ie.posterior('RecommendedElectives')

    # Mostrar las probabilidades de las materias recomendadas
    print(recommended)

    variable = recommended.variable(0)  # obtener la primera variable
    labels = variable.labels()           # obtener las etiquetas de la variable

    values = recommended[:]

    # Crear una lista de tuples (materia, probabilidad)
    subject_probabilities = list(zip(labels, values))

    # Ordenar la lista de tuples por probabilidad en orden descendente
    subject_probabilities.sort(key=lambda x: x[1], reverse=True)

    # Obtener las tres probabilidades más altas con el respectivo nombre de la materia
    top_3_subjects = subject_probabilities[:3]

    subj1 = top_3_subjects[0][0].replace("_"," ")
    subj2 = top_3_subjects[1][0].replace("_"," ")
    subj3 = top_3_subjects[2][0].replace("_"," ")

    return subj1, subj2, subj3

'''
favorite_subject = input("Ingrese su materia favorita (AI, MRC, AST, AMR): ")
work_preference = input("Ingrese su preferencia de trabajo (AI, Robotics): ")
semester = input("Ingrese el semestre preferido (winter, summer): ")
schedule = input("Ingrese su horario preferido (morning, afternoon): ")
'''
#user_preferences = {"subject": "Mathematics", "work": "Artificial", "schedule": "afternoon", "semester": "summer"}
#val1,val2,val3 = recommend_subjects(user_preferences)
#print(val1)
#print(val2)
#print(val3)


