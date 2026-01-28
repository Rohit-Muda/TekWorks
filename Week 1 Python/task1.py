project=int(input("Enter project marks:"))
internal=int(input("Enter internal marks:"))
external=int(input("Enter external marks:"))
total=0
if(project>49 and internal>49 and external>49):
    total=(0.70*project)+(0.10* internal)+(0.20*external)
    print("Your Score is:",total)
    if(total>=90):
        print("A")
    elif(total>=70):
        print("B")
    else:
        print("C")
else:
    if(project<50):
        print("Failed in project and score is:",project)
    if(internal<50):
        print("Failed in internal and score is:",internal);
    if(external<50): 
        print("Failed in external and score is:",external);
