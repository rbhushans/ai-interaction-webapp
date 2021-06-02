const num_train = parseInt(window.localStorage.getItem("numTrainTimes")); // Number of times user has trained a model

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

document.addEventListener("DOMContentLoaded", function() {
    let dialog = document.getElementById("results-dialog");
    dialog.close()
    store = window.localStorage
    prec = Number(store.getItem("precision"))
    rec = Number(store.getItem("recall"))
    prec = prec.toFixed(3)
    rec = rec.toFixed(3)
    // document.getElementById("results-precision").innerText = "Your model's precision is " + prec
    // document.getElementById("results-recall").innerText = "Your model's recall is " + rec

    // Write out the user model's selected features
    writeFeaturesToList(document.getElementById('feature-list-last'));

    // Check if the user has at least trained once before showing the 'end-experience' button
    if (parseInt(window.localStorage.getItem("numTrainTimes")) > 1) {
        document.getElementById("end-div").style.visibility = "visible";
    } else {
        document.getElementById("end-div").style.visibility = "hidden";
    }

    document.getElementById("results-close").addEventListener('click', function() {
        dialog.close()
    })

    document.getElementById("test-persona").addEventListener("click", function() {
        let input_items = document.getElementById("results-features").getElementsByTagName("input");
        let select_items = document.getElementById("results-features").getElementsByTagName("select");

        let data = []
        for(var i = 0; i < input_items.length; i++){
            if(input_items[i].value == ''){
                data.push(0)
            }else{
                data.push(input_items[i].value)
            }
            
        }
        for(var i = 0; i < select_items.length; i++){
            if(select_items[i].value == ''){
                data.push('Not Specified')
            }else{
                data.push(select_items[i].value)
            }
        }

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/test_model');
        xhr.onreadystatechange = function() { // Call a function when the state changes.
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                console.log("Received prediction: " + this.responseText)
                var data = this.responseText.split("|")
                console.log(data)
                let pred = data[0][2]
                let conf = data[1]
                conf = conf.split(" ")[pred]
                if(pred == 1){
                    conf = conf.substring(0, conf.length-1)
                }else{
                    conf = conf.substring(1, conf.length)
                }
                
                conf = conf * 100
                conf = conf.toFixed(3)

                console.log(pred)
                console.log(conf)
                
                if(pred == 0){
                    document.getElementById("results-pred").innerText = "not recidivate"
                    document.getElementById("results-pred").setAttribute("class", "not-recid-pred")
                    document.getElementById("results-conf").setAttribute("class", "not-recid-pred")
                    document.getElementById("results-dialog-img").setAttribute("src", "../static/img/logo_not_recid.png")
                }else{
                    document.getElementById("results-pred").innerText = "recidivate"
                    document.getElementById("results-pred").setAttribute("class", "recid-pred")
                    document.getElementById("results-conf").setAttribute("class", "recid-pred")
                    document.getElementById("results-dialog-img").setAttribute("src", "../static/img/logo_recid.png")
                }
                

                document.getElementById("results-conf").innerText = conf + "%"
                dialog.showModal()
            }
        }
        xhr.send(data);
    });

    // Set the transition to the end screen
    document.getElementById("end-button").addEventListener("click", () => {
        uiEndTransition();

    });
})
    
/**
 * Write out the trained model's features to an HTML unordered list.
 * 
 * @param {<ul>} HTMLList
 */
function writeFeaturesToList(HTMLList) {
    var featureArray = getModelFeatures();

    for (var index in featureArray) {
        var newItem = document.createElement("li");
        newItem.innerText = featureArray[index];
        HTMLList.appendChild(newItem);
    }    

}

/**
 * Retrieves the trained models feature names that are stored in the client browser 
 * storage.
 * 
 * @returns {String Array}
 */
function getModelFeatures() {
    var featureArray = JSON.parse(window.localStorage.getItem("features"));
    return featureArray;

}

/**
 * Move the normal results page to the left (off screen) and
 * pull in end page to finish session. 
 * 
 */
function uiEndTransition() {
    var normalResultsPage = document.getElementById("results-main");
    normalResultsPage.style.transform = "translate(-100%)"

    var endResultsPage = document.getElementById("results-end");
    endResultsPage.style.transform = "translate(-100%)"

}