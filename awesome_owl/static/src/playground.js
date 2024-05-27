/** @odoo-module **/

import {Component, markup, useState} from "@odoo/owl";

import {Counter} from "./Counter/counter";
import {Card} from "./Card/card";
import {TodoList} from "./todo/TodoList/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {
        Counter, Card, TodoList
    }

    setup() {
        this.cardContent = markup("<div>some text 2</div>")
        this.state = useState({totalCounter: 0})
    }

    onCounterChange() {
        this.state.totalCounter++
    }

}
