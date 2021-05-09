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
            var modelObject = thisDb.createObjectStore("model",
                {keyPath:"model_file"}
            );

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