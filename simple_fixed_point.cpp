#include <iostream>
#include <cmath>
#include <iomanip>
#include <string>
#include "muParser.h"

using namespace std;

double eps = 0, error = 0;
int iter = 1, maxIter = 0;
bool useEps = false;
mu::Parser parserG;
double xVar = 0;

/* Removes a trailing carriage return (\r) from a string,
   needed when reading lines on Windows where lines end in \r\n */
void trimLine(string &s) {
    if (!s.empty() && s.back() == '\r') s.pop_back();
}

/* Evaluates g(x) at a given x by updating the shared variable
   that muParser references internally */
double g(double x) { xVar = x; return parserG.Eval(); }

/* Recursively applies the Simple Fixed Point iteration:
       x_{i+1} = g(x_i)
   Convergence requires |g'(x)| < 1 near the root.
   xi : the current iterate
   Returns the estimated root when the stopping condition is met */
double fixedpoint(double xi) {
    double xiPlus1 = g(xi);
    if (iter > 1) error = abs((xiPlus1 - xi) / xiPlus1) * 100;

    cout << fixed << setprecision(4);
    cout << "I=" << setw(2) << iter
         << " | Xi="    << setw(10) << xi
         << " | G(Xi)=" << setw(10) << xiPlus1;
    if (iter > 1) cout << " | ERROR= %" << setw(8) << error;
    cout << endl;

    if (useEps  && iter > 1 && error <= eps) return xiPlus1;
    if (!useEps && maxIter > 0 && iter >= maxIter) return xiPlus1;

    iter++;
    return fixedpoint(xiPlus1);
}

/* Entry point: reads g(x), initial guess x0, and stopping condition
   (epsilon or max iterations) from stdin, then runs the fixed point iteration */
int main() {
    string line;

    getline(cin, line); trimLine(line);
    try {
        parserG.DefineVar("x", &xVar);
        parserG.SetExpr(line);
    } catch (mu::Parser::exception_type &e) {
        cerr << "Parser error: " << e.GetMsg() << endl; return 1;
    }

    getline(cin, line); trimLine(line); double x0 = stod(line);
    getline(cin, line); trimLine(line); char choice = line[0];
    getline(cin, line); trimLine(line); double stopVal = stod(line);

    if (choice == 'e') { useEps = true;  eps     = stopVal; }
    else               { useEps = false; maxIter = (int)stopVal; }

    cout << "\n--- Simple Fixed Point Method ---" << endl;
    double root = fixedpoint(x0);
    cout << "\nFinal Root = " << root << endl;
    return 0;
}
