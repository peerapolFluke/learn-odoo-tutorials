/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {TodoItem} from "../TodoItem/todo_item";
import {useAutofocus} from "../../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = {TodoItem}

    setup() {
        this.todos = useState([]);
        useAutofocus("todo_input")
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push({
                id: this.todos.length + 1,
                description: ev.target.value,
                isCompleted: false
            })
            ev.target.value = ""
        }
    }

    onToggle(id) {
        console.log('test', id, this.todos)
        const todo = this.todos.find((i) => i.id === id)
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodo(id) {
        const todoIndex = this.todos.findIndex((i) => i.id === id)
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1)
        }
    }
}