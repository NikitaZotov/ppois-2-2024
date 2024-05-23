function setBrightness(value) {
    fetch('/set_brightness', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ brightness: value })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Brightness set to " + value);
        } else {
            console.error("Error setting brightness");
        }
    })
    .catch(error => console.error('Error:', error));
}

function setVolume(value) {
    fetch('/set_volume', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ volume: value })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Volume set to " + value);
        } else {
            console.error("Error setting volume");
        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    var playButton = document.getElementById("playButton");
    var pauseButton = document.getElementById("pauseButton");
    var popUp = document.getElementById("popUp");
    var btn = document.getElementById("addToQueueBtn");
    var span = document.getElementsByClassName("close")[0];

    function set_play_pause_btn(){
        fetch('/is_open', { method: 'GET' })
        .then(response => response.json())
        .then(player => {
            if (!player.open) {
                playButton.style.display = "block";
                pauseButton.style.display = "none";
            } else {
                fetch('/is_playing', { method: 'GET' })
                .then(response => response.json())
                .then(video => {
                    if (video.playing) {
                        playButton.style.display = "none";
                        pauseButton.style.display = "block";
                    } else {
                        playButton.style.display = "block";
                        pauseButton.style.display = "none";
                    }
                });
            }
        });
    }

    function setBrightness(){
        fetch('/get_brightness', { method: 'GET' })
        .then(response => response.json())
        .then(screen => {
            if (screen.brightness) {
                console.log(screen.brightness);
                document.getElementById("brightness").value = screen.brightness;
            }
        });
    }


    function updateView(){
        setCurrentVideoFileName();
        set_play_pause_btn();
        setQueueFileNames();
    }

    btn.onclick = function() {
        popUp.style.display = "block";
    }

    span.onclick = function() {
        popUp.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == popUp) {
            popUp.style.display = "none";
        }
    }

    function add_to_queue() {
        popUp.style.display = "block";
        return new Promise((resolve, reject) => {
            document.getElementById("uploadForm").onsubmit = function(event) {
                event.preventDefault();
                var formData = new FormData(this);
                fetch('/add_to_queue', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    popUp.style.display = "none";
                    if (response.ok) {
                        resolve(true);
                    } else {
                        reject(false);
                    }
                })
                .catch(error => reject(false));
            }
        });
    }

    function setCurrentVideoFileName(){
        currentFile = document.getElementById("currentFile");
        fetch('/get_current_video_file_name', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(video => {
            if (video.name) {
                currentFile.textContent = video.name;
                console.log("current "+ video.name);
            }else{
                currentFile.textContent = "";
            }
        });
    }


    function setQueueFileNames() {
        // clearQueue();

        fetch('/get_queue', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            var queue = document.querySelector('.queue');
            while (queue.firstChild) {
                queue.removeChild(queue.firstChild);
            }
            if (data.queue && data.queue.length > 0) {
                console.log("Files in the queue:");
                data.queue.forEach(filename => {
                    console.log(filename);
                    var queueItem = document.createElement('div');
                    queueItem.classList.add('queueItem');
                    var h2 = document.createElement('h2');
                    h2.textContent = filename;
                    queueItem.appendChild(h2);
                    document.querySelector('.queue').appendChild(queueItem);
                });
                
            } else {
                var queueItem = document.createElement('div');
                queueItem.classList.add('queueItem');
                var h2 = document.createElement('h2');
                h2.textContent = "The queue is empty";
                queueItem.appendChild(h2);
                document.querySelector('.queue').appendChild(queueItem);
            }
        })
        .catch(error => console.error('Error:', error));
    }




    function play_queue() {
        fetch('/play', { method: 'POST' });
    }

    playButton.onclick = function() {
        fetch('/is_open', { method: 'GET' })
        .then(response => response.json())
        .then(player => {
            if (!player.open) {
                fetch('/is_queue_empty', { method: 'GET' })
                .then(response => response.json())
                .then(queue => {
                    if(queue.empty){
                        add_to_queue().then(() => {
                            play_queue();
                        });
                    } else {
                        play_queue();
                    }
                });
            } else {
                toggle_pause();
            }
        });
    }

    pauseButton.onclick = function() { toggle_pause(); }

    function toggle_pause() {
        fetch('/is_open', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.open) {
                fetch('/toggle_pause', { method: 'POST' }).then(isPlaying => {
                    if (isPlaying) {
                        console.log("Video paused...");
                        set_play_pause_btn();
                    } else {
                        console.log("Video unpaused...");
                        set_play_pause_btn();
                    }
                });
            }
        });
    }

    function clearQueue() {
        var queue = document.querySelector('.queue');
        while (queue.firstChild) {
            queue.removeChild(queue.firstChild);
        }
    }

    document.querySelector("form[action='/save_queue']").onsubmit = function(event) {
        event.preventDefault();
        fetch('/save_queue', { method: 'POST' })
    };

    document.querySelector("form[action='/load_queue']").onsubmit = function(event) {
        event.preventDefault();
        fetch('/load_queue', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateView();
                }
            });
    };

    setBrightness();
    updateView();
    setInterval(updateView, 3000);
});