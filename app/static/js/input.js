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
                let input = document.createElement("input");
                input.setAttribute("type", "hidden")
                input.setAttribute("name", "params");
                input.setAttribute("value", val)
                item.appendChild(input)
                item.setAttribute("class", "selected-features-item")
                fList.appendChild(item)
            }
        })
    });

    document.getElementById("start-train-btn").addEventListener('click', function() {
        let items = document.getElementById("selected-features-list").getElementsByTagName("li");
        let data = []
        for(var i = 0; i < items.length; i++){
            if(items[i].innerText != "") data.push(items[i].innerText)
        }
        let xhr = new XMLHttpRequest(),
            blob,
            fileReader = new FileReader();
        xhr.open('POST', '/train_model');
        xhr.responseType = "arraybuffer"
        xhr.onreadystatechange = function() { // Call a function when the state changes.
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                blob = new Blob([this.response])
                fileReader.onload = function(evt) {
                    let result = evt.target.result;
                    localStorage.setItem("model", result)
                    console.log("stored in local storage")
                    window.location = "results"
                }
                fileReader.readAsDataURL(blob)
            }
        }
        xhr.send(data);
    })
})
