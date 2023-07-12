print( "========= Task 1 =========")
# Task 1

def find_and_print(messages):
    # value 包含 >17 的數字、college 與 legal 與 vote 就印出相應的 key

    key_outcome = []

    for k, v in messages.items():
        if 'college' in v or 'legal' in v or 'vote' in v:
            print(k)
            key_outcome.append(k)
        for age in range(18, 200):
            if str(age) in v:
                print(k)
                key_outcome.append(k)
                break
    print(key_outcome)
    return key_outcome

find_and_print({
    "Bob": "My name is Bob. I'm 18 years old.",
    "Mary": "Hello, glad to meet you.",
    "Copper": "I'm a college student. Nice to meet you.",
    "Leslie": "I am of legal age in Taiwan.",
    "Vivian": "I will vote for Donald Trump next week",
    "Jenny": "Good morning."
})

print( "========= Task 2 =========")
# Task 2

def calculate_sum_of_bonus(data):
    # 以另外函數處理 salary 非數字資料，有 USD *30，有逗號則直接去掉
    # 以另外函數設定表現 performance 影響獎金倍數，above 為兩倍，below 為 1/2，average 則為 1
    # 設定總獎金不得超過10000，即 totalBonus。分配獎金總額可以略小於 10000
    # 以本薪乘以獎金倍數，但總額不得超過 10000，因此除以 scaleRatio 等比減少以分配總獎金
    def convert_salary(salary):
        if isinstance(salary, str):
            if 'USD' in salary:
                salary = int(salary.replace('USD', '').replace(',', '')) * 30
            else:
                salary = int(salary.replace(',', ''))
        return salary

    def bonus_rate(performance):
        if 'above' in performance:
            return 2
        elif 'below' in performance:
            return 0.5
        else:
            return 1

    employees = []
    for employee in data['employees']:
        employees.append(employee.copy())

    total_bonus = 10000
    total_bonus_primitive = 0

    for employee in employees:
        employee['salary'] = convert_salary(employee['salary'])
        employee['rate'] = bonus_rate(employee['performance'])
        total_bonus_primitive += employee['salary'] * employee['rate']

    scale_ratio = total_bonus / total_bonus_primitive
    total_bonus_spent = 0

    for employee in employees:
        final_bonus = int(employee['salary'] * employee['rate'] * scale_ratio)
        total_bonus_spent += final_bonus

        print(f"{employee['name']}'s bonus: {final_bonus} (Rate: {employee['rate']})")

    print("Total Bonus Spent:", total_bonus_spent)

calculate_sum_of_bonus ({
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

print( "========= Task 3 =========")
# Task 3

def func(*data):
    # 抓出第二個字即可
    # 以物件 key: value 紀錄每個字出現時的完整名字資料集供印出
    # 如果只有出現一次，就把名字印出來
    # 如果沒有出現，狀態機為否，則印出 "沒有"
    name_counts = {}

    for i in range(len(data)):
        middle_name = data[i][1]

        if middle_name in name_counts:
            name_counts[middle_name].append(data[i])
        else:
            name_counts[middle_name] = [data[i]]

    unique_names = []

    for name in name_counts.values():
        if len(name) == 1:
            unique_names.append(name[0])

    if unique_names:
        print(",".join(unique_names))
    else:
        print("沒有")

func("彭大牆", "王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有

print( "========= Task 4 =========")
# Task 4

def get_number(index):
    # index[0] = 0 + 0, index[1] = 1 + 3
    # index[2] = 2 + 1, index[3] = 3 + 4
    # index[4] = 4 + 2, index[5] = 5 + 5 
    # index[6] = 6 + 3, index[7] = 7 + 6
    # index[8] = 8 + 4, index[9] = 9 + 7
    # index[10] = 10 + 5 
    # 由此可知奇數項目為初始值 index + 3，每增加一奇數增 1
    # 偶數項目(含0) 為 index + 0，每增加一奇數增 1
    array = []
    even_count = 0
    odd_count = 3
    arrayLimit = 12

    for i in range(arrayLimit):
        if i % 2 == 0:
            array.append(i + even_count)
            even_count += 1
        else:
            array.append(i + odd_count)
            odd_count += 1

    print(array)
    print(array[index])
    return array[index]
get_number(1) # print 4
get_number(5) # print 10 
get_number(10) # print 15