import time

def fetch_time():
    tid = time.perf_counter()
    return tid

# ------------------- TESTE FUNKSJONER \/

# start_tid = fetch_time()

# sum_liste = []
# for i in range(1, 10000):
#     sum = 0
#     for n in range(1, i+1):
#         # print(f"n: {n}")
#         sum += n
#     sum_liste.append(sum)
#     # print(sum_liste)

# total_tid = fetch_time() - start_tid
# print(f"Total tid: {total_tid}")