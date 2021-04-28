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
    document.getElementById("test-button").addEventListener("click", function() {
        console.log("here")
        let blob = new Blob(localStorage.getItem("model"))
        console.log("here")
        saveData(blob, 'model.txt')
    })
})
    