#include <iostream>
#include <cmath>
#include <iomanip>
#include <string>
#include <muParser.h>

using namespace std;

mu::Parser muF, muDF;
double muX = 0;

/* Removes a trailing carriage return (\r) from a string,
   needed when reading lines on Windows where lines end in \r\n */
void trimLine(string &s) {
    if (!s.empty() && s.back() == '\r') s.pop_back();
}

/* Evaluates f(x) at a given x using the muParser instance for f */
double f(double x)  { muX = x; return muF.Eval(); }

/* Evaluates f'(x) at a given x using the muParser instance for f' */
double df(double x) { muX = x; return muDF.Eval(); }

/* Entry point: reads f(x), f'(x) (pre-computed by SymPy), initial guess x0,
   and stopping condition from stdin, then iterates Newton's formula:
       x_{i+1} = x_i - f(x_i) / f'(x_i)
   until the condition (max iterations or error threshold) is met */
int main() {
    string fStr, dfStr, line;

    getline(cin, fStr);  trimLine(fStr);
    getline(cin, dfStr); trimLine(dfStr);
    getline(cin, line);  trimLine(line); double x0 = stod(line);
    getline(cin, line);  trimLine(line); char modeChar = line[0];
    getline(cin, line);  trimLine(line); double stopVal = stod(line);

    try {
        muF.DefineVar("x", &muX);  muF.SetExpr(fStr);
        muDF.DefineVar("x", &muX); muDF.SetExpr(dfStr);
    } catch (mu::Parser::exception_type &e) {
        cout << "Parser error: " << e.GetMsg() << endl;
        return 1;
    }

    cout << "\n--- Newton Method ---\n" << fixed << setprecision(4);

    double xi = x0, error = 0;
    int i = 1;

    while (true) {
        double fxi = f(xi), dfxi = df(xi);

        cout << "I=" << setw(2) << i
             << " | Xi="     << setw(10) << xi
             << " | F(Xi)="  << setw(10) << fxi
             << " | F'(Xi)=" << setw(10) << dfxi;

        if (i > 1) cout << " | ERROR= %" << setw(8) << error;
        cout << endl;

        if (modeChar == 'i' && i >= (int)stopVal) break;
        if (modeChar == 'e' && i > 1 && error <= stopVal) break;

        if (abs(dfxi) < 1e-12) { cout << "Derivative too small." << endl; break; }

        double xiPlus1 = xi - (fxi / dfxi);
        error = abs((xiPlus1 - xi) / xiPlus1) * 100;
        xi = xiPlus1;
        i++;
    }

    cout << "\nFinal Root = " << xi << endl;
    return 0;
}
