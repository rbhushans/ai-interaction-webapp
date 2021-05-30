function getElementY(query) {
    return window.pageYOffset + document.querySelector(query).getBoundingClientRect().top
}
  
function doScrolling(element, duration) {
    var startingY = window.pageYOffset
    var elementY = getElementY(element)
    var targetY = document.body.scrollHeight - elementY < window.innerHeight ? document.body.scrollHeight - window.innerHeight : elementY
    var diff = targetY - startingY
    
    var easing = function (t) { return t<.5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1 }
    var start
  
    if (!diff) return
        window.requestAnimationFrame(function step(timestamp) {
            if (!start) start = timestamp
            var time = timestamp - start
            var percent = Math.min(time / duration, 1)
            percent = easing(percent)
            window.scrollTo(0, startingY + diff * percent)
        if (time < duration) {
            window.requestAnimationFrame(step)
        }
    })
}
  

document.addEventListener("DOMContentLoaded", function(){
    let dialog = document.getElementById("home-dialog");
    dialog.close()
    document.getElementById("down-arrow-1").addEventListener("click", doScrolling.bind(null, "#home-section-2", 1000))

    document.getElementById("down-arrow-2").addEventListener("click", doScrolling.bind(null, "#home-section-3", 1000))

    document.getElementById("home-close").addEventListener('click', function() {
        dialog.close()
    })

    document.getElementById("home-ai").addEventListener("click", function(){
        document.getElementById("home-dialog-header").innerText = "What is AI?"
        document.getElementById("home-dialog-body").innerText = "AI stands for Artificial Intelligence, ..."
        document.getElementById("home-dialog-img").setAttribute("src", "../static/img/TEA Logo.png") 
        dialog.showModal();
    })

    //Connect start button to the correct page
    document.getElementById('start-btn').addEventListener("click", () => {
        document.location.href = "/train";
    })

})