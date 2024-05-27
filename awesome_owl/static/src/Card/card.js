/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card"

    static props = {
        title: {
            type: String
        },
        slots: {
            type: Object,
            shape: {body: true}
        }
    }

    setup() {
        this.state = useState({showBody: true})
    }

    toggleShowBody() {
        console.log('test', this.state.showBody)
        this.state.showBody = !this.state.showBody
    }
}