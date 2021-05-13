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
        //show dialog and make request to test model
    })
})
    