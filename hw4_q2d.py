import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Function to filter non-inferior solutions
def filter_non_inferior_solutions(df):
    non_inferior_df = df.groupby(["Optimal x", "Optimal y"]).apply(lambda group: group.loc[group["Z_grand"].idxmax()])
    return non_inferior_df

# Create a Gurobi model
model = gp.Model("MultiObjectiveProblem")

# Define decision variables
x = model.addVar(name="x", vtype=GRB.CONTINUOUS, lb=0)
y = model.addVar(name="y", vtype=GRB.CONTINUOUS, lb=0)

# Add constraints
model.addConstr(x + y <= 10, name="constraint1")
model.addConstr(x - y <= 6, name="constraint2")
model.addConstr(y <= 8, name="constraint3")

# Initialize an empty DataFrame to store results
results_df = pd.DataFrame(columns=["Alpha", "Optimal x", "Optimal y", "Z1", "Z2", "Z_grand"])

# choose number of alpha values 
n = 6

# Iterate over different values of alpha
for alpha in range(0, n):  # alpha ranges from 0 to 10
    alpha /= len(range(0,n))  # Convert alpha to a float between 0 and 1

    # Set the objectives
    Z1 = x + y
    Z2 = 0.5*x + y

    # Scalarization: Combine the objectives into a single objective
    Z = alpha * Z1 - (1 - alpha) * Z2

    # Maximize the combined objective
    model.setObjective(Z, sense=GRB.MAXIMIZE)

    # Optimize the model
    model.optimize()

    # Store results in the DataFrame
    results_df = results_df.append({
        "Alpha": alpha,
        "Optimal x": x.x,
        "Optimal y": y.x,
        "Z1": Z1.getValue(),
        "Z2": Z2.getValue(),
        "Z_grand": model.objVal
    }, ignore_index=True)

print('\n\n\n')
print(results_df)
print('\n\n\n')

# Filter non-inferior solutions
non_inferior_df = filter_non_inferior_solutions(results_df)

# Display the filtered results
print('These are the unique non-inferior solutions found in the process\n')
print(non_inferior_df)

print('\n\n\n')