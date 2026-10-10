#include <muParser.h>
#include <iostream>
#include <cmath>
#include <iomanip>
#include <string>

using namespace std;

double eps    = 0;
double error  = 0;
int    iter   = 1;
int    maxIter = 0;

mu::Parser parser;
double xVal = 0;

/* Evaluates f(x) at a given x by updating the shared variable
   that muParser references internally */
double f(double x) {
    xVal = x;
    return parser.Eval();
}

/* Recursively applies the False Position (Regula Falsi) Method.
   Unlike bisection, the new point xr is computed using a linear
   interpolation between xl and xu rather than the midpoint.
   xl      : current left bracket
   xu      : current right bracket
   xrOld   : xr from the previous iteration (used for error %)
   Returns the estimated root when the stopping condition is met */
double falsePosition(double xl, double xu, double xrOld = 0) {
    double xr = xu - (f(xu) * (xl - xu) / (f(xl) - f(xu)));

    if (iter > 1)
        error = abs((xr - xrOld) / xr) * 100;

    cout << fixed << setprecision(4);
    cout << "I=" << setw(2) << iter
        << " | XL=" << setw(8) << xl
        << " | F(Xl)=" << setw(9) << f(xl)
        << " | XU=" << setw(8) << xu
        << " | F(Xu)=" << setw(9) << f(xu)
        << " | XR=" << setw(8) << xr
        << " | F(XR)=" << setw(9) << f(xr);

    if (iter > 1)
        cout << " | ERROR= %" << setw(8) << error;

    cout << endl;

    if (eps != 0 && iter > 1 && error <= eps) return xr;

    if (maxIter != 0 && iter >= maxIter) {
        cout << "Maximum iterations reached." << endl;
        return xr;
    }

    if (f(xl) * f(xr) < 0) xu = xr;
    else xl = xr;

    iter++;
    return falsePosition(xl, xu, xr);
}

/* Entry point: reads f(x), bracket [xl, xu], and stopping condition
   (epsilon or max iterations) from stdin, then runs the false position method */
int main() {
    string expression_str, line;
    double xl, xu;

    cout << "--- False Position Method ---" << endl;
    cout << "Enter f(x): ";
    getline(cin, expression_str);

    try {
        parser.DefineVar("x", &xVal);
        parser.SetExpr(expression_str);
    } catch (mu::Parser::exception_type &e) {
        cout << "Error: " << e.GetMsg() << endl;
        return 1;
    }

    cout << "Enter xl: ";
    getline(cin, line);
    xl = stod(line);

    cout << "Enter xu: ";
    getline(cin, line);
    xu = stod(line);

    cout << "Mode (e/i): ";
    getline(cin, line);
    char choice = line[0];

    switch (choice) {
        case 'e':
            cout << "Enter epsilon: ";
            getline(cin, line);
            eps = stod(line);
            break;
        case 'i':
            cout << "Enter max iterations: ";
            getline(cin, line);
            maxIter = stoi(line);
            break;
        default:
            cout << "Invalid choice. Exiting." << endl;
            return 1;
    }

    if (f(xl) * f(xu) < 0) {
        double root = falsePosition(xl, xu);
        cout << "\nFinal Root = " << root << endl;
    } else {
        cout << "No root found in the given interval." << endl;
    }

    return 0;
}
