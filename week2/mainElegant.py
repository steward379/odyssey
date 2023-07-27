print("\n")
print("========= Task 1 =========")
# Task 1

def find_and_print(messages):
    key_outcome = [key for key, value in messages.items() 
                   if any( term in value 
                           for term in ['college', 'legal', 'vote'] +
                           [str(age) for age in range(18, 200)]
                  )]
    for key in key_outcome:
        print(key)
    return key_outcome  

#   [str(age) in value for age in range(18, 200)]
#list comprehension

print(find_and_print({
    "Bob": "My name is Bob. I'm 18 years old.",
    "Mary": "Hello, glad to meet you.",
    "Copper": "I'm a college student. Nice to meet you.",
    "Leslie": "I am of legal age in Taiwan.",
    "Vivian": "I will vote for Donald Trump next week",
    "Jenny": "Good morning."
}))

print("========= Task 2 =========")
# Task 2

# get
# f 相當於反引號，可以直接將變數 {} 放入字串中不需要 $

def calculate_sum_of_bonus(data):
    # def convert_salary(salary):
    #     if isinstance(salary, str):
    #         if 'USD' in salary:
    #             salary = int(salary.replace('USD', '')) * 30
    #         else:
    #             salary = int(salary.replace(',', ''))
    #     return salary

    bonus_rates = {
            "above average": 2, 
            "average": 1, 
            "below average": 0.5
        }

    employees = [
        {
            "name": employee["name"],
            "salary": int(employee["salary"].replace('USD', '')) * 30 
                      if isinstance(employee["salary"], str) and 'USD' in employee["salary"] 
                      else int(employee["salary"].replace(',', '')) 
                      if isinstance(employee["salary"], str) 
                      else employee["salary"],
            "rate": bonus_rates.get(employee["performance"], 1),
        }
        for employee in data["employees"]
    ]

    total_bonus = 10000
    total_primitive_bonus = sum(employee["salary"] * employee["rate"] for employee in employees)
    scale_ratio = total_bonus / total_primitive_bonus
    print("scale ratio", scale_ratio)

    total_bonus_spent = 0
    return_distribution = []

    for employee in employees:
        final_bonus = int(employee["salary"] * employee["rate"] * scale_ratio)
        total_bonus_spent += final_bonus
        return_distribution.append({
            "name": employee['name'],
            "bonus": final_bonus,
            "rate": employee['rate']
        })
        print(f"{employee['name']}'s bonus: {final_bonus} (Rate: {employee['rate']})")

    print("Total Bonus Spent:", total_bonus_spent)

    return return_distribution, total_bonus_spent

return_distribution, total_bonus_spent = calculate_sum_of_bonus({
    "employees": [
        {
            "name": "John",
            "salary": "1000USD",
            "performance": "above average",
            "role": "Engineer"
        }, 
        {
            "name": "Bob",
            "salary": 60000,
            "performance": "average",
            "role": "CEO"
        }, 
        {
            "name": "Jenny",
            "salary": "50,000",
            "performance": "below average",
            "role": "Sales"
        }
    ]
})

print(return_distribution)
print(total_bonus_spent)

print("========= Task 3 =========")
# Task 3

# get
# setdefault

# def func(*data):
#     name_counts = {}
#     for name in data:
#         name_counts[name[1]] = name_counts.get(name[1], []) + [name]

#     print(name_counts)
    
#     unique_names = [names[0] for names in name_counts.values() if len(names) == 1]
#     print(", ".join(unique_names) if unique_names else "沒有")

# def func(*data):
#     name_counts = {}
#     for name in data:
#         # 使用 Python 的 setdefault 方法，這個方法會嘗試查找字典中特定的鍵。
#         # 如果該鍵不存在，它會創建一個新的鍵並將其值設為第二個參數（在此例中是一個空列表[]）
#         # 然後，無論該鍵是否已經存在，該方法都會返回該鍵相關聯的值（在此例中是列表）
#         name_counts.setdefault(name[1], []).append(name)
    
#     # print(name_counts)

#     unique_names = []

#     # 遍歷 name_counts 字典中的每個值（即每個名字列表）
#     for names in name_counts.values():
#         if len(names) == 1:
#             unique_names.append(names[0])

#     if unique_names:
#         # for name in unique_names:
#         #     print(name)
#          print(", ".join(unique_names))
#     else:
#         print("沒有")

# func("彭大牆", "王明雅", "吳明") # print 彭大牆
# func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花") # print 林花花
# func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有

print("========= Task 4 =========")
# Task 4 

# math.ceil
# -(-x // y)

def get_number(index):
    if index % 2 == 0: 
        print(index + index // 2)
        return index + index // 2
    else:
        print(index + index // 2 + 3)
        return index + index // 2 + 3

get_number(1) # print 4
get_number(5) # print 10 
get_number(10) # print 15

        # print(index + (-(-index // 2)) + 2)


def func(*data):

    name_times = {}

    for data_name in data:
        name = data_name.split()
        second_name = name[1]
        print(second_name)

        if second_name in name_times:
            name_times[second_name].append(name)
        else:
            name_times[second_name] = [name]

    print(name_times)

    lonely_name = []

    for names in name_times.values():
        if len(names) == 1:
            lonely_name.append(names[0])

    # 印出來
    if lonely_name:
        print(lonely_name)
    else:
        print("沒有")

func("彭大牆", "王明雅", "吳明")
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花")
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")

def get_number(index):
    if index % 2 == 0:
        result = index // 2 + index
    else:
        result = index // 2 + index + 3
    print(result)
    return result

get_number(1) # print 4
get_number(5) # print 10 
get_number(10) # print 15

