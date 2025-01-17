/** @odoo-module **/

import {NumberCard} from "./components/NumberCard/number_card";
import {PieChartCard} from "./components/PieChartCard/pie_chart_card";
import {registry} from "@web/core/registry";

const items = [
    {
        id: "average_quantity",
        description: "Average amount of t-shirt",
        Component: NumberCard,
        props: (data) => ({
            title: "Average amount of t-shirt by order this month",
            value: data.average_quantity
        })
    },
    {
        id: "average_time",
        description: "Average time for an order",
        Component: NumberCard,
        props: (data) => ({
            title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
            value: data.average_time,
        })
    },
    {
        id: "nb_new_orders",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.nb_new_orders,
        })
    },
    {
        id: "nb_cancelled_orders",
        description: "Number of cancelled orders this month",
        Component: NumberCard,
        props: (data) => ({
            title: "Number of cancelled orders this month",
            value: data.nb_cancelled_orders,
        })
    },
    {
        id: "total_amount",
        description: "Total amount of new orders this month",
        Component: NumberCard,
        size: 1,
        props: (data) => ({
            title: "Total amount of new orders this month",
            value: data.total_amount,
        })
    },
    {
        id: "orders_by_size",
        description: "Shirt order by size",
        Component: PieChartCard,
        size: 1,
        props: (data) => ({
            title: "Shirt order by size",
            value: data.orders_by_size,
        })
    },
]

items.forEach((data) => {
    registry.category("awesome_dashboard").add(data.id, data)
})