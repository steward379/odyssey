//Task 1-revise

//forEach
//match
//regularExpression
//-  \b 單詞邊界的特殊字符
//-  \d 對應數字字符
//-  /g 是全局修飾符，表示在整個字符串中全局地匹配。
//- (\d+) 是一個捕獲組，對應一個/多個連續的數字字符
// [1] 代表第一個捕獲組

function findAndPrint(messages) {
    let keyOutcome = [];

    for (let key in messages) {
        let value = messages[key];
        if (value.includes("college") || value.includes("legal") || value.includes("vote")) {
            console.log(key);
            keyOutcome.push(key);
        }
        for (let age = 18; age < 200; age++) {
            if (value.includes(age.toString())) {
                console.log(key);
                keyOutcome.push(key);
                break;
            }
        }
    }
    console.log(keyOutcome);
    return keyOutcome;
}
    
// function findAndPrint(messages) {
//     let keyOutcome = [];
  
//     Object.keys(messages).forEach((key) => {
//       const eachValue = messages[key];
//       const ageMatch = eachValue.match(/\b(\d+)\b/);

//       if (eachValue.includes('college') || eachValue.includes('legal') || 
//             (ageMatch && ageMatch[1]) > 17
//          ) {
//             console.log(key);
//             keyOutcome.push(key);
//       }
//     });
  
//     console.log(keyOutcome);
//     return keyOutcome;
//   }
  
  findAndPrint({
    "Bob": "My name is Bob. I'm 18 years old.",
    "Mary": "Hello, glad to meet you.",
    "Copper": "I'm a college student. Nice to meet you.",
    "Leslie": "I am of legal age in Taiwan.",
    "Vivian": "I will vote for Donald Trump next week",
    "Jenny": "Good morning."
  });

//Task 2-revise

//map
//三元運算子(Ternary Operator）

function calculateSumOfBonus(data) {
    const totalBonus = 10000;
    let totalBonusPrimitive = 0;

    const employeeBonuses = data.employees.map(
      ({name, salary, performance}) => {
        salary = typeof salary === "string" ? 
            parseInt(salary.replace("USD", "").replace(",", "")) * (salary.includes("USD") ? 30 : 1) :
            salary;
        
        const rate = performance.includes("above") ? 2 :
            performance.includes("below") ? 0.5 :
            1;

        const bonusPrimitive = salary * rate;
        totalBonusPrimitive += bonusPrimitive;

        return { name, rate, bonusPrimitive };
    });

    const scaleRatio = totalBonus / totalBonusPrimitive;
    console.log(`👉 scaleRatio: ${scaleRatio}`);

    const totalBonusSpent = employeeBonuses.reduce((acc, {name, rate, bonusPrimitive}) => {
        const finalBonus = Math.floor(bonusPrimitive * scaleRatio);
        console.log(`${name}'s bonus 🎉 ${finalBonus} 🎉 (rate: ${rate})`);
        return acc + finalBonus;
    }, 0);

    console.log("🎉 Total Bonuses 🎉 : ", totalBonusSpent);
}

calculateSumOfBonus({
    "employees": [{
        "name": "John",
        "salary": "1000USD",
        "performance": "above average",
        "role": "Engineer"
    }, {
        "name": "Bob",
        "salary": 60000,
        "performance": "average",
        "role": "CEO"
    }, {
        "name": "Jenny",
        "salary": "50,000",
        "performance": "below average",
        "role": "Sales"
    }]
});


//Task 3-revise

//map
//filter
//lastindexof
//find


// function func(...data){
//     let middleNameData = data.map(name => name.substring(1,2));
//     let uniqueMiddleNameData = middleNameData.filter((item, index) => middleNameData.indexOf(item) === middleNameData.lastIndexOf(item));
//     let uniqueName = data.find(name => uniqueMiddleNameData.includes(name.substring(1,2)));

//     if (uniqueName) {
//         console.log(uniqueName);
//     } else {
//         console.log("沒有");
//     }
// }

//   func("彭大牆", "王明雅", "吳明"); // prints 彭大牆
//   func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花"); // prints 林花花
//   func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // prints 沒有

//Task 4-revise

// Array.from
// _ 代表不需要使用的參數

function getNumberArray(index){
    const array = Array.from({length: 20}).map((_, i) => {
        return i % 2 === 0 ? i + Math.floor(i / 2) : i + Math.floor(i / 2) + 3;
    });

    console.log(array[index]);
    return array[index];
}

function getNumber(index){
    let result = index % 2 === 0 ? 
                 index + Math.floor(index / 2) : 
                 index + Math.floor(index / 2) + 3;
    console.log(result);
    return result;
}

getNumber(1); // print 4 
getNumber(5); // print 10 
getNumber(10); // print 15

function findIndexOfCar(seats, status, number){
    // 如果該陣列索引值的值大於等於 number，且 status 為 1，則印出該索引值
    const avaiSeats = seats.map((item, index) => item*status[index]);

    console.log("new",avaiSeats);

    avaiSeats.sort(function(a, b) {
        return a - b;
    });

    let result = avaiSeats.find( value => value >= number);

    console.log(seats.indexOf(result));
    return avaiSeats.indexOf(result);
}
findIndexOfCar([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2); // print 4 
findIndexOfCar([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); //print -1 
findIndexOfCar([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
findIndexOfCar([3, 10, 3, 1], [1, 1, 0, 1], 2); // print 0


function findIndexOfCarTry(seats, status, number){
    let min_val = Infinity;
    let min_index = -1;

    for(let i = 0; i < seats.length; i++){
        if(seats[i] >= number && status[i] && seats[i] < min_val){
            min_val = seats[i];
            min_index = i;
        }
    }

    console.log(min_index);
    return min_index;
}

findIndexOfCar([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2); // print 4 
findIndexOfCar([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); //print -1 
findIndexOfCar([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2





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
