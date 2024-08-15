import sqlite3

db = sqlite3.connect("fitnessTracker.db")
cursor = db.cursor()

# Create SQL tables to store the necessary data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercise_categories(
        exercise_name TEXT PRIMARY KEY,
        muscle_group TEXT,
        set_number INTEGER,
        rep_number INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS workout_routines(
        routine_name TEXT,
        exercise_name TEXT,
        set_number INTEGER,
        rep_number INTEGER,
        PRIMARY KEY (routine_name, exercise_name)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fitness_goals(
        goal_name TEXT PRIMARY KEY,
        description TEXT,
        target_date TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress(
        exercise_name TEXT,
        date TEXT,
        sets_completed INTEGER,
        reps_completed INTEGER
    )
''')
db.commit()

# Add some initial data
cursor.executemany('''INSERT OR IGNORE INTO exercise_categories VALUES(?,?,?,?)''', [
    ('Squat', 'Legs', 3, 10),
    ('Bench Press', 'Chest', 3, 8),
    ('Deadlift', 'Back', 4, 6)
])

cursor.executemany('''INSERT OR IGNORE INTO workout_routines VALUES(?,?,?,?)''', [
    ('Full Body Routine', 'Squat', 3, 10),
    ('Full Body Routine', 'Bench Press', 3, 8),
    ('Full Body Routine', 'Deadlift', 4, 6)
])

cursor.execute('''INSERT OR IGNORE INTO fitness_goals VALUES(?,?,?)''',
               ('Build Muscle', 'Gain 3 kg of muscle in 3 months', '2024-07-04'))

cursor.executemany('''INSERT OR IGNORE INTO progress VALUES(?,?,?,?)''', [
    ('Squat', '2023-07-01', 3, 10),
    ('Bench Press', '2023-07-02', 3, 8),
    ('Deadlift', '2023-07-03', 4, 6)
])

db.commit()

# Function for adding exercises


def add_exercise():
    print("Hi, This is the adding exercise category section!")
    try:
        exercise_name = input("Please enter the exercise name: ").strip()
        if not exercise_name:
            raise ValueError("Exercise name cannot be empty.")

        muscle_group = input("Please enter the muscle group: ").strip()
        if not muscle_group:
            raise ValueError("Muscle group cannot be empty.")

        set_number = int(input("Please enter the set number: "))
        rep_number = int(input("Please enter the rep number: "))

        if set_number <= 0 or rep_number <= 0:
            raise ValueError("Set and rep numbers must be positive integers.")

        cursor.execute('''INSERT INTO exercise_categories VALUES(?,?,?,?)''',
                       (exercise_name, muscle_group, set_number, rep_number))
        db.commit()
        print("Category was added SUCCESSFULLY!")
    except ValueError as ve:
        print(f"Error: {ve}")
    except sqlite3.IntegrityError:
        print("This exercise already exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function for viewing exercises


def view_exercise():
    print("Hi, This is the view exercise category section!")
    cursor.execute('''SELECT * FROM exercise_categories''')
    rows = cursor.fetchall()
    if rows:
        print("Exercise Categories:")
        for row in rows:
            print(f"Exercise Name: {row[0]}, Muscle Group: {row[1]}, Set Number: {row[2]}, Rep Number: {row[3]}")
    else:
        print("No exercises found.")

# Function for deleting exercises


def delete_exercise():
    print("Hi, This is the deleting exercise category section!")
    view_exercise()
    exercise_name = input("Please enter the exercise name you want to delete: ").strip()
    if exercise_name:
        cursor.execute('''DELETE FROM exercise_categories WHERE exercise_name = ?''', (exercise_name,))
        db.commit()
        if cursor.rowcount > 0:
            print(f"Exercise {exercise_name} was deleted SUCCESSFULLY!")
        else:
            print("Exercise not found.")
    else:
        print("Invalid input.")

# Function for creating workouts


def create_workout():
    print("Hi, This is the create workout routine section!")
    routine_name = input("Please enter the workout routine name: ").strip()
    if not routine_name:
        print("Routine name cannot be empty.")
        return
    while True:
        exercise_name = input("Please enter the exercise name (or 'done' to finish): ").strip()
        if exercise_name.lower() == 'done':
            break
        try:
            set_number = int(input("Please enter the set number: "))
            rep_number = int(input("Please enter the rep number: "))
            cursor.execute('''INSERT INTO workout_routines VALUES(?,?,?,?)''',
                           (routine_name, exercise_name, set_number, rep_number))
            db.commit()
        except ValueError:
            print("Please enter valid numeric values for set and rep numbers.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    print("Workout routine was created SUCCESSFULLY!")

# Function for viewing workouts


def view_workout():
    print("Hi, This is the view workout routine section!")
    cursor.execute('''SELECT DISTINCT routine_name FROM workout_routines''')
    routines = cursor.fetchall()
    if routines:
        print("Workout Routines:")
        for routine in routines:
            print(f"Routine Name: {routine[0]}")
            cursor.execute('''SELECT * FROM workout_routines WHERE routine_name = ?''', (routine[0],))
            exercises = cursor.fetchall()
            for exercise in exercises:
                print(f"  Exercise Name: {exercise[1]}, Set Number: {exercise[2]}, Rep Number: {exercise[3]}")
    else:
        print("No workout routines found.")

# Function for viewing exercise progress


def view_exercise_progress():
    print("Hi, This is the view exercise progress section!")
    cursor.execute('''SELECT * FROM progress''')
    rows = cursor.fetchall()
    if rows:
        print("Exercise Progress:")
        for row in rows:
            print(f"Exercise Name: {row[0]}, Date: {row[1]}, Sets Completed: {row[2]}, Reps Completed: {row[3]}")
    else:
        print("No progress records found.")

# Function for setting fitness goals


def set_fitness_goals():
    print("Hi, This is the set fitness goals section!")
    try:
        goal_name = input("Please enter the goal name: ").strip()
        if not goal_name:
            raise ValueError("Goal name cannot be empty.")

        description = input("Please enter the goal description: ").strip()
        if not description:
            raise ValueError("Description cannot be empty.")

        target_date = input("Please enter the target date (YYYY-MM-DD): ").strip()
        if not target_date:
            raise ValueError("Target date cannot be empty.")

        cursor.execute('''INSERT INTO fitness_goals VALUES(?,?,?)''',
                       (goal_name, description, target_date))
        db.commit()
        print("Fitness goal was set SUCCESSFULLY!")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function for viewing progress towards fitness goals


def view_progress_towards_fitness_goals():
    print("Hi, This is the view progress towards fitness goals section!")
    cursor.execute('''SELECT * FROM fitness_goals''')
    rows = cursor.fetchall()
    if rows:
        print("Fitness Goals:")
        for row in rows:
            print(f"Goal Name: {row[0]}, Description: {row[1]}, Target Date: {row[2]}")
    else:
        print("No fitness goals found.")

# User interface


def main_menu():
    while True:
        menu_choice = input('''\n--- Main Menu ---
1. Add Exercise Category
2. View Exercises
3. Delete Exercise
4. Create Workout Routine
5. View Workout Routine
6. View Exercise Progress
7. Set Fitness Goals
8. View Progress Towards Fitness Goals
9. Quit
:''')
        if menu_choice == '1':
            add_exercise()
        elif menu_choice == '2':
            view_exercise()
        elif menu_choice == '3':
            delete_exercise()
        elif menu_choice == '4':
            create_workout()
        elif menu_choice == '5':
            view_workout()
        elif menu_choice == '6':
            view_exercise_progress()
        elif menu_choice == '7':
            set_fitness_goals()
        elif menu_choice == '8':
            view_progress_towards_fitness_goals()
        elif menu_choice == '9':
            print("Goodbye!")
            db.close()
            break
        else:
            print("Invalid choice, please try again.")

# Run the main menu


main_menu()
