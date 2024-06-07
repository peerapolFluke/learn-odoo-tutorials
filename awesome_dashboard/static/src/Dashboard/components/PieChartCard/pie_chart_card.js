/** @odoo-module **/
import {Component} from "@odoo/owl";
import {PieChart} from "../PieChart/pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard"
    static components = {PieChart}
    static props = {
        title: String,
        value: {
            type: Object,
            shape: {
                s: Number,
                m: Number,
                xl: Number,
            }
        }
    }
}