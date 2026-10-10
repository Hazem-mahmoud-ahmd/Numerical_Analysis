from flask import Flask, request, jsonify
from flask_cors import CORS
import os, signal, threading, time
from runners import (run_bisection, run_false_position, run_newton,
                     run_secant, run_fixed_point, differentiate_fx)
from parsers  import (parse_bisection_output, parse_false_position_output,
                      parse_newton_output, parse_secant_output,
                      parse_fixed_point_output)

app = Flask(__name__)
CORS(app)

last_heartbeat = time.time()

def heartbeat():
    """Updates the timestamp of the last received heartbeat ping.
    Called by the frontend every 5 seconds to keep the server alive."""
    global last_heartbeat
    last_heartbeat = time.time()
    return 'ok'

app.add_url_rule('/heartbeat', 'heartbeat', heartbeat, methods=['GET'])

def watchdog():
    """Background thread that terminates the server process if no heartbeat
    is received within 20 seconds (i.e. the browser tab was closed)."""
    while True:
        time.sleep(5)
        if time.time() - last_heartbeat > 20:
            os.kill(os.getpid(), signal.SIGTERM)

threading.Thread(target=watchdog, daemon=True).start()

@app.route('/solve/bisection', methods=['POST'])
def solve_bisection():
    """Receives bisection parameters (fx, xl, xu, mode, value) as JSON,
    runs bisection.exe, parses the output, and returns the iteration
    table rows and final root as JSON."""
    d = request.json
    out, err = run_bisection(d['fx'], d['xl'], d['xu'], d['mode'], d['value'])
    if not out: return jsonify({'error': err or 'bisection.exe not found'})
    rows, root = parse_bisection_output(out)    
    return jsonify({'rows': rows, 'root': root})

@app.route('/solve/false_position', methods=['POST'])
def solve_false_position():
    """Receives false position parameters (fx, xl, xu, mode, value) as JSON,
    runs false_position.exe, parses the output, and returns the iteration
    table rows and final root as JSON."""
    d = request.json
    out, err = run_false_position(d['fx'], d['xl'], d['xu'], d['mode'], d['value'])
    if not out: return jsonify({'error': err or 'false_position.exe not found'})
    rows, root = parse_false_position_output(out)
    return jsonify({'rows': rows, 'root': root})

@app.route('/solve/newton', methods=['POST'])
def solve_newton():
    """Receives Newton's method parameters (fx, x0, mode, value) as JSON,
    auto-differentiates f(x) via SymPy, runs newton.exe, parses the output,
    and returns the iteration table, final root, and derived f'(x) as JSON."""
    d = request.json
    df_display, df_muparser, err = differentiate_fx(d['fx'])
    if err: return jsonify({'error': f'Differentiation error: {err}'})
    out, err = run_newton(d['fx'], df_muparser, d['x0'], d['mode'], d['value'])
    if not out: return jsonify({'error': err or 'newton.exe not found'})
    rows, root = parse_newton_output(out)
    return jsonify({'rows': rows, 'root': root, 'dfx': df_display})

@app.route('/solve/secant', methods=['POST'])
def solve_secant():
    """Receives secant method parameters (fx, xi_minus, xi, mode, value) as JSON,
    runs secant.exe, parses the output, and returns the iteration
    table rows and final root as JSON."""
    d = request.json
    out, err = run_secant(d['fx'], d['xi_minus'], d['xi'], d['mode'], d['value'])
    if not out: return jsonify({'error': err or 'secant.exe not found'})
    rows, root = parse_secant_output(out)
    return jsonify({'rows': rows, 'root': root})

@app.route('/solve/fixed_point', methods=['POST'])
def solve_fixed_point():
    """Receives fixed point parameters (gx, x0, mode, value) as JSON,
    runs simple_fixed_point.exe, parses the output, and returns the iteration
    table rows and final root as JSON."""
    d = request.json
    out, err = run_fixed_point(d['gx'], d['x0'], d['mode'], d['value'])
    if not out: return jsonify({'error': err or 'simple_fixed_point.exe not found'})
    rows, root = parse_fixed_point_output(out)
    return jsonify({'rows': rows, 'root': root})

if __name__ == '__main__':
    print("Server running → http://localhost:5050")
    app.run(port=5050, debug=True)
