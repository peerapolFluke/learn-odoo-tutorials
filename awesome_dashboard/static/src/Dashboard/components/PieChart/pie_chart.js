/** @odoo-module */

import {loadJS} from "@web/core/assets";
import {Component, onMounted, onWillStart, onWillUnmount, useRef} from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: {
            type: Object,
            shape: {
                s: Number,
                m: Number,
                xl: Number,
            }
        }
    }

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"])
        });
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        // @ts-ignore
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        data: Object.values(this.props.data),
                    },
                ],
            },
        });
    }
}