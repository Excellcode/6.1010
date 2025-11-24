def calculate_my_grade():
    """
    Calculates your total grade based on a detailed list of assignments.
    You can edit the 'earned' and 'possible' scores in the list
    to see how your grade changes.
    """

    # --- EDIT YOUR SCORES HERE ---
    # This list contains all assignments.
    # 'earned' is your score.
    # 'possible' is the max score for the assignment.
    # 'category' is the weighting group from your syllabus.
    
    assignments = [
        # == Group and Prep Finger Exercises (10% Weight) ==
        # -- Items from original gradebook --
        {'name': '3.2 Lec 2 Group', 'category': 'FEprepgroup', 'earned': 7, 'possible': 7},
        {'name': '2.3 Lec 3 Prep', 'category': 'FEprepgroup', 'earned': 5, 'possible': 5},
        {'name': '2.4 Lec 4 Prep', 'category': 'FEprepgroup', 'earned': 8, 'possible': 8},
        {'name': '3.4 Lec 4 Group', 'category': 'FEprepgroup', 'earned': 4, 'possible': 4},
        {'name': '2.6 Lec 6 Prep', 'category': 'FEprepgroup', 'earned': 1, 'possible': 1},
        {'name': '3.5 Lec 6 Group', 'category': 'FEprepgroup', 'earned': 3, 'possible': 3},
        {'name': '2.7 Lec 7 Prep', 'category': 'FEprepgroup', 'earned': 8, 'possible': 9},
        {'name': '2.8 Lec 8 Prep', 'category': 'FEprepgroup', 'earned': 3, 'possible': 3},
        {'name': '3.8 Lec 9 Group', 'category': 'FEprepgroup', 'earned': 2, 'possible': 9},
        {'name': '2.10 Lec 10 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 4},
        {'name': '3.9 Lec 10 Group', 'category': 'FEprepgroup', 'earned': 4, 'possible': 4},
        {'name': '2.14 Lec 14 Prep', 'category': 'FEprepgroup', 'earned': 6, 'possible': 6},
        
        # -- Missing items (scored as 0) from gradebook screenshot --
        {'name': '2.2 Lec 2 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 13},
        {'name': '3.3 Lec 3 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 2},
        {'name': '2.11 Lec 11 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 2},
        {'name': '3.10 Lec 14 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 1},
        {'name': '3.11 Lec 15 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 2},
        {'name': '3.12-14 Lec 15 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 26},
        { 'name': '3.15 Lec 15 Group', 'category': 'FEprepgroup', 'earned': 2, 'possible': 2},
        
       
        
        # -- Items from list with no questions/points (assumed 0/0) --
        # These are included for completeness but do not affect the grade.
        {'name': '2.1 Lec 1 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '2.5 Lec 5 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '2.9 Lec 9 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '2.12 Lec 12 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '2.13 Lec 13 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '2.15 Lec 15 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '2.16 Lec 17 Prep', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '3.1 Lec 1 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '3.6 Lec 7 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},
        {'name': '3.7 Lec 8 Group', 'category': 'FEprepgroup', 'earned': 0, 'possible': 0},


        # == Solo Finger Exercises (30% Weight) ==
        {'name': '4.1 Lec 3 Solo', 'category': 'FEsolo', 'earned': 100, 'possible': 100},
        {'name': '4.2 Lec 4 Solo', 'category': 'FEsolo', 'earned': 66.67, 'possible': 100},
        {'name': '4.3 Lec 5 Solo', 'category': 'FEsolo', 'earned': 160, 'possible': 200},
        {'name': '4.5 Lec 8 Solo', 'category': 'FEsolo', 'earned': 100, 'possible': 100},
        {'name': '4.6 Lec 10 Solo - Fixed', 'category': 'FEsolo', 'earned': 33.34, 'possible': 100},
        {'name': '4.6 Lec 10 Solo', 'category': 'FEsolo', 'earned': 0, 'possible': 0},
        {'name': '4.7 Lec 11 Solo', 'category': 'FEsolo', 'earned': 33.33, 'possible': 100},
        {'name': '4.10 Lec 16 Solo', 'category': 'FEsolo', 'earned': 100, 'possible': 100},
        {'name': '4.13 Lec 15 Solo', 'category': 'FEsolo', 'earned': 200, 'possible': 200},
        
        # -- Missing items (scored as 0) from gradebook screenshot --
        {'name': '4.4 Lec 7 Solo', 'category': 'FEsolo', 'earned': 0, 'possible': 100},
        {'name': '4.8 Lec 12 Solo', 'category': 'FEsolo', 'earned': 0, 'possible': 100},
        {'name': '4.9 Lec 15 Solo', 'category': 'FEsolo', 'earned': 0, 'possible': 100},
        {'name': '4.11 Lec 15 Solo', 'category': 'FEsolo', 'earned': 0, 'possible': 200},
        {'name': '4.12 Lec 15 Solo', 'category': 'FEsolo', 'earned': 0, 'possible': 100},
        
        
        # == Pset Functionality (27% Weight) ==
        {'name': '5.1 PS1 Func', 'category': 'Pset Functionality', 'earned': 100, 'possible': 100},
        {'name': '5.2 PS2 Func', 'category': 'Pset Functionality', 'earned': 94, 'possible': 100}, # Scored as 0
        
        
        # == Pset Style (6% Weight) ==
        {'name': 'Pset 1 Style', 'category': 'Pset Style', 'earned': 100, 'possible': 100},
        {'name': 'Pset 2 Style', 'category': 'Pset Style', 'earned': 100, 'possible': 100}, # Scored as 0
        
        
        # == Pset Checkoffs (27% Weight) ==
        {'name': 'Check-off 1', 'category': 'Pset Checkoffs', 'earned': 95.45, 'possible': 100},
        {'name': 'Check-off 2', 'category': 'Pset Checkoffs', 'earned': 100, 'possible': 100}, # Scored as 0
        {'name': 'Check-off 3', 'category': 'Pset Checkoffs', 'earned': 40, 'possible': 100}, # Scored as 0
        {'name': 'Check-off 4', 'category': 'Pset Checkoffs', 'earned': 100, 'possible': 100}, # Scored as 0
    ]

    # --- Grade Calculation Logic ---
    
    # 1. Define weights
    weights = {
        "FEprepgroup": 0.10,
        "FEsolo": 0.30,
        "Pset Functionality": 0.27,
        "Pset Style": 0.06,
        "Pset Checkoffs": 0.27
    }

    # 2. Calculate totals for each category
    totals = {}
    for item in assignments:
        category = item['category']
        if category not in totals:
            totals[category] = {'earned': 0, 'possible': 0}
        
        totals[category]['earned'] += item['earned']
        totals[category]['possible'] += item['possible']

    # 3. Calculate final grade
    total_grade = 0
    
    print("--- Grade Calculation (What-If: Missing = 0) ---")
    print("\n" + "="*50)
    print(f"{'Category':<25} | {'Weight':<7} | {'Points':<12} | {'Average':<7}")
    print("-"*50)

    for category, scores in totals.items():
        weight = weights.get(category, 0)
        
        # Avoid division by zero if a category has no possible points
        if scores['possible'] == 0:
            category_avg = 0.0
        else:
            category_avg = scores['earned'] / scores['possible']
        
        category_contribution = category_avg * weight
        total_grade += category_contribution
        
        # Print table row
        points_str = f"{scores['earned']:.2f}/{scores['possible']:.2f}"
        avg_str = f"{category_avg*100:.2f}%"
        weight_str = f"{weight*100:.0f}%"
        print(f"{category:<25} | {weight_str:<7} | {points_str:<12} | {avg_str:<7}")

    print("="*50)
    print(f"TOTAL GRADE: {total_grade * 100:.2f}%")
    print("="*50)


# --- Run the calculation ---
calculate_my_grade()