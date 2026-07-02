# Student Record Management System

dictionary = {}

def add_func():

  name = input ("Name :")
  age = int(input("Age: "))
  roll_no = int(input("Roll No: "))
  course  = input("Course : ")
  dictionary[roll_no] = [name,age,course]

def search():

    search = int(input("Enter roll_no :"))
    if search in dictionary:
        print(dictionary[x])
    else:
        print("No record found")

def update():

    search = int(input("Enter roll_no :"))
    if search in dictionary:
        name = input ("Name :")
        age = int(input("Age: "))
        course  = input("Course : ")
        dictionary[search] = [name,age,course]
        
    else:
        print("No record found")

def delete():
    search = int(input("Enter roll_no :"))
    if search in dictionary:
      del dictionary[x]  
    else:
        print("No record found")  

while True:

  choice  = int(input("1:Add Student\n2:View All Students\n3:Search Student\n4:Update Student Information\n5:Delete Student\n6. Quit\n"))

  if choice == 1:
    add_func()

  elif choice == 2:

    print(f"Total Students: {len(dictionary.keys())}\n")
    for x,y in dictionary.items():
      print("------------------------")
      print(f"{x} : {y}")
  
  elif choice == 3:

    search()

  elif choice == 4:

    update()
    
  elif choice == 5:
    
    delete()

  elif choice == 6:
    break
  else:
    print("Invalid Input")
