import matplotlib as mpl
import matplotlib.pyplot as plt
import json

# 1. 获取 Train Set 的数据
train_rel_fre_dict = {}
with open("nyt10_text.txt", 'r', encoding = 'utf-8') as f:
    # 2. 建立词频表
    for line in f.readlines():
        line = json.loads(line) # loads(字符串)， load(文件名字)
        if line['relation'] not in train_rel_fre_dict.keys():
            train_rel_fre_dict[line['relation']] = 1
        else:
            train_rel_fre_dict[line['relation']] += 1

# print("train set中的Relation个数：",len(train_rel_fre_dict))

# 3. 绘图
x = []
y = []
width = []
sort = sorted(train_rel_fre_dict.items(), key=lambda kv: (-kv[1])) # 按值排序
for i in sort:
    x.append(i[0])
    y.append(i[1])
    width.append(1)
plt.figure(figsize = [40, 10])
plt.bar(x,y,width, align='center', alpha=0.5, clip_on = True)
plt.ylim([0, 5000]) # 限制y轴数据的取值范围
plt.xlabel("relation name")
plt.ylabel("# of relation")
plt.title("WikidataNYT-- train_data -- relation number statistic")
plt.tick_params(axis='x', colors='red', length=13, width=3, rotation=90)
plt.savefig('wikidata_NYT_train.png')