// ============  УДАЛЕНИЕ ВИДЕО =========

function addDeleteModal() {
    let modal = document.querySelector('.mod')
    modal.classList.add('is-active')
}

function removeDeleteModal() {
    let modal = document.querySelector('.mod')
    modal.classList.remove('is-active')
}

// ========================================================


//================== КОММЕНТЫ =============================

function addCommentModal() {
    let modal = document.querySelector('.mod_comment')
    modal.classList.add('is-active')
}

function removeCommentModal() {
    let modal = document.querySelector('.mod_comment')
    modal.classList.remove('is-active')
}


function addComment(pk){
    let comment = document.querySelector('.parent-comment-' + pk)
    comment.classList.toggle('is-hidden')
}

function toggleButParent(pk){
    let but = document.querySelector('.cart-parent-' + pk)
    but.classList.toggle('is-hidden')
}

function toggleParentForm(pk) {
    let form = document.querySelector('.par-comment-' + pk)
    form.classList.toggle('is-hidden')
}
//=========================================================