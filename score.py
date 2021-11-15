f = open("answers.csv", "r")
answers = sorted(f.read().split("\n"))
f.close()

f = open("result.csv", "r")
results = sorted(f.read().split("\n"))
f.close()

answers = [s for s in answers if s]
results = [s for s in results if s]
score = 0.0
for i in range(len(answers)):
    ans_fname = answers[i].split(";")[0]
    for j in range(len(results)):
        res_fname = results[j].split(";")[0].split(".")[0]
        if res_fname == ans_fname:
            ans_vals = answers[i].split(";")
            res_vals = results[j].split(";")
            name = ans_vals[0]
            s = name + ": "
            if ans_vals[-1] == res_vals[-1]:
                score += 0.5
                s += "correct; "
            else:
                s += "incorrect; "
        
            ans_vals = [int(v) for v in ans_vals[1:-1]]
            res_vals = [int(v) for v in res_vals[1:-1]]
    
            res_area = (res_vals[2] - res_vals[0]) * (res_vals[3] - res_vals[1])
            intersec = [0,0,0,0]
            if (res_vals[0] >= ans_vals[2]) or (res_vals[1] >= ans_vals[3]) or (res_vals[2] <= ans_vals[0]) or (res_vals[3] <= ans_vals[1]):
                intersec_area = 0
            else:
                intersec[0] = max(res_vals[0], ans_vals[0])
                intersec[1] = max(res_vals[1], ans_vals[1])
                intersec[2] = min(res_vals[2], ans_vals[2])
                intersec[3] = min(res_vals[3], ans_vals[3])
                intersec_area = (intersec[2] - intersec[0]) * (intersec[3] - intersec[1])
        
            seg_score = float(intersec_area) / float(res_area)
            score += seg_score / 2.0
    
            s += "score = " + str(seg_score)
            print(s)
    
print("Total score: " + str(score * 5) + " / 100")
