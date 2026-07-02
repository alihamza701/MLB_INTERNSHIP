import numpy as np

name = input("Name:")
Class = input("Class:")

subjects = []
score = []
counter = int(input("How many subjects you are studying? "))
i=1
while i<=counter:
  a = input("Subjects: ")
  subjects.append(a)
  i+=1

i=0
while i<counter:
  print("\n" ,subjects[i] , ":")
  a = float(input("Score "))
  score.append(a)
  i+=1

avg = np.mean(score)

if avg >= 90:
  grade = "A"
elif avg >= 80:
  grade = "B"
elif avg >= 70:
  grade = "C"
elif avg >= 60:
  grade = "D"
else:
  grade = "F"
print("\n" , name , "You got: " , grade)