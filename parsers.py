def _parse_root(line):
    """Extracts the final root value from a line that contains '=' or '≈'.
    Returns the value as a string, or None if neither separator is found."""
    for sep in ['≈', '=']:
        if sep in line:
            try:
                return line.split(sep)[1].strip()
            except:
                pass
    return None


def parse_bisection_output(output):
    """Parses the stdout of bisection.exe into a list of iteration row dicts
    and the final root string. Each row contains: iter, xl, fxl, xu, fxu, xr, fxr, error."""
    rows, final_root = [], None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("I="):
            row = {}
            try:
                for part in line.split("|"):
                    part = part.strip()
                    if   part.startswith("I="):      row["iter"] = part.split("=")[1].strip()
                    elif part.startswith("XL="):     row["xl"]   = part.split("=")[1].strip()
                    elif part.startswith("F(Xl)="):  row["fxl"]  = part.split("=")[1].strip()
                    elif part.startswith("XU="):     row["xu"]   = part.split("=")[1].strip()
                    elif part.startswith("F(Xu)="):  row["fxu"]  = part.split("=")[1].strip()
                    elif part.startswith("XR="):     row["xr"]   = part.split("=")[1].strip()
                    elif part.startswith("F(XR)="):  row["fxr"]  = part.split("=")[1].strip()
                    elif "ERROR=" in part:           row["error"]= part.split("%")[1].strip() if "%" in part else ""
                rows.append(row)
            except Exception:
                pass
        elif "Final Root" in line:
            final_root = _parse_root(line)
    return rows, final_root

def parse_false_position_output(output):
    """Parses the stdout of false_position.exe into a list of iteration row dicts
    and the final root string. Each row contains: iter, xl, fxl, xu, fxu, xr, fxr, error."""
    rows, final_root = [], None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("I="):
            row = {}
            try:
                for part in line.split("|"):
                    part = part.strip()
                    if   part.startswith("I="):      row["iter"] = part.split("=")[1].strip()
                    elif part.startswith("XL="):     row["xl"]   = part.split("=")[1].strip()
                    elif part.startswith("F(Xl)="):  row["fxl"]  = part.split("=")[1].strip()
                    elif part.startswith("XU="):     row["xu"]   = part.split("=")[1].strip()
                    elif part.startswith("F(Xu)="):  row["fxu"]  = part.split("=")[1].strip()
                    elif part.startswith("XR="):     row["xr"]   = part.split("=")[1].strip()
                    elif part.startswith("F(XR)="):  row["fxr"]  = part.split("=")[1].strip()
                    elif "ERROR=" in part:           row["error"]= part.split("%")[1].strip() if "%" in part else ""
                rows.append(row)
            except Exception:
                pass
        elif "Final Root" in line:
            final_root = _parse_root(line)
    return rows, final_root


def parse_newton_output(output):
    """Parses the stdout of newton.exe into a list of iteration row dicts
    and the final root string. Each row contains: iter, xi, fxi, dfxi, error."""
    rows, final_root = [], None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("I="):
            row = {}
            try:
                for part in line.split("|"):
                    part = part.strip()
                    if   part.startswith("I="):       row["iter"] = part.split("=")[1].strip()
                    elif part.startswith("Xi="):      row["xi"]   = part.split("=")[1].strip()
                    elif part.startswith("F(Xi)="):   row["fxi"]  = part.split("=")[1].strip()
                    elif part.startswith("F'(Xi)="):  row["dfxi"] = part.split("=")[1].strip()
                    elif "ERROR=" in part:            row["error"]= part.split("%")[1].strip() if "%" in part else ""
                rows.append(row)
            except Exception:
                pass
        elif "Final Root" in line:
            final_root = _parse_root(line)
    return rows, final_root


def parse_secant_output(output):
    """Parses the stdout of secant.exe into a list of iteration row dicts
    and the final root string. Each row contains: iter, xim1, fxim1, xi, fxi, error."""
    rows, final_root = [], None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("I="):
            row = {}
            try:
                for part in line.split("|"):
                    part = part.strip()
                    if   part.startswith("I="):        row["iter"]  = part.split("=")[1].strip()
                    elif part.startswith("Xi-1="):     row["xim1"]  = part.split("=")[1].strip()
                    elif part.startswith("F(Xi-1)="):  row["fxim1"] = part.split("=")[1].strip()
                    elif part.startswith("Xi="):       row["xi"]    = part.split("=")[1].strip()
                    elif part.startswith("F(Xi)="):    row["fxi"]   = part.split("=")[1].strip()
                    elif "ERROR=" in part:             row["error"] = part.split("%")[1].strip() if "%" in part else ""
                rows.append(row)
            except Exception:
                pass
        elif "Final Root" in line:
            final_root = _parse_root(line)
    return rows, final_root


def parse_fixed_point_output(output):
    """Parses the stdout of simple_fixed_point.exe into a list of iteration row dicts
    and the final root string. Each row contains: iter, xi, gxi, error."""
    rows, final_root = [], None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("I="):
            row = {}
            try:
                for part in line.split("|"):
                    part = part.strip()
                    if   part.startswith("I="):      row["iter"] = part.split("=")[1].strip()
                    elif part.startswith("Xi="):     row["xi"]   = part.split("=")[1].strip()
                    elif part.startswith("G(Xi)="):  row["gxi"]  = part.split("=")[1].strip()
                    elif "ERROR=" in part:           row["error"]= part.split("%")[1].strip() if "%" in part else ""
                rows.append(row)
            except Exception:
                pass
        elif "Final Root" in line:
            final_root = _parse_root(line)
    return rows, final_root
