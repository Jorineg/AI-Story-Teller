//const spinner = '<!--waiting--><style>body{background-color:black;display:flex;justify-content:center;align-items:center;height: 100vh;}</style><div class="d-flex justify-content-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';
//replace with spinner_white.gif as 128x128 image everything else is the same
const spinner = '<!--waiting--><style>body{background-color:black;display:flex;justify-content:center;align-items:center;height: 100vh;}</style><img src="/static/images/spinner_white.gif" alt="Loading..." style="width:128px;height:128px;">';
let buffer = spinner;

function onNewImageLoaded() {
    fetch_next_imagesound();

    const bgImage = document.getElementById('bg-image');
    bgImage.style.opacity = '0';
    setTimeout(function () {
        bgImage.style.transition = 'opacity 2s ease-in-out';
        bgImage.style.opacity = '1';
    }, 50);
    const audioElement = document.getElementById('narrator');
    if (!audioElement) {
        console.log("no audio element found. End of story.");
        return;
    }
    // set speed to 80% of normal
    // audioElement.playbackRate = .8;
    audioElement.addEventListener('ended', function () {
        console.log("audio ended");
        load_next_image(buffer);
        buffer = spinner;
    });
}


function load_next_image(data) {
    bgImage = document.getElementById('bg-image');
    function set_html() {
        if (data != document.body.innerHTML) {
            document.body.innerHTML = data;
        }
        if (!data.startsWith("<!--waiting-->")) {
            onNewImageLoaded();
        }
    }
    if (bgImage) {
        bgImage.style.opacity = '0';
        setTimeout(set_html, 2000);
    } else {
        set_html();
    }
}



function fetch_next_imagesound() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "false") {
                html = spinner;
                setTimeout(fetch_next_imagesound, 1000);
            } else {
                html = this.responseText;
            }

            // if html doesn't start with <!--waiting-->, <!-- imagesound -->, or <!-- endofstorytag -->,
            // then something went wrong and we want to redirect to /
            if (!html.startsWith("<!--waiting-->") && !html.startsWith("<!-- imagesound -->") && !html.startsWith("<!-- endofstorytag -->")) {
                console.log("redirecting to /");
                window.location.href = "/";
                return;
            }

            show_immediately = document.body.innerHTML.startsWith("<!--waiting-->");
            if (show_immediately) {
                load_next_image(html);
            } else {
                buffer = html;

                // Pre-download the image and mp3
                let parser = new DOMParser();
                let doc = parser.parseFromString(html, "text/html");
                let imageURL = doc.querySelector("#bg-image").style.backgroundImage.slice(5, -2);
                let mp3URL = doc.querySelector("#narrator source").src;
                let image = new Image();
                let audio = new Audio();
                image.src = imageURL;
                audio.src = mp3URL;
            }
        }
    };
    xhttp.open("GET", "/nextimagesound", true);
    xhttp.send();
    console.log("xhttp send for next imagesound");
}


var elem = document.documentElement;
function openFullscreen() {
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
}

function registerOnCloseFullscreen() {
    document.addEventListener("fullscreenchange", function () {
        if (!document.fullscreenElement) {
            console.log("Leaving fullscreen");
            location.reload();
        }
    });
}

function start() {
    openFullscreen();
    registerOnCloseFullscreen();
    document.body.innerHTML = spinner;
    //fetch_next_imagesound();

    // make request to /story/<id>/start and replace body with response
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            load_next_image(this.responseText);
        }
    };
    var story_id = window.location.pathname.split("story/")[1].split("/")[0];
    xhttp.open("GET", "/story/" + story_id + "/start", true);
    xhttp.send();

    // register keypress right arrow to go to next image
    document.addEventListener("keydown", function (event) {
        if (event.keyCode == 39) {
            load_next_image(buffer);
            buffer = spinner;
        }
    });
}


// // start instantaneously
// openFullscreen();
// registerOnCloseFullscreen();
// document.addEventListener("DOMContentLoaded", function () {
//     onNewImageLoaded();
// });
