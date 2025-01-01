# 日経ソフトウエア 2025年1月号 にあったナップサック問題の解法をPythonで実装してみた。
# 変数の意味合いが少しわかりづらかったので、listではなくdict型に置き換えてみました。
# numpyを使う意味はあまりないです。インデックスの指定が少し楽になるだけです。

import numpy as np


# 品物の種類 0はダミー indexとnameを一致させないとうまく動かないはず
ITEMS = [
    {'name': 0, 'weight': 0, 'value': 0 },
    {'name': 1,  'weight': 3, 'value': 400 },
    {'name': 2,  'weight': 4, 'value': 900 },
    {'name': 3,  'weight': 2, 'value': 200 },
    {'name': 4,  'weight': 5, 'value': 1200 },
    {'name': 5,  'weight': 1, 'value': 150 }
]

WEIGHT_LIMIT = 7

def default_value():
    return {"added": 0, "weight": 0, "value": 0}

def solve(items, max_weight):
    table = []
    for i in range(len(items)):
        item = items[i]
        if i == 0:
            table.append([default_value() for _ in range(max_weight + 1)])
        else:
            subtable = []
            for weight_limit in range(max_weight + 1):
                if weight_limit == 0:
                    subtable.append(default_value())
                else:
                    optimized_item = select_optimized_item(item, weight_limit, table, subtable)
                    subtable.append(optimized_item)
            
            table.append(subtable)
    
    table = np.array(table)
    return table

def can_add_item(item, weight_limit):
    return item["weight"] <= weight_limit

def has_more_value_if_added(item, weight_limit, table, subtable):
    return table[-1][weight_limit]["value"] > subtable[weight_limit - item["weight"]]["value"] + item["value"]

def new_item(item, weight_limit, subtable):
    return {
                "added" : item["name"],
                "weight": subtable[weight_limit-item["weight"]]["weight"] + item["weight"],
                "value" : subtable[weight_limit-item["weight"]]["value"]  + item["value"]
            }

def select_optimized_item(item, weight_limit, table, subtable):
    # 追加で入れられる場合、入れた場合と上の行の結果を比較して大きい方を選ぶ
    if can_add_item(item, weight_limit):
        if has_more_value_if_added(item, weight_limit, table, subtable):
            return table[-1][weight_limit].copy()
        else:
            return new_item(item, weight_limit, subtable)
    #追加で入れられない場合、入れない場合と上の行の結果を比較して大きい方を選ぶ
    else:
        if table[-1][weight_limit]["value"] > subtable[weight_limit-1]["value"]:
            return table[-1][weight_limit].copy()
        else:
            return subtable[weight_limit - 1].copy()

def unpack(table, items):
    p = [-1, -1]
    value = table[p[0], p[1]]["value"]
    weight = table[p[0], p[1]]["weight"]

    last_item = items[table[p[0], p[1]]["added"]]

    while value > 0:
        last_item = items[table[p[0], p[1]]["added"]]
        if last_item["name"] == items[p[0]]["name"]:
            p[1] -= last_item["weight"]
            print("{}を取り出した。残りは{}kgで{}円".format(
                                                last_item["name"],
                                                weight - last_item["weight"],
                                                value  - last_item["value"]))
        else:
            p[0] = last_item["name"]

        value = table[p[0], p[1]]["value"]
        weight = table[p[0], p[1]]["weight"]
    

if __name__ == '__main__':

    table = solve(ITEMS, WEIGHT_LIMIT)
    unpack(table, ITEMS)