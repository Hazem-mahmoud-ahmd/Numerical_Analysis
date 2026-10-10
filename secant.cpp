#include <iostream>
#include <cmath>
#include <iomanip>
#include <string>
#include "muParser.h"

using namespace std;

double eps    = 0;
double error  = 0;
int    iter   = 1;
int    maxIter = 0;
bool   useEps = false;

mu::Parser parser;
double xVar = 0;

/* Evaluates f(x) at a given x by updating the shared variable
   that muParser references internally */
double f(double x) {
    xVar = x;
    return parser.Eval();
}

/* Recursively applies the Secant Method to approximate the root.
   Unlike Newton's method, no derivative is needed; the slope is
   approximated using two previous points:
       x_{i+1} = x_i - f(x_i) * (x_{i-1} - x_i) / (f(x_{i-1}) - f(x_i))
   xiMinus1 : the older of the two current points (x_{i-1})
   xi       : the more recent point (x_i)
   Returns the estimated root when the stopping condition is met */
double secant(double xiMinus1, double xi) {
    double fxm = f(xiMinus1);
    double fxi = f(xi);

    cout << fixed << setprecision(4);
    cout << "I=" << setw(2) << iter
         << " | Xi-1="    << setw(10) << xiMinus1
         << " | F(Xi-1)=" << setw(10) << fxm
         << " | Xi="      << setw(10) << xi
         << " | F(Xi)="   << setw(10) << fxi;

    if (iter > 1)
        cout << " | ERROR= %" << setw(8) << error;

    cout << endl;

    if (useEps  && iter > 1 && error <= eps) return xi;
    if (!useEps && maxIter > 0 && iter >= maxIter) return xi;

    if (abs(fxm - fxi) < 1e-12) {
        cout << "Division by zero in secant formula." << endl;
        return xi;
    }

    double xiNext = xi - (fxi * (xiMinus1 - xi)) / (fxm - fxi);
    error = abs((xiNext - xi) / xiNext) * 100;

    iter++;
    return secant(xi, xiNext);
}

/* Entry point: reads f(x), two initial points (xi-1, xi), and stopping
   condition (epsilon or max iterations) from stdin, then runs the secant method */
int main() {
    string line;

    cout << "Enter f(x): ";
    getline(cin, line);
    string fStr = line;

    try {
        parser.DefineVar("x", &xVar);
        parser.SetExpr(fStr);
    } catch (mu::Parser::exception_type &e) {
        cerr << "Parser error: " << e.GetMsg() << endl;
        return 1;
    }

    cout << "Enter xi-1: ";
    getline(cin, line);
    double xiMinus1 = stod(line);

    cout << "Enter xi: ";
    getline(cin, line);
    double xi = stod(line);

    cout << "Mode (e/i): ";
    getline(cin, line);
    char choice = line[0];

    cout << "Value: ";
    getline(cin, line);
    double stopVal = stod(line);

    if (choice == 'e') { useEps = true;  eps     = stopVal; }
    else               { useEps = false; maxIter = (int)stopVal; }

    cout << "\n--- Secant Method ---" << endl;
    double root = secant(xiMinus1, xi);
    cout << "\nFinal Root = " << root << endl;

    return 0;
}
