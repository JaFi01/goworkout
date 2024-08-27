document.addEventListener('DOMContentLoaded', function() {
    //  AJAX handling
    function handleAjaxRequest(url, method, data, successCallback, errorCallback) {
        fetch(url, {
            method: method,
            body: data,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(successCallback)
        .catch(errorCallback);
    }

    // "How to" button
    const howToButtons = document.querySelectorAll('.how-to');
    howToButtons.forEach(button => {
        button.addEventListener('click', function() {
            const instructionsRow = this.closest('tr').nextElementSibling;
            if (instructionsRow.style.display === 'none' || instructionsRow.style.display === '') {
                instructionsRow.style.display = 'table-row';
            } else {
                instructionsRow.style.display = 'none';
            }
        });
    });

    // Obsługa przycisku YouTube
    const youtubeButtons = document.querySelectorAll('.youtube-button');
    youtubeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const exerciseName = this.getAttribute('data-exercise-name');
            const searchQuery = encodeURIComponent(exerciseName + " exercise");
            const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${searchQuery}`;
            window.open(youtubeSearchUrl, '_blank');
        });
    });

    // Handling "Ask AI"
    const askAIButton = document.getElementById('askAIButton');
    if (askAIButton) {
        askAIButton.addEventListener('click', function() {
            const routineId = this.dataset.routineId; // Add the data-routine-id attribute in HTML
            handleAjaxRequest(
                `/workout-routines/${routineId}/ask-ai/`,
                'POST',
                JSON.stringify({}),
                function(data) {
                    document.getElementById('aiResponseContent').innerHTML = data.ai_response;
                    document.getElementById('aiResponse').style.display = 'block';
                },
                function(error) {
                    console.error('Error:', error);
                    alert('An error occurred while communicating with AI. Please try again later.');
                }
            );
        });
    } else {
        console.warn('Przycisk "Ask AI" nie został znaleziony na stronie.');
    }

    // add exercise handling
    const addButtons = document.querySelectorAll('.add-exercise');
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const planId = this.dataset.planId;
            const form = document.getElementById(`exercise-form-${planId}`);
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        });
    });

    const forms = document.querySelectorAll('.exercise-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/add-exercise/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Błąd podczas dodawania ćwiczenia');
                }
            });
        });
    });

    // edit exercise handling
    const editButtons = document.querySelectorAll('.edit-exercise');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const exerciseId = this.dataset.exerciseId;
            const editForm = document.getElementById(`edit-form-${exerciseId}`);
            editForm.style.display = 'table-row';
            this.closest('tr').style.display = 'none';
        });
    });

    const cancelButtons = document.querySelectorAll('.cancel-edit');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function() {
            const editForm = this.closest('tr');
            editForm.style.display = 'none';
            editForm.previousElementSibling.style.display = 'table-row';
        });
    });

    const editForms = document.querySelectorAll('.exercise-edit-form');
    editForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/edit-exercise/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error during editing of exercise');
                }
            });
        });
    });

    // handling exercise delete
    const deleteButtons = document.querySelectorAll('.delete-exercise');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const exerciseId = this.dataset.exerciseId;
            if (confirm('Are You sure You want to delete this exercise?')) {
                fetch(`/delete-exercise/${exerciseId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error during removal of exercise');
                    }
                });
            }
        });
    });

    // routine analysis handling
    const analyzeButton = document.getElementById('analyzeButton');
    if (analyzeButton) {
        analyzeButton.addEventListener('click', function() {
            const routineId = this.dataset.routineId;
            fetch(`/workout-routines/${routineId}/analyze/`)
                .then(response => response.json())
                .then(data => {
                    console.log('Analysis completed. Check the server console.');
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
});

// showing instructions
window.showInstructions = function(exerciseId) {
    console.log('Show instructions clicked for exercise:', exerciseId);
    
    var instructionsRow = document.getElementById('instructions-' + exerciseId);
    if (!instructionsRow) {
        console.error('No instruction row found for exercise:', exerciseId);
        return;
    }
    var instructionsContent = instructionsRow.querySelector('.instructions-content');

    if (instructionsRow.style.display === 'table-row') {
        instructionsRow.style.display = 'none';
        return;
    }

    fetch('/exercise/' + exerciseId + '/instructions/')
        .then(response => response.json())
        .then(data => {
            //console.log('Otrzymane instrukcje:', data);
            if (data.instructions && data.instructions.length > 0) {
                var instructions = data.instructions.join('<br>');
                instructionsContent.innerHTML = instructions;
                instructionsRow.style.display = 'table-row';
            } else {
                instructionsContent.innerHTML = 'No instructions available.';
                instructionsRow.style.display = 'table-row';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to fetch instructions. Error: ' + error);
        });
};