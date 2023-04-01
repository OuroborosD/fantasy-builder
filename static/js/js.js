

function sumAtributes(){
    // console.log('carregou a função')
    // let num1 = document.getElementsByClassName('num1')[0].innerHTML
    // let num2 = document.getElementsByClassName('num1')[0].innerHTML
    // let sum = parseInt(num1) + parseInt(num2)
    // document.getElementsByClassName('sum')[0].innerHTML = sum
    let num1 = [];
    let num2 = [];
    let teste = document.querySelectorAll('.num1')
    let teste2 = document.querySelectorAll('.num2')

    teste.forEach((value) =>{
        num1.push(parseInt(value.innerHTML))
    })
    teste2.forEach((value) =>{
        num2.push(parseInt(value.innerHTML))
    })


    for(let i= 0; i < num1.length ; i++){
        let sum = num1[i]+ num2[i]
        document.getElementsByClassName('sum')[i].innerHTML = sum
    }

}

function selectonchace(){
    
}