import numpy as np

def extended_problem(configs = {}):
    restrictions = configs["restrictions"]
    if len(restrictions) < 3:
        return None

    ref = []
    output = []
    #Separe inferior limit and normal restrictions
    for i in range(0, len(restrictions)):
        r = restrictions[i]
        if is_inferior_limit_restriction(r):
            output.append(r.copy())
        else:
            ref.append(r.copy())
    
    #Count the number of adicional variables
    adicional_vars = 0
    for restriction in ref:
        c = restriction["coeficients"]
        match(restriction["type"]):
            case "<=":
                adicional_vars+=1
            case ">=":
                adicional_vars+=2

    #Update the restriction coeficients
    length = len(ref[0]["coeficients"])
    for i in range(0, len(output)):
        output[i]["coeficients"] = output[i]["coeficients"].__add__(np.zeros(adicional_vars).tolist())
    
    total_length = length + adicional_vars
    for i in range(length, total_length):
        c = np.zeros(total_length)
        c[i] = 1
        output.append({"coeficients": c, "type":">=", "value": 0})

    pos = length
    for restriction in ref:
        c = restriction["coeficients"]
        new_c = c.__add__(np.zeros(adicional_vars).tolist())

        match(restriction["type"]):
            case "<=":
                new_c[pos] = 1
                pos+=1
            case ">=":
                new_c[pos] = 1
                new_c[pos+1] = "M"
                pos+=2

        output.append({"coeficients": new_c, "type":"=", "value": restriction["value"]})
    
    return output

def normalize_restriction(restriction, ref_index):
    r = restriction.copy()
    c = np.array(r["coeficients"])
    ref_value = c[ref_index]
    c = c / ref_value
    r["coeficients"] = c.tolist()
    r["value"] /= ref_value
    return r

def primal_to_dual(configs = {}):
    output = []
    return output

def is_inferior_limit_restriction(restriction):
    var_index = -1
    c = restriction["coeficients"]
    for i in range(0, len(c)):
        if c[i] == 1:
            if var_index != 1:
                var_index = i
            else:
                return False
        elif c[i] != 0:
            return False
    
    return restriction["type"] == ">="