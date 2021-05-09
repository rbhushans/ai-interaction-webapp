const getModelBtn = document.getElementById("get-model-btn");
const sendModelBtn = document.getElementById("send-model-btn");

const dbName = "model_storage";
var db;

document.onreadystatechange = () => {

    // First check if indexedDB is supported by the user browser
    if (!("indexedDB" in window)) {
        console.log("IndexedDB not supported. Try another browser");
        return;
    } 

    //Request the DB from the user's browser
    var openRequest = indexedDB.open(dbName, 1);

    // Function onupgradeneeded called when the db doesn't exist in the user's browser or
    // a new data type (table) has been created in the db and it needs to update. 
    openRequest.onupgradeneeded = (e) => {
        var thisDb = e.target.result;
        console.log("Running onupgradeneeded");
        
        // Check for each table/data type entry and add if missing
        if (!thisDb.objectStoreNames.contains("model")) {
            /*
            var modelObject = thisDb.createObjectStore("model",
                {keyPath:"model_file"}
            );
            */
            var modelObject = thisDb.createObjectStore("model");

        }
    }

    // Function onsuccess is called when a database open() request is successfully completed
    // and returns the database object (skips over onupgradeneeded).
    openRequest.onsuccess = function(e) {
        console.log("running onsuccess");
        db = e.target.result;
        console.dir(db.objectStoreNames);

        // Start listening for button clicks to add a person


    }

    // Function onerror is called when a database open() request is unsuccessfully completed
    // and doesn't need to call onupgradeneeded.
    openRequest.onerror = function(e) {
        console.log("onerror!");
        console.dir(e);
    }

}

// ! Get a model from the database
getModelBtn.addEventListener("click", (evt) => {
    var xhr = new XMLHttpRequest(), blob;

    xhr.open("GET", "/database/model");
    xhr.responseType = "blob";

    xhr.addEventListener("load", () => {
        if (xhr.status == 200) {
            console.log("Model Retrieved");

            blob = xhr.response; // Load in response

            putModelInDb(blob);
        }

    }, false);

    // Send XHR
    xhr.send();

});

function putModelInDb(blob) {
    console.log("Put Model In DB");

    // Open database transaction
    var transaction = db.transaction("model", "readwrite");

    console.log(transaction);

    // Put blob in database
    var put = transaction.objectStore("model").add(blob, "model_file");

    transaction.objectStore("model").get("model_file").onsuccess = (event) => {
        // Test retrieving model from local IndexDB
        console.log("Model File: " + event.target.result);

    };

} 


// ! Send a model from the database
sendModelBtn.addEventListener("click", (evt) => {
    // Open database transaction
    var modelBlob;
    var transaction = db.transaction("model", "readonly");

    transaction.objectStore("model").get("model_file").onsuccess = (event) => {
        // Test retrieving model from local IndexDB
        modelBlob = event.target.result;

        var data = new FormData();
        data.append('file', modelBlob, "blob");

        console.log("Model Blob Retrieved from browser database: " + data);
        fetch("/database/model", {method: "POST", body: data});


    };

});

async function getModelInDb() {
    // Open database transaction
    var transaction = db.transaction("model", "readonly");

    transaction.objectStore("model").get("model_file").onsuccess = (event) => {
        // Test retrieving model from local IndexDB
        return event.target.result;

    };

}