var quill = new Quill('#editor', {
    modules: {
        toolbar: [
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            [{ 'size': ['small', false, 'large', 'huge'] }],
            [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'list': 'check' }],
            ['bold', 'italic', 'underline'],
            ['image', 'code-block', 'link', 'formula'],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'font': [] }],
            [{ 'align': [] }],
            ['clean']
        ],
    },
    placeholder: 'Compose an epic...',
    theme: 'snow',
});

document.querySelector('form').onsubmit = function () {
    var content = document.querySelector('input[name=content]');
    content.value = quill.root.innerHTML;
};