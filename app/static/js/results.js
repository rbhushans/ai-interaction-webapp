function saveData(blob, fileName) // does the same as FileSaver.js
{
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";

    var url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(url);
}

document.addEventListener("DOMContentLoaded", function(){
    store = window.localStorage
    document.getElementById("results-precision").innerText = "Your model's precision is " + store.getItem("precision")
    document.getElementById("results-recall").innerText = "Your model's recall is " + store.getItem("recall")

    document.getElementById("test-persona").addEventListener("click", function() {
        let input_items = document.getElementById("results-features").getElementsByTagName("input");
        let select_items = document.getElementById("results-features").getElementsByTagName("select");

        let data = []
        for(var i = 0; i < input_items.length; i++){
            data.push(input_items[i].value)
        }
        for(var i = 0; i < select_items.length; i++){
            data.push(select_items[i].value)
        }

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/test_model');
        xhr.onreadystatechange = function() { // Call a function when the state changes.
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                console.log("Received prediction: " + this.responseText)
                var data = this.responseText.split("|")
                console.log(data)
                //show dialog 
            }
        }
        xhr.send(data);
    })
})
    