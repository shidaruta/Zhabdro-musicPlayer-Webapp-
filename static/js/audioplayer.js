
// drop down
document.getElementById('dropdownToggle').addEventListener('click', function () {
    var dropdownContent = document.getElementById('dropdownContent');
    dropdownContent.classList.toggle('active');
});

window.onclick = function (event) {
    if (!event.target.matches('#dropdownToggle') && !event.target.closest('.dropdown')) {
        var dropdownContent = document.getElementById('dropdownContent');
        if (dropdownContent.classList.contains('active')) {
            dropdownContent.classList.remove('active');
        }
    }
}

// Clear the search input fields after the page loads
document.addEventListener('DOMContentLoaded', function () {
    var topSearchInput = document.querySelector('.top-search-container .search-input');
    var dropdownSearchInput = document.querySelector('.dropdown-search-input');
    if (topSearchInput) {
        topSearchInput.value = '';
    }
    if (dropdownSearchInput) {
        dropdownSearchInput.value = '';
    }
});
// Function to show the custom warning dialog
function showLogoutWarning() {
    document.getElementById('custom-warning-dialog').style.display = 'block';
}

// Function to hide the custom warning dialog
function hideLogoutWarning() {
    document.getElementById('custom-warning-dialog').style.display = 'none';
}

// Event listener for logout link
document.getElementById('logout-link').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default action (navigation)
    showLogoutWarning();
});

// Event listener for logout link in dropdown
document.getElementById('dropdown-logout').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default action (navigation)
    showLogoutWarning();
});

// Event listener for confirm logout button
document.getElementById('confirm-logout').addEventListener('click', function () {
    // Hide the dialog when the user confirms logout
    hideLogoutWarning();
    // Redirect to the logout URL
    window.location.href = "/logout/";
});

// Event listener for cancel logout button
document.getElementById('cancel-logout').addEventListener('click', function () {
    // Hide the dialog when the user cancels logout
    hideLogoutWarning();
});



// for audio player
document.addEventListener('DOMContentLoaded', function () {
    var audioElement = document.getElementById('audio');
    var seekBar = document.getElementById('seek-bar');
    var currentTime = document.querySelector('.current-time');
    var songDuration = document.querySelector('.song-duration');
    var volumeBar = document.getElementById('volume-bar');
    var muteButton = document.getElementById('mute');

    // Update the song duration once metadata has loaded
    audioElement.addEventListener('loadedmetadata', function () {
        var durationMinutes = Math.floor(audioElement.duration / 60);
        var durationSeconds = Math.floor(audioElement.duration % 60);
        songDuration.textContent = durationMinutes + ':' + (durationSeconds < 10 ? '0' : '') + durationSeconds;
    });

    // Update the seek bar and current time as the song plays
    audioElement.addEventListener('timeupdate', function () {
        var currentTimeMinutes = Math.floor(audioElement.currentTime / 60);
        var currentTimeSeconds = Math.floor(audioElement.currentTime % 60);
        currentTime.textContent = currentTimeMinutes + ':' + (currentTimeSeconds < 10 ? '0' : '') + currentTimeSeconds;

        // Calculate the progress of the song and update the seek bar
        var progress = (audioElement.currentTime / audioElement.duration) * 100;
        seekBar.value = progress;
    });

    // When the user changes the seek bar position, seek the song to the corresponding time
    seekBar.addEventListener('input', function () {
        var seekTo = (audioElement.duration * (seekBar.value / 100));
        audioElement.currentTime = seekTo;
    });

    document.querySelectorAll('.play-btn').forEach(button => {
        button.addEventListener('click', function () {
            var audioUrl = this.getAttribute('data-audio-url');
            var albumImage = this.closest('tr').querySelector('.album-logo-img').src;
            var songTitle = this.closest('tr').querySelector('td:nth-child(2)').textContent;
            var artist = this.closest('tr').querySelector('td:nth-child(3)').textContent;

            // Update audio player with song information
            var audioPlayer = document.querySelector('.audio-player');
            audioPlayer.style.display = 'flex';
            audioPlayer.querySelector('.audio-player-left img').src = albumImage;
            audioPlayer.querySelector('.song-details .song-title').textContent = songTitle;
            audioPlayer.querySelector('.song-details .artist').textContent = artist;

            // Update audio source
            var audioElement = document.getElementById('audio');
            audioElement.src = audioUrl;

            // Play the audio
            audioElement.play();
            // Change the play button icon
            var playPauseButton = document.getElementById('play-pause');
            playPauseButton.innerHTML = '<i class="fa-solid fa-pause"></i>';
        });
    });


    // Function to toggle play/pause icon and audio playback
    document.getElementById('play-pause').addEventListener('click', function () {
        if (audioElement.paused) {
            audioElement.play();
            this.innerHTML = '<i class="fa-solid fa-pause"></i>';
        } else {
            audioElement.pause();
            this.innerHTML = '<i class="fa-solid fa-play"></i>';
        }
    });
    volumeBar.addEventListener('input', function () {
        audioElement.volume = this.value / 100;
    });

    // Mute/unmute functionality
    muteButton.addEventListener('click', function () {
        if (audioElement.muted) {
            audioElement.muted = false;
            this.innerHTML = '<i class="fa-solid fa-volume-up"></i>';
            volumeBar.value = audioElement.volume * 100;
        } else {
            audioElement.muted = true;
            this.innerHTML = '<i class="fa-solid fa-volume-mute"></i>';
            volumeBar.value = 0;
        }
    });

});
// for ajax request cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleFavorite(button, songId) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/toggle_favorite/${songId}/`);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                if (response.success) {
                    let starIcon = button.querySelector('i');
                    if (response.is_favorite) {
                        starIcon.classList.remove('unchecked');
                        starIcon.classList.add('checked');
                    } else {
                        starIcon.classList.remove('checked');
                        starIcon.classList.add('unchecked');
                    }
                } else {
                    alert('Failed to toggle favorite.');
                }
            } else {
                alert('Failed to toggle favorite.');
            }
        }
    };

    xhr.onerror = function() {
        alert('Failed to toggle favorite. Network error.');
    };

    xhr.send();
}


function deleteSong(songId) {
    // Show the delete song dialog box
    document.getElementById('delete-song-dialog').style.display = 'block';

    // Event listener for cancel delete button
    document.getElementById('cancel-delete').addEventListener('click', function () {
        // Hide the dialog box when cancel is clicked
        document.getElementById('delete-song-dialog').style.display = 'none';
    });

    // Event listener for confirm delete button
    document.getElementById('confirm-delete').addEventListener('click', function () {
        // Make AJAX request to delete the song
        let xhr = new XMLHttpRequest();
        let deleteUrl = `/delete_song/${songId}/`;
        console.log("Delete URL:", deleteUrl);
        xhr.open('POST', deleteUrl);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        // Remove the deleted song from the table
                        let row = document.getElementById('song-row-' + songId);
                        if (row) {
                            row.parentNode.removeChild(row);
                        }
                    } else {
                        alert('Failed to delete the song.');
                    }
                } else {
                    alert('Failed to delete the song.');
                }
                // Hide the dialog box after completing the operation
                document.getElementById('delete-song-dialog').style.display = 'none';
            }
        };

        xhr.send();
    });
}

function deleteAlbum(albumId) {
    // Show the delete album dialog box
    document.getElementById('delete-album-dialog').style.display = 'block';

    // Event listener for cancel delete button
    document.getElementById('cancel-album-delete').addEventListener('click', function () {
        // Hide the dialog box when cancel is clicked
        document.getElementById('delete-album-dialog').style.display = 'none';
    });

    // Event listener for confirm delete button
    document.getElementById('confirm-album-delete').addEventListener('click', function () {
        // Submit the form to delete the album
        document.getElementById('delete-album-form').submit();
    });
}

// Show the correct section based on local storage value or default to 'view' in profile/album

function showSection(section) {
    var viewBtn = document.getElementById('view-btn');
    var addSongBtn = document.getElementById('add-song-btn');
    var songsDetails = document.getElementById('songs-bottom-details');
    var addSongForm = document.getElementById('add-song-form');

    if (section === 'view') {
        songsDetails.style.display = 'block';
        addSongForm.style.display = 'none';
        viewBtn.classList.add('active');
        addSongBtn.classList.remove('active');
    } else if (section === 'add-song') {
        songsDetails.style.display = 'none';
        addSongForm.style.display = 'block';
        viewBtn.classList.remove('active');
        addSongBtn.classList.add('active');
    }

    // Store the last clicked section in local storage
    localStorage.setItem('lastClickedSection', section);
}

// Show the correct section based on local storage value or default to 'view' in profile/album
document.addEventListener('DOMContentLoaded', function () {
    var lastClickedSection = "{{ last_clicked_section }}";
    showSection(lastClickedSection);
});

// to delete comment
document.addEventListener('DOMContentLoaded', function () {
    const deleteCommentButtons = document.querySelectorAll('#delete-comment');
    console.log(deleteCommentButtons)
    const deleteCommentDialog = document.getElementById('delete-song-dialog');
    const cancelDeleteCommentBtn = document.getElementById('cancel-delete-comment');
    const confirmDeleteCommentBtn = document.getElementById('confirm-delete-comment');

    // Add event listeners to delete buttons
    deleteCommentButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default form submission
            deleteCommentDialog.style.display = 'block';
        });
    });

    // Event listener for cancel delete button
    cancelDeleteCommentBtn.addEventListener('click', function () {
        deleteCommentDialog.style.display = 'none';
    });

    // Event listener for confirm delete button
    confirmDeleteCommentBtn.addEventListener('click', function () {
        // Here you can submit the delete form or perform any other action
        document.querySelector('.delete-form').submit(); // Submit the delete form
        deleteCommentDialog.style.display = 'none';
    });
});