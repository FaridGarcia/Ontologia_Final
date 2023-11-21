from owlready2 import *
import pandas as pd
    
    
onto = get_ontology("http://localhost:9000/StudentProfile.owl")
onto_student = get_ontology("http://localhost:9000/Student.owl")
onto_goal = get_ontology("http://localhost:9000/LearningGoal.owl")
onto_residence = get_ontology("http://localhost:9000/Residence.owl")
onto_type = get_ontology("http://localhost:9000/StudentType.owl")
onto_exp = get_ontology("http://localhost:9000/PreviousExperience.owl")
onto_knowledge = get_ontology("http://localhost:9000/PreviousKnowledge.owl")

onto.load()
onto_student.load()
onto_goal.load()
onto_residence.load()
onto_type.load()
onto_exp.load()
onto_knowledge.load()

print("\n\n================INTELLIGENT INVESTOR================")

print("\nImported ontologies: ")
print(onto.imported_ontologies)


print("\n\n====================================================")


file_path = "C:/Users/farid/OneDrive/Escritorio/Ontologia_Final/2022_Diagnóstico inicial -Cómo proteger a tus hijos en la red (Respuestas).xlsx"
data = pd.read_excel(file_path, sheet_name=4)


# print(list(onto_student.classes()))

# farid = onto_student.Student

# print(farid.iri)

# with onto_student:
#     farid = onto_student.Student("Farid")
#     farid.Document = ["12345"]
#     farid.Gender = ["M"]
    

# print(list(onto_student.individuals()))


for index, row in data.iterrows():
    with onto:
        
        #Creacion de estudiante con sus data properties
        student = onto_student.Student(row['student'])
        student.StudentName = [row['student_Name']]
        student.Document = [str(row['document'])]
        student.Mail = [row['mail']]
        student.Gender = [row['gender']]
        student.AgeRange = [row['age_Range']]


        #Creacion de profile y Relacion HasA
        profile = onto.StudentProfile(row['profile'])
        student.HasA.append(profile)
        
        
        #Relacion HasGoals
        goal = onto_goal.search(iri="*#Goal001")
        profile.HasGoals.append(goal[0])
                    
        
        #Relacion HasResidence
        if row['residence'] == 'Rural':
            residence = onto_residence.search(iri="*#Rural")
            profile.HasResidence.append(residence[0])
            
        else:
            residence = onto_residence.search(iri="*#Urban")
            profile.HasResidence.append(residence[0])
            
        
        #Relacion HasType    
        if row['type_Student'] == 'Familiar':
            type = onto_type.search(iri="*#Familiar")
            profile.HasStudentType.append(type[0])
        else:
            if row['type_Student'] == 'Teacher':
                type = onto_type.search(iri="*#Teacher")
                profile.HasStudentType.append(type[0])
                
                
            else:
                type = onto_type.search(iri="*#Other")
                profile.HasStudentType.append(type[0])
        
        
        #Relacion HasExp
        if row['previous_Experience'] == 'ExpFalse':   
            exp = onto_exp.search(iri="*#False")
            profile.HasExp.append(exp[0])
            
        else:
            exp = onto_exp.search(iri="*#True")
            profile.HasExp.append(exp[0])
        
        
        #Relacion HasKnowledge
        if row['knowledge'] == 'Basic':
            know = onto_knowledge.search(iri="*#Basic")
            profile.HasKnowledge.append(know[0])
            
        else:
            know = onto_knowledge.search(iri="*#Intermediate")
            profile.HasKnowledge.append(know[0])


       
rules = [
    ############### REGLAS PARA "ontoOnlyReasoner" ################################
     
        # #Regla de recomendacion de itinerario001
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#False),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary001)""",
        
        # #Regla de recomendacion de itinerario002
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#False),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary002)""",
        
        # #Regla de recomendacion de itinerario003
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary003)""",
        
        # #Regla de recomendacion de itinerario004
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary004)""",
        
        # #Regla de recomendacion de itinerario005
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Intermediate), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary005)""",
        
        # #Regla de recomendacion de itinerario006
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Intermediate), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary006)""",
        
        # #Regla de recomendacion de itinerario007
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#False),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary007)""",
        
        # #Regla de recomendacion de itinerario008
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#False),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary008)""",
        
        # #Regla de recomendacion de itinerario009
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Intermediate), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary009)""",
        
        # #Regla de recomendacion de itinerario010
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary010)""",
        
        # #Regla de recomendacion de itinerario011
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Intermediate), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary011)""",
        
        # #Regla de recomendacion de itinerario012
        # """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        # http://localhost:9000/StudentProfile#HasExp(?p, http://localhost:9000/PreviousExperience#True),
        # http://localhost:9000/StudentProfile#HasKnowledge(?p, http://localhost:9000/PreviousKnowledge#Basic), 
        # http://localhost:9000/StudentProfile#HasGoals(?p, http://localhost:9000/LearningGoal#Goal001), 
        # http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        # http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        # -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary012)"""
        
        
        
    ############### REGLAS PARA "ontoForRecommender" ################################
    
        #Regla de recomendacion de itinerario001, itinerario003 e itinerario005
        #Estudiantes con residencia "Rural" y con tipo "Familiar"
        """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary001),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary003),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary005)""",
        
        #Regla de recomendacion de itinerario002, itinerario004 e itinerario006
        #Estudiantes con residencia "Urban" y con tipo "Familiar"
        """http://localhost:9000/StudentProfile#StudentProfile(?p), 
        http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Familiar) 
        -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary002),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary004),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary006)""",
        
        #Regla de recomendacion de itinerario007, itinerario011 e itinerario012
        #Estudiantes con residencia "Rural" y con tipo "Teacher"
        """http://localhost:9000/StudentProfile#StudentProfile(?p),  
        http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Rural), 
        http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary007),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary011),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary012)""",
        
        #Regla de recomendacion de itinerario008, itinerario009 e itinerario010
        #Estudiantes con residencia "Urban" y con tipo "Teacher"
        """http://localhost:9000/StudentProfile#StudentProfile(?p),   
        http://localhost:9000/StudentProfile#HasResidence(?p, http://localhost:9000/Residence#Urban), 
        http://localhost:9000/StudentProfile#HasStudentType(?p, http://localhost:9000/StudentType#Teacher) 
        -> http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary008),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary009),
        http://localhost:9000/StudentProfile#RecommendsOne(?p, http://localhost:9000/Itinerary#Itinerary010)""",
    ]

with onto:
      
    for i, rule in enumerate(rules, start=1):
        imp = Imp()
        imp.set_as_rule(rule)
    
    sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True, debug=3)



#onto.save("ontoOnlyReasoner.owl")
#onto.save("ontoForRecommender.owl")
onto.save("ontoprueba.owl")