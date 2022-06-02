function editNote(noteId) {
    fetch("/edit-note", 
    {method: "FETCH", body: JSON.stringify({noteId: noteId})}).then((_res) => {window.location.href = "/"})
}

// function hideNote(noteId) {
//     fetch("/delete-note", 
//     {method: "POST", body: JSON.stringify({noteId: noteId})}).then((_res) => {window.location.href = "/"})
// }

function deleteNote(noteId) {
    fetch("/delete-note", 
    {method: "POST", body: JSON.stringify({noteId: noteId})}).then((_res) => {window.location.href = "/"})
}