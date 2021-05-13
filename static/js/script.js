
const searchWraper = document.querySelector(".search-input");
const inputBox = searchWraper.querySelector('input');
const suggBox = searchWraper.querySelector('.autocom-box')

inputBox.onkeyup = (e)=>{
    let userData = e.target.value;
    let emptyArray = [];
    if (userData){
        emptyArray = suggestions.filter((data)=>{
            // filtering array value and user char to lowercase and return req only
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data)=>{
            return data = '<li>' + data + '</li>';
        });
        searchWraper.classList.add('active');    
        showsuggestions(emptyArray);
        let alllist = suggBox.querySelectorAll('li');
        for(let i = 0;i<alllist.length;i++){
            alllist[i].setAttribute('onclick', 'select(this)'); 
        } 
    }
    else{
        searchWraper.classList.remove('active');
    }
}


function select(element){
    let seldata = element.textContent;
    inputBox.value = seldata;
    searchWraper.classList.remove('active');
}

function showsuggestions(list){
    let listData;
    
    if(!list.length){
        uservalue = inputBox.value;
        listData ='<li>' +uservalue + '</li>'
    }
    else{
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}