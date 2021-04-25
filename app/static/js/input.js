console.log("Hello from app.js!");
// const addToList = (val)=>  {
//     console.log(val)
//     let fList = document.getElementById("selected-features-list")

//     let item = document.createElement("li");
//     item.appendChild(document.createTextNode(val))
//     fList.appendChild(item)
// }

document.addEventListener("DOMContentLoaded", function(){
    let buttons = document.getElementsByClassName("feature-option")
    Array.prototype.forEach.call(buttons, function(item) {
        item.addEventListener('click', function(){
            let val = this.innerText
            let fList = document.getElementById("selected-features-list")
            var items = fList.getElementsByTagName("li");
            let inList = -1
            for (var i = 0; i < items.length; ++i) {
                if(val == items[i].innerText){
                    inList = i
                    break
                }
            }
            if(inList != -1){
                fList.removeChild(fList.childNodes[inList])
            }else{
                let item = document.createElement("li");
                item.appendChild(document.createTextNode(val))
                item.setAttribute("class", "selected-features-item")
                fList.appendChild(item)
            }
        })
    });
})