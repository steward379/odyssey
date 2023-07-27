console.log("========= Task 1 =========");
// Task 1

function findAndPrint(messages){
    //value 包含 >17 的數字、college 與 legal 與 vote 就印出相應的 key

    let keyOutcome = [];
    
    for(i=0; i< Object.keys(messages).length; i++){
      
        function ageMature(messages){
            for (age=18; age < 200; age++){
                if(Object.values(messages)[i].includes(age)){
                    return true;
                }
            }
        }
        
        if(Object.values(messages)[i].includes("college") ||
           Object.values(messages)[i].includes("legal") || 
           Object.values(messages)[i].includes("vote") ||
           ageMature(messages)){
                console.log(Object.keys(messages)[i]);
                keyOutcome.push(Object.keys(messages)[i]);
        }
    }
    console.log(keyOutcome);    
    return keyOutcome.join(", ");
} 
findAndPrint(
    {
        "Bob":"My name is Bob. I'm 18 years old.", 
        "Mary":"Hello, glad to meet you.",
        "Copper":"I'm a college student. Nice to meet you.", 
        "Leslie":"I am of legal age in Taiwan.",
        "Vivian":"I will vote for Donald Trump next week",
        "Jenny":"Good morning." 
    }
);

console.log("========= Task 2 =========");
// Task 2

function calculateSumOfBonus(data) {
    //以另外函數處理 salary 非數字資料，有 USD *30，有逗號則直接去掉
    //以另外函數設定表現 performance 影響獎金倍數，above 為兩倍，below 為 1/2，average 則為 1
    //設定總獎金不得超過10000，即 totalBonus。分配獎金總額可以略小於 10000
    //以本薪乘以獎金倍數，但總額不得超過 10000，因此除以 scaleRatio 等比減少以分配總獎金

    //切記不更動到原始資料
    const employees = data.employees;
    let totalEmployeesCount = employees.length;
    const totalBonus = 10000;
    let totalBonusPrimitive = 0;
    let totalBonusSpent = 0;
    let returnData = [];

    //另外設定一陣列儲存獎金
    let employeeBonuses = [];
  
    for (let i = 0; i < totalEmployeesCount; i++) {
        let employee = employees[i];
            
        let { salary } = employee;
        salary = convertSalary(salary);
        
        const { performance, name } = employee;  // 解構賦值ㄥ
        const rate = bonusRate(performance);
    
        const bonusPrimitive = salary * rate;
        totalBonusPrimitive += bonusPrimitive;
    
        employeeBonuses.push({
            name: name,
            rate: rate,
            bonusPrimitive: bonusPrimitive
        });
    }

    const scaleRatio = totalBonus / totalBonusPrimitive;
    console.log(`👉 scaleRatio: ${scaleRatio}`);
    returnData.push(`👉 scaleRatio: ${scaleRatio}`);

    for (let i = 0; i < totalEmployeesCount; i++) {
        const { name, rate, bonusPrimitive } = employeeBonuses[i]; // 解構賦值
        
        const finalBonus = Math.floor(bonusPrimitive * scaleRatio);
        totalBonusSpent += finalBonus;
    
        console.log(`${name}'s bonus 🎉 ${finalBonus} 🎉 (rate: ${rate})`);
        returnData.push(`${name}'s bonus 🎉 ${finalBonus} 🎉 (rate: ${rate})`);
    }
    console.log("🎉 Total Bonuses 🎉 : ", totalBonusSpent);
    returnData.push("🎉 Total Bonuses 🎉 : "+ totalBonusSpent);

    let returnDataString = returnData.toString().replaceAll(",","\n");
    console.log(returnDataString);
    return returnDataString;

    //functional Programming
    function convertSalary(salary) {
        if (typeof salary === "string") {
            const isUSD = salary.includes("USD");
            salary = parseInt(salary.replace("USD", "").replace(",", ""));
            return isUSD ? salary * 30 : salary;
        }
        return salary;
    }

    //functional Programming
    function bonusRate(performance) {
        if (performance.includes("above")) {
            return 2;
        } else if (performance.includes("below")) {
            return 0.5;
        }
            return 1;
    }
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

console.log("========= Task 3 =========");
// Task 3

function func(...data){
    //抓出第二個字即可
    //以物件 key: value 紀錄每個字出現時的完整名字資料集供印出
    //如果只有出現一次，就把名字印出來
    //如果沒有出現，狀態機為否，則印出 "沒有"

    let nameCounts = {};
    let isUnique = false;
    
    for (let i = 0; i < data.length; i++){
        let middleName = data[i].substring(1, 2);
        if(nameCounts[middleName]) {
            nameCounts[middleName].push(data[i]);
        } else {
            nameCounts[middleName] = [data[i]];
        }
    }
    console.log(nameCounts);
    
    for(let name in nameCounts){
        if(nameCounts[name].length === 1){
            console.log( nameCounts[name][0]);
            isUnique = true;
            return nameCounts[name][0];
        }
    }
  
    if(!isUnique){
      console.log("沒有");
      return "沒有";
    }
}



func("彭大牆", "王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花"); // print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有j

console.log("========= Task 4 =========");
// Task 4

// function getNumber(index){
//     // index[0] = 0 + 0, index[1] = 1 + 3
//     // index[2] = 2 + 1, index[3] = 3 + 4
//     // index[4] = 4 + 2, index[5] = 5 + 5 
//     // index[6] = 6 + 3, index[7] = 7 + 6
//     // index[8] = 8 + 4, index[9] = 9 + 7
//     // index[10] = 10 + 5 
//     // 由此可知奇數項目為初始值 index + 3，每增加一奇數增 1
//     // 偶數項目(含0) 為 index + 0，每增加一奇數增 1

//     let array =[];
//     let evenCount = 0;
//     let oddCount = 3;
//     let arrayLimit = 20;

//     for (i=0; i < arrayLimit; i++){
//         if(i%2 === 0 ){
//             array.push(i + evenCount);
//             evenCount ++;
//         }else{
//             array.push(i + oddCount);
//             oddCount ++;
//         }
        
//     }
//     // console.log(array);
//     console.log(array[index]);
//     return array[index];
// }

// O(1)
function getNumber(index){
    let result;
    if(index % 2 === 0 ){
        result = index + Math.floor(index / 2);
    }else{
        result = index + Math.floor(index / 2) + 3;
    }
    console.log(result);
    return result;
}

getNumber(1); // print 4 
getNumber(5); // print 10 
getNumber(10); // print 15

console.log("========= Task 5 =========");
//Task 5

function findIndexOfCar(seats, status, number){
    // 如果該陣列索引值的值大於等於 number，且 status 為 1，則印出該索引值
    let numberArray = [];

    for(i =0; i < seats.length; i++){
        if(seats[i] >= number && status[i]){
            numberArray.push(seats[i]);
        }else{
            numberArray.push(0);
        }
    }
    numberArray.sort(function(a, b) {
        return a - b;
    });

    let result = numberArray.find( value => value);

    seats.indexOf(result);

    console.log(seats.indexOf(result));
    return seats.indexOf(result);
}
findIndexOfCar([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2); // print 4 
findIndexOfCar([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); //print -1 
findIndexOfCar([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2