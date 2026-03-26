from logic import *

# List of characters and political systems
characters = ["Holden", "Alex", "Miller", "Naomi"]
systems = ["Belters", "OPA", "MCRN", "UN"]

# Create variables for every (character, system) pair
variables = {}
for c in characters:
    for s in systems:
        # creating a variable like Holden_UN
        # each one is a true/false statement
        variables[(c, s)] = Variable(f"{c}_{s}")

constraints = []

# Rule 1: each character belongs to exactly one system
for c in characters:
    # at least one system must be true
    constraints.append(
        Or(*[variables[(c, s)] for s in systems])
    )

    # they cannot belong to two systems at the same time
    for s1 in systems:
        for s2 in systems:
            if s1 != s2:
                constraints.append(
                    ~(variables[(c, s1)] & variables[(c, s2)])
                )

# Rule 2: each system is assigned to exactly one character
for s in systems:
    # at least one character must have this system
    constraints.append(
        Or(*[variables[(c, s)] for c in characters])
    )

    # two characters cannot share the same system
    for c1 in characters:
        for c2 in characters:
            if c1 != c2:
                constraints.append(
                    ~(variables[(c1, s)] & variables[(c2, s)])
                )

# Given facts from the problem

# Holden is part of the United Nations
constraints.append(variables[("Holden", "UN")])

# Naomi is either Belters or OPA
constraints.append(
    variables[("Naomi", "Belters")] | variables[("Naomi", "OPA")]
)

# Miller is NOT part of MCRN
constraints.append(
    ~variables[("Miller", "MCRN")]
)

# Combine all constraints into one big logical expression
knowledge = And(*constraints)

print("Valid solutions:\n")

# Loop through all possible truth assignments
for row in truth_table_rows(knowledge.variables()):
    # Check which ones satisfy all constraints
    if knowledge.evaluate(**row):
        solution = []

        # Collect only the true assignments
        for (c, s), var in variables.items():
            if row[str(var)]:
                solution.append(f"{c} -> {s}")

        print(solution)
