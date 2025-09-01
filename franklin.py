from ortools.init.python import init
from ortools.linear_solver import pywraplp


def main():
    print("Google OR-Tools version:", init.OrToolsVersion.version_string())

    # Crear el solver con GLOP
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("No se pudo crear el solver GLOP")
        return

    # Variables de decisión
    x_var = solver.NumVar(0, solver.infinity(), "x")  # x ≥ 0
    y_var = solver.NumVar(0, solver.infinity(), "y")  # y ≥ 0

    print("Número de variables =", solver.NumVariables())

    infinity = solver.infinity()

    # Restricción 1: x + y ≤ 4
    c1 = solver.Constraint(-infinity, 4, "ct1")
    c1.SetCoefficient(x_var, 1)
    c1.SetCoefficient(y_var, 1)

    # Restricción 2: 3x + 2y ≤ 12
    c2 = solver.Constraint(-infinity, 12, "ct2")
    c2.SetCoefficient(x_var, 3)
    c2.SetCoefficient(y_var, 2)

    print("Número de restricciones =", solver.NumConstraints())

    # Nueva función objetivo: 3x + 4y
    objective = solver.Objective()
    objective.SetCoefficient(x_var, 3)
    objective.SetCoefficient(y_var, 4)
    objective.SetMaximization()

    print(f"Resolviendo con {solver.SolverVersion()}")
    result_status = solver.Solve()

    print(f"Estado: {result_status}")
    if result_status != pywraplp.Solver.OPTIMAL:
        print("¡El problema no tiene una solución óptima!")
        return

    print("Solución:")
    print("Valor de la función objetivo =", objective.Value())
    print("x =", x_var.solution_value())
    print("y =", y_var.solution_value())


if __name__ == "__main__":
    init.CppBridge.init_logging("problema_modificado.py")
    cpp_flags = init.CppFlags()
    cpp_flags.stderrthreshold = True
    cpp_flags.log_prefix = False
    init.CppBridge.set_flags(cpp_flags)
    main()
