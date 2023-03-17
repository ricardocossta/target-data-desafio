const todoForm = document.querySelector('#todo-form');
const addFormInput = document.querySelector('#add-input');
const editForm = document.querySelector('#edit-form');
const editFormInput = document.querySelector('#edit-input');
const cancelEditBtn = document.querySelector('#cancel-edit-btn');
const todoItems = document.querySelector('.todos-items');

let = oldTodoTitle = '';

const todos = [
]


function changeBorderColorWhenInputNotEmpty() {
    if (addFormInput.value !== '') {
        addFormInput.style.borderColor = '#002554';
        addFormInput.style.boxShadow = '0 0 10px #002554';
    } else {
        addFormInput.style.borderColor = '';
        addFormInput.style.boxShadow = '';
    }
}

cancelEditBtn.addEventListener('click', e => {
    e.preventDefault();
    editForm.style.display = 'none';
    todoForm.style.display = 'flex';
    todoItems.style.display = 'block';
    addFormInput.focus();
});

addFormInput.addEventListener('input', changeBorderColorWhenInputNotEmpty);

todoForm.addEventListener('submit', e => {
    e.preventDefault();
    addTodo();
});

editForm.addEventListener('submit', e => {
    e.preventDefault();
    editTodo();
    editForm.style.display = 'none';
    todoForm.style.display = 'flex';
    todoItems.style.display = 'block';
    addFormInput.focus();
});

function addTodo() {
    const title = addFormInput.value;
    if (title && !todos.some(todo => todo.title === title)) {        
        todos.push({
            id : todos.length + 1,
            title : title,
        });
    }
    else {
        if (!title) {
            alert('Digite uma tarefa');
        }
        else {
            alert('Essa tarefa ja existe');
        }
    }
    showAllTodos();
    console.log(todos);
}

function editTodo() {
    const title = editFormInput.value;
    if (title && !todos.some(todo => todo.title === title)) {
        todos.forEach(todo => {
            if (todo.title === oldTodoTitle) {
                todo.title = title;
            }
        });
    }
    else {
        if (!title) {
            alert('Digite uma tarefa');
        }
        else {
            alert('Essa tarefa ja existe');
        }
    }
    showAllTodos();
    console.log(todos);
}

function showAllTodos() {
    todoItems.innerHTML = '';
    todos.forEach(todo => {
        const todoItem = document.createElement('li');
        todoItem.classList.add('todo-item');

        const todoTitleDiv = document.createElement('div');
        todoItem.appendChild(todoTitleDiv);
        todoTitleDiv.classList.add('todo-sentence');

        const todoTitle = document.createElement('h3');
        todoTitle.textContent = todo.title;
        todoTitleDiv.appendChild(todoTitle);

        const buttonsDiv = document.createElement('div');
        buttonsDiv.classList.add('todo-buttons');
        todoItem.appendChild(buttonsDiv);

        const finishTodoBtn = document.createElement('button');
        finishTodoBtn.classList.add('finish-todo-btn');
        finishTodoBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
        const editTodoBtn = document.createElement('button');
        editTodoBtn.classList.add('edit-todo-btn');
        editTodoBtn.innerHTML = '<i class="fa-solid fa-pen"></i>';
        const removeTodoBtn = document.createElement('button');
        removeTodoBtn.classList.add('remove-todo-btn');
        removeTodoBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i>';

        buttonsDiv.appendChild(finishTodoBtn);
        buttonsDiv.appendChild(editTodoBtn);
        buttonsDiv.appendChild(removeTodoBtn);

        todoItems.appendChild(todoItem);
    });
}

function removeTodo(name) {
    todos.forEach((todo, index) => {
        if (todo.title === name) {
            todos.splice(index, 1);
        }
    });
    showAllTodos();
    console.log(todos);
}

document.addEventListener('click', e => {
    parentDiv = e.target.parentElement.parentElement;

    if (e.target.classList.contains('finish-todo-btn')) {   
        const title = parentDiv.querySelector('.todo-sentence h3');
        title.classList.toggle('done');
    }
    
    if (e.target.classList.contains('edit-todo-btn')) {
        const title = parentDiv.querySelector('.todo-sentence h3').textContent;
        editFormInput.value = title;
        oldTodoTitle = title;
        todoForm.style.display = 'none';
        editForm.style.display = 'flex';
        todoItems.style.display = 'none';
        editFormInput.focus();
    }
    
    if (e.target.classList.contains('remove-todo-btn')) {
        const title = parentDiv.querySelector('.todo-sentence h3').textContent;
        removeTodo(title);
    }
});

