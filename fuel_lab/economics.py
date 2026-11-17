"""汇总分配所对应的成本与碳强度，不替代资格判断。"""
def summarize(plan):
    rows=plan['allocations']
    quantity=sum(row['quantity'] for row in rows)
    cost=sum(row['quantity']*row['unit_cost'] for row in rows)
    emissions=sum(row['quantity']*row['intensity'] for row in rows)
    return {'delivered':quantity,'cost':round(cost,4),'emissions':round(emissions,4),
            'unit_cost':round(cost/quantity,4) if quantity else None,
            'unmet':sum(row['quantity'] for row in plan['unmet'])}
