"""Energy consumption and tariff calculator for utility meters."""
import ast
import json
import math
import operator
from datetime import datetime

METERS = {}
RATES = [3.5, 5.0, 7.5]
SPIKE_LIMIT = 500
TIER_1_LIMIT = 100
TIER_2_LIMIT = 300

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval_node(node):
    """Evaluate a parsed arithmetic node (numbers and + - * / only)."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(
                node.value, bool):
            return node.value
        raise ValueError("only numbers are allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        return _BINARY_OPS[type(node.op)](
            _eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("unsupported expression")


def safe_eval(expression):
    """Safely evaluate a simple arithmetic expression such as '20 + 5*2'.

    Replaces eval(): anything other than numbers and + - * / is rejected.
    """
    return _eval_node(ast.parse(expression.strip(), mode="eval"))


def record_reading(meter_id, units, history=None):
    """Add a meter reading and return the history list of all readings.

    Raises ValueError if units is not a finite, non-negative number.
    """
    if history is None:
        history = []
    if (isinstance(units, bool) or not isinstance(units, (int, float))
            or not math.isfinite(units) or units < 0):
        raise ValueError(f"Invalid reading for {meter_id}: {units!r}")
    history.append((meter_id, units, str(datetime.now())))
    METERS[meter_id] = METERS.get(meter_id, 0) + units
    return history


def compute_bill(meter_id, tier_rates):
    """Return the three-tier bill for a meter (raises KeyError if unknown)."""
    units = METERS[meter_id]
    if units <= TIER_1_LIMIT:
        return units * tier_rates[0]
    if units <= TIER_2_LIMIT:
        return (TIER_1_LIMIT * tier_rates[0]
                + (units - TIER_1_LIMIT) * tier_rates[1])
    return (TIER_1_LIMIT * tier_rates[0]
            + (TIER_2_LIMIT - TIER_1_LIMIT) * tier_rates[1]
            + (units - TIER_2_LIMIT) * tier_rates[2])


def raise_rates(percent):
    """Increase every tariff rate by the given percentage (in place)."""
    factor = 1 + percent / 100
    RATES[:] = [rate * factor for rate in RATES]


def flag_spikes():
    """Return the ids of meters whose usage exceeds SPIKE_LIMIT."""
    return [meter for meter, units in METERS.items() if units > SPIKE_LIMIT]


def load_meter_data(file="meters.json"):
    """Load meter totals from a JSON file; start empty if unreadable."""
    try:
        with open(file, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    METERS.clear()
    METERS.update(data)


def save_meter_data(file="meters.json"):
    """Write the current meter totals to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(METERS, handle)


def main():
    """Demo run: record readings, bill them, flag spikes, save and reload."""
    history = []
    record_reading("M-01", 120, history)
    record_reading("M-02", 640, history)
    try:
        record_reading("M-03", -50, history)
    except ValueError as error:
        print("Rejected reading:", error)
    print("Readings stored so far:", len(history))
    raise_rates(10)
    rates = list(RATES)
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    try:
        print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    except KeyError:
        print("Bill M-03: no valid readings recorded")
    print("Spikes:", flag_spikes())
    adjustment = input(
        "Extra units for M-01 as an expression (Enter for 0): ") or "0"
    try:
        record_reading("M-01", safe_eval(adjustment), history)
    except (ValueError, SyntaxError, ZeroDivisionError) as error:
        print("Invalid expression, nothing added:", error)
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
